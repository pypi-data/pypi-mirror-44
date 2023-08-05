import warnings
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import norm

from zepid.causal.ipw import propensity_score


class AIPTW:
    r"""Augmented inverse probablity weight estimator. This is a simple implementation of AIPW for a time-fixed exposure
    and a single time-point outcome. `AIPTW` does not account for missing data.

    AIPTW have a desirable property compared to either the g-formula or IPTW. Both of the prior estimators require that
    we specify our parametric regression models correctly. AIPTW allows us to have two 'chances' at getting the model
    correct. If either our outcome-model or treatment-model is correctly specified, then our estimate will be unbiased

    The augment-inverse probability weights are calculated from the following formula

    .. math::

        \widehat{DR}(a) = \frac{YA}{\widehat{\Pr}(A=a|L)} - \frac{\hat{Y}^a*(A-\widehat{\Pr}(A=a|L)}{
        \widehat{\Pr}(A=a|L)}

    The risk difference and risk ratio are calculated using the following formulas, respectively

    .. math::

        \widehat{RD} = \widehat{DR}(a=1) - \widehat{DR}(a=0)

    .. math::

        \widehat{RR} = \frac{\widehat{DR}(a=1)}{\widehat{DR}(a=0)}

    Confidence intervals for the risk difference come from the influence curve. Confidence intervals for the risk ratio
    are less straight-forward. To get confidence intervals for the risk ratio, a bootstrap procedure should be used

    Parameters
    ----------
    df : DataFrame
        Pandas DataFrame object containing all variables of interest
    exposure : str
        Column name of the exposure variable. Currently only binary is supported
    outcome : str
        Column name of the outcome variable. Currently only binary is supported
    alpha : float, optional
        Alpha for confidence interval level. Default is 0.05, returning the 95% CL

    Examples
    --------
    Set up the environment and the data set

    >>> from zepid import load_sample_data, spline
    >>> from zepid.causal.doublyrobust import AIPTW
    >>> df = load_sample_data(timevary=False)
    >>> df[['cd4_rs1','cd4_rs2']] = spline(df,'cd40',n_knots=3,term=2,restricted=True)
    >>> df[['age_rs1','age_rs2']] = spline(df,'age0',n_knots=3,term=2,restricted=True)

    Initialize the AIPTW model

    >>> aipw = AIPTW(df, exposure='art', outcome='dead')

    Specify the exposure/treatment model

    >>> aipw.exposure_model('male + age0 + age_rs1 + age_rs2 + cd40 + cd4_rs1 + cd4_rs2 + dvl0')

    Specify the outcome model

    >>> aipw.outcome_model('art + male + age0 + age_rs1 + age_rs2 + cd40 + cd4_rs1 + cd4_rs2 + dvl0')

    Estimate the risk difference and risk ratio

    >>> aipw.fit()

    Displaying the results

    >>> aipw.summary()

    Extracting risk difference and risk ratio respectively

    >>> aipw.risk_difference
    >>> aipw.risk_ratio

    References
    ----------
    Funk, M. J., Westreich, D., Wiesen, C., Stürmer, T., Brookhart, M. A., & Davidian, M. (2011). Doubly robust
    estimation of causal effects. American Journal of Epidemiology, 173(7), 761-767.

    Lunceford JK, Davidian M. (2004). Stratification and weighting via the propensity score in estimation of causal
    treatment effects: a comparative study. Statistics in medicine, 23(19), 2937-2960.
    """
    def __init__(self, df, exposure, outcome, alpha=0.05):
        self.df = df.copy()
        if df.dropna().shape[0] != df.shape[0]:
            warnings.warn("There is missing data in the dataset. By default, AIPTW will drop all missing data. AIPTW "
                          "will fit "+str(df.dropna().shape[0])+' of '+str(df.shape[0])+' observations', UserWarning)
        self.df = df.copy().dropna().reset_index()
        self._exposure = exposure
        self._outcome = outcome
        self.alpha = alpha

        self.risk_difference = None
        self.risk_ratio = None
        self.risk_difference_ci = None
        self.risk_ratio_ci = None

        self._fit_exposure_ = False
        self._fit_outcome_ = False
        self._exp_model = None
        self._out_model = None

    def exposure_model(self, model, print_results=True):
        r"""Specify the propensity score / inverse probability weight model. Model used to predict the exposure via a
        logistic regression model. This model estimates

        .. math::

            \widehat{\Pr}(A=1|L) = logit^{-1}(\widehat{\beta_0} + \widehat{\beta} L)

        Parameters
        ----------
        model : str
            Independent variables to predict the exposure. For example, 'var1 + var2 + var3'
        print_results : bool, optional
            Whether to print the fitted model results. Default is True (prints results)
        """
        self._exp_model = self._exposure + ' ~ ' + model
        fitmodel = propensity_score(self.df, self._exp_model, print_results=print_results)
        self.df['_ps_'] = fitmodel.predict(self.df)
        self._fit_exposure_ = True

    def outcome_model(self, model, print_results=True):
        r"""Specify the outcome model. Model used to predict the outcome via a logistic regression model

        .. math::

            \widehat{\Pr}(Y|A,L) = logit^{-1}(\widehat{\beta_0} + \widehat{\beta_1} A + \widehat{\beta} L)

        Parameters
        ----------
        model : str
            Independent variables to predict the outcome. For example, 'var1 + var2 + var3 + var4'
        print_results : bool, optional
            Whether to print the fitted model results. Default is True (prints results)
        """
        self._out_model = self._outcome + ' ~ ' + model
        f = sm.families.family.Binomial()
        log = smf.glm(self._out_model, self.df, family=f).fit()
        if print_results:
            print('\n----------------------------------------------------------------')
            print('MODEL: ' + self._out_model)
            print('-----------------------------------------------------------------')
            print(log.summary())

        dfx = self.df.copy()
        dfx[self._exposure] = 1
        self.df['_pY1_'] = log.predict(dfx)
        dfx = self.df.copy()
        dfx[self._exposure] = 0
        self.df['_pY0_'] = log.predict(dfx)
        self._fit_outcome_ = True

    def fit(self):
        """Once the exposure and outcome models are specified, we can estimate the risk ratio and risk difference.

        Returns
        -------
        Gains `risk_difference`, `risk_difference_ci`, and `risk_ratio` values
        """
        if (self._fit_exposure_ is False) or (self._fit_outcome_ is False):
            raise ValueError('The exposure and outcome models must be specified before the doubly robust estimate can '
                             'be generated')

        # Doubly robust estimator under all treated
        a_obs = self.df[self._exposure]
        y_obs = self.df[self._outcome]
        ps = self.df['_ps_']
        py_a1 = self.df['_pY1_']
        py_a0 = self.df['_pY0_']
        dr_a1 = np.where(a_obs == 1,
                         (y_obs / ps) - ((py_a1 * (1 - ps)) / ps),
                         py_a1)

        # Doubly robust estimator under all untreated
        dr_a0 = np.where(a_obs == 1,
                         py_a0,
                         (y_obs / (1 - ps) - ((py_a0 * ps) / (1 - ps))))

        # Generating estimates for the risk difference and risk ratio
        self.risk_difference = np.mean(dr_a1) - np.mean(dr_a0)
        self.risk_ratio = np.mean(dr_a1) / np.mean(dr_a0)

        var_ic = np.var((dr_a1 - dr_a0) - self.risk_difference, ddof=1) / self.df.shape[0]
        zalpha = norm.ppf(1 - self.alpha / 2, loc=0, scale=1)
        self.risk_difference_ci = [self.risk_difference - zalpha * np.sqrt(var_ic),
                                   self.risk_difference + zalpha * np.sqrt(var_ic)]

    def summary(self, decimal=3):
        """Prints a summary of the results for the doubly robust estimator. Confidence intervals are only available for
        the risk difference currently

        Parameters
        ----------
        decimal : int, optional
            Number of decimal places to display in the result
        """
        if (self._fit_exposure_ is False) or (self._fit_exposure_ is False):
            raise ValueError('The exposure and outcome models must be specified before the double robust estimate can '
                             'be generated')

        print('======================================================================')
        print('           Augment Inverse Probability of Treatment Weights           ')
        print('======================================================================')
        print('Risk Difference:   ', round(float(self.risk_difference), decimal))
        print(str(round(100 * (1 - self.alpha), 1)) + '% two-sided CI: (' +
              str(round(self.risk_difference_ci[0], decimal)), ',',
              str(round(self.risk_difference_ci[1], decimal)) + ')')
        print('----------------------------------------------------------------------')
        print('Risk Ratio:        ', round(float(self.risk_ratio), decimal))
        print(str(round(100 * (1 - self.alpha), 1)) + '% two-sided CI: -')
        print('======================================================================')
