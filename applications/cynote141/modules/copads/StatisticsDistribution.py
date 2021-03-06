"""
File containing the functions for various statistical distributions.
References:
1. Regress+ A compendium of common probability distributions (version 2.3)
by Michael P. McLaughlin (mpmcl@mitre.org)
http://www.causascientia.org/math_stat/Dists/Compendium.pdf
2. Hand-book on statistical distributions for experimentalists
Internal report SUF-PFY/96-01. University of Stockholms
by Christian Walck (walck@physto.se)


Distribution
|- BetaDistribution(location, scale, p, q)
|  |- PowerFunctionDistribution(shape)
|- BinomialDistribution(success, trial)
|  |- BernoulliDistribution(success)  
|- BradfordDistribution
|- BurrDistribution
|- CauchyDistribution(location = 0.0, scale = 1.0)
|  |- LorentzDistribution (alias of CauchyDistribution)
|- ChiDistribution
|  |- HalfNormalDistribution(location, scale)
|  |- MaxwellDistribution(scale)
|  |- RayleighDistribution(scale)
|- CosineDistribution(location = 0.0, scale = 1.0)
|- DoubleGammaDistribution
|- DoubleWeibullDistribution
|- ExponentialDistribution(location = 0.0, scale = 1.0)
|  |- NegativeExponentialDistribution (alias of ExponentialDistribution)
|- ExtremeLBDistribution
|- FDistribution
|- FiskDistribution
|  |- LogLogisticDistribution (alias of FiskDistribution)
|- FoldedNormalDistribution
|- GammaDistribution
|  |- ChiSquareDistribution(df)
|  |- ErlangDistribution(shape)
|  |- FurryDistribution (alias of GammaDistribution)
|- GenLogisticDistribution
|- GeometricDistribution(success = 0.5)
|- GumbelDistribution(location, scale)
|  |- FisherTippettDistribution (alias of GumbelDistribution)
|  |- GompertzDistribution  (alias of GumbelDistribution)
|  |- LogWeibullDistribution (alias of GumbelDistribution)
|- HyperbolicSecantDistribution
|- HypergeometricDistribution
|- InverseNormalDistribution
|  |- WaldDistribution (alias of InverseNormalDistribution)
|- LaplaceDistribution
|  |- BilateralExponentialDistribution (alias of LaplaceDistribution)
|  |- DoubleExponentialDistribution (alias of LaplaceDistribution)
|- LogarithmicDistribution(shape)
|- LogisticDistribution
|  |- SechSquaredDistribution (alias of LogisticDistribution)
|- LogNormalDistribution
|  |- AntiLogNormalDistribution (alias of LogNormalDistribution)
|  |- CobbDouglasDistribution (alias of LogNormalDistribution)
|- NakagamiDistribution
|- NegativeBinomialDistribution(success, target)
|  |- PascalDistribution(success, target)
|  |- PolyaDistribution (alias of NegativeBinomialDistribution)
|- NormalDistribution()
|- ParetoDistribution(location = 1.0, shape = 1.0)
|- PoissonDistribution(expectation)
|- RademacherDistribution()
|- ReciprocalDistribution
|- SemicircularDistribution(location = 0.0, scale = 1.0)
|- TDistribution(location = 0.0, scale = 1.0, shape = 2)
|- TriangularDistribution
|- UniformDistribution(location, scale)
|  |- RectangularDistribution (alias of UniformDistribution)
|- WeibullDistribution
   |- FrechetDistribution (alias of WeibullDistribution)


Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>
Date created: 17th August 2005
"""

import math
import random
from CopadsExceptions import DistributionParameterError
from CopadsExceptions import DistributionFunctionError
from CopadsExceptions import NormalDistributionTypeError
import NRPy
from Constants import *

class Distribution:
    """
    Abstract class for all statistical distributions.
    Due to the large variations of parameters for each distribution, it is
    unlikely to be able to standardize a parameter list for each method that
    is meaningful for all distributions. Instead, the parameters to construct
    each distribution is to be given as keyword arguments.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, **parameters):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.
        """
        raise NotImplementedError

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability. CDF is
        also known as density function.
        """
        raise NotImplementedError

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability for the
        particular value of x, or the area under probability distribution from
        x-h to x+h for continuous distribution.
        """
        raise NotImplementedError

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability value and
        returns the corresponding value on the x-axis.
        """
        raise NotImplementedError

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        raise NotImplementedError

    def mode(self):
        """
        Gives the mode of the sample, if closed-form is available.
        """
        raise NotImplementedError

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        raise NotImplementedError

    def skew(self):
        """
        Gives the skew of the sample.
        """
        raise NotImplementedError

    def variance(self):
        """
        Gives the variance of the sample.
        """
        raise NotImplementedError
    
# ----------------------------------------------------------
# Tested Distributions
# ----------------------------------------------------------

class BetaDistribution(Distribution):
    """
    Class for Beta Distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, location, scale, p, q):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameters:
        1. location
        2. scale (upper bound)
        3. p (shape parameter. Although no upper bound but seldom
           exceed 10.)
        4. q (shape parameter. Although no upper bound but seldom
           exceed 10.)
        """
        self.location = float(location)
        self.scale = float(scale)
        self.p = float(p)
        self.q = float(q)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        return NRPy.betai(self.p, self.q, (x - self.location)/
                         (self.scale - self.location))

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability
        for particular value of x, or the area under probability
        distribution from x-h to x+h for continuous distribution.
        """
        n = (self.scale - self.location) ** (self.p + self.q - 1)
        n = NRPy.gammln(self.p) * NRPy.gammln(self.q) * n
        n = NRPy.gammln(self.p + self.q) / n
        p = (x - self.location) ** (self.p - 1)
        q = (self.scale - x) ** (self.q - 1)
        return n * p * q

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability
        value and returns the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        n = (self.location * self.q) + (self.scale * self.p)
        return n / (self.p + self.q)

    def mode(self):
        """
        Gives the mode of the sample.
        """
        n = (self.location * (self.q - 1)) + (self.scale * \
            (self.p - 1))
        return n / (self.p + self.q - 2)

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        n = (self.p ** 2) * (self.q + 2) + \
            (2 * (self.q ** 2)) + \
            ((self.p * self.q) * (self.q - 2))
        n = n * (self.p + self.q + 1)
        d = self.p * self.q * (self.p + self.q + 2) * \
            (self.p + self.q + 3)
        return 3 * ((n / d) - 1)

    def skew(self):
        """
        Gives the skew of the sample.
        """
        d = (self.p + self.q) ** 3
        d = d * (self.p + self.q + 1) * (self.p + self.q + 2)
        e = ((self.p + self.q) ** 2) * (self.p + self.q + 1)
        e = (self.p * self.q) / e
        e = e ** 1.5
        return ((2 * self.p * self.q) * (self.q - self.q)) / (d * e)

    def variance(self):
        """
        Gives the variance of the sample.
        """
        n = self.p * self.q * ((self.scale - self.location) ** 2)
        d = (self.p + self.q + 1) * ((self.p + self.q) ** 2)
        return n / d

    def moment(self, r):
        """
        Gives the r-th moment of the sample.
        """
        return NRPy.beta(self.p + r,
            self.q)/NRPy.beta(self.p, self.q)

    def random(self):
        """
        Gives a random number based on the distribution.
        """
        return random.betavariate(self.p, self.q)
    

class BinomialDistribution(Distribution):
    """
    Class for Binomial Distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, success=0.5, trial=1000):
        """
        Constructor method. The parameters are used to construct
        the probability distribution.

        Parameters:
        1. success (probability of success; 0 <= success <= 1)
        2. trial (number of Bernoulli trials)
        """
        self.success = float(success)
        self.trial = int(trial)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        return NRPy.cdf_binomial(x, self.trial, self.success)

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability for the
        particular value of x, or the area under probability distribution from
        x-h to x+h for continuous distribution.
        """
        x = int(x)
        return NRPy.bico(self.trial, x) * \
            (self.success ** x) * \
            ((1 - self.success) ** (self.trial - x))

    def inverseCDF(self, probability, start=0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability
        value and returns the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return self.success * self.trial

    def mode(self):
        """
        Gives the mode of the sample.
        """
        return int(self.success * (self.trial + 1))

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        return (1 - ((6 * self.success * (1 - self.success))) /
            (self.trial * self.success * (1 - self.success)))

    def skew(self):
        """
        Gives the skew of the sample.
        """
        return (1 - self.success - self.success)/ \
            ((self.trial * self.success * (1 - self.success)) ** 0.5)

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return self.mean() * (1 - self.success)


class CauchyDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (default = 0.0)
        2. scale (lambda; default = 1.0)"""
        try: self.location = parameters['location']
        except KeyError: self.location = 0.0
        try: self.scale = parameters['scale']
        except KeyError: self.scale = 1.0
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return 0.5 + 1/PI * math.atan((x-self.location)/self.scale)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return 1 / (PI * self.scale * \
            (1 + (((x - self.location)/self.scale) ** 2)))
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        raise DistributionFunctionError('Mean for Cauchy Distribution is \
            undefined')
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def median(self): 
        """Gives the median of the sample."""
        return self.location
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location - self.scale
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        return self.location + self.scale
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.5
    def random(self, seed):
        """Gives a random number based on the distribution."""
        while 1:
            seed = self.loaction + (self.scale * math.tan(PI * (seed - 0.5)))
            yield seed


def ErlangDistribution(**parameters):
    """
    Erlang distribution is an alias of Gamma distribution where the shape
    parameter is an integer."""
    try: parameters['shape'] = int(parameters['shape'])
    except KeyError: 
            raise DistributionParameterError('Erlang distribution requires \
            shape parameter')
    return GammaDistribution(**parameters)


class FDistribution(Distribution):
    """
    Class for F Distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, df1=1, df2=1):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameters:
        1. df1 (degrees of freedom for numerator)
        2. df2 (degrees of freedom for denorminator)
        """
        self.df1 = float(df1)
        self.df2 = float(df2)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        sub_x = (self.df1 * x) / (self.df1 * x + self.df2)
        return NRPy.betai(self.df1 / 2.0, self.df2 / 2.0, sub_x)

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability
        for particular value of x, or the area under probability
        distribution from x-h to x+h for continuous distribution.
        """
        x = float(x)
        n1 = ((x * self.df1) ** self.df1) * (self.df2 ** self.df2)
        n2 = (x * self.df1 + self.df2) ** (self.df1 + self.df2)
        d = x * NRPy.beta(self.df1 / 2.0, self.df2 / 2.0)
        return math.sqrt(n1 / n2) / d

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return float(self.df2 / (self.df2 - 2))


def FurryDistribution(**parameters):
    """
    Furry distribution is an alias of Gamma distribution."""
    return GammaDistribution(**parameters)


class GammaDistribution(Distribution):
    """
    Class for Gamma Distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, location, scale, shape):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameters:
        1. location
        2. scale
        3. shape"""
        self.location = float(location)
        self.scale = float(scale)
        self.shape = float(shape)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        return NRPy.gammp(self.shape,
                          (x - self.location) / self.scale)

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return self.location + (self.scale * self.shape)

    def mode(self):
        """
        Gives the mode of the sample.
        """
        return self.location + (self.scale * (self.shape - 1))

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        return 6 / self.shape

    def skew(self):
        """
        Gives the skew of the sample.
        """
        return 2 / math.sqrt(self.shape)

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return self.scale * self.scale * self.shape

    def qmean(self):
        """
        Gives the quantile of the arithmetic mean of the sample.
        """
        return NRPy.gammp(self.shape, self.shape)

    def qmode(self):
        """
        Gives the quantile of the mode of the sample.
        """
        return NRPy.gammp(self.shape, self.shape - 1)


class ChiSquareDistribution(GammaDistribution):
    """
    Chi-square distribution is a special case of Gamma distribution where
    location = 0, scale = 2 and shape is twice that of the degrees of freedom.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, df=2):
        """
        Constructor method. The parameters are used to construct
        the probability distribution.

        Parameters:
        1. df = degrees of freedom"""
        GammaDistribution.__init__(self, location=0, scale=2,
                                   shape=float(df) / 2.0)
                                   
                                   
class GeometricDistribution(Distribution):
    """
    Geometric distribution is the discrete version of Exponential
    distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, success=0.5):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameters:
        1. success (probability of success; 0 <= success <= 1;
           default = 0.5)
           """
        self.prob = float(success)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        total = self.PDF(1)
        for i in range(2, int(x) + 1):
            total += self.PDF(i)
        return total

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability
        for particular value of x, or the area under probability
        distribution from x-h to x+h for continuous distribution.
        """
        return self.prob * ((1 - self.prob) ** (x - 1))

    def inverseCDF(self, probability, start=1, step=1):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return 1/self.prob

    def mode(self):
        """
        Gives the mode of the sample.
        """
        return 1.0

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return (1 - self.prob) / (self.prob ** 2)

    
class NormalDistribution(Distribution):
    """
    Class for standardized normal distribution (area under the curve = 1)
    
    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100 
    Statistical Tests. The Python Papers Source Codes 1:5
    """
    def __init__(self, **kwargs):
        self.mean = 0.0
        self.stdev = 1.0
    def CDF(self, x):
        return 1.0 - 0.5 * NRPy.erfcc(x/SQRT2)
    def PDF(self, x): 
        """
        Calculates the density (probability) at x by the formula:
        f(x) = 1/(sqrt(2 pi) sigma) e^-((x^2/(2 sigma^2))
        where mu is the mean of the distribution and sigma the standard 
        deviation.
        
        @param x: probability at x
        """
        return (1/(math.sqrt(PI2) * self.stdev)) * \
            math.exp(-(x ** 2/(2 * self.stdev**2)))
    def inverseCDF(self, probability, start = -10.0, 
                   end = 10.0, error = 10e-8): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis, together with the 
        cumulative probability.
        
        @param probability: probability under the curve from -infinity
        @param start: lower boundary of calculation (default = -10)
        @param end: upper boundary of calculation (default = 10)
        @param error: error between the given and calculated probabilities 
        (default = 10e-8)
        @return (start, cprob): 'start' is the standard deviation for the area 
        under the curve from -infinity to the given 'probability' (+/- step). 
        'cprob' is the calculated area under the curve from -infinity to the 
        returned 'start'.
        """
        # check for tolerance
        if abs(self.CDF(start)-probability) < error:
            return (start, self.CDF(start))
        # case 1: lower than -10 standard deviations
        if probability < self.CDF(start):
            return self.inverseCDF(probability, start-5, start, error)
        # case 2: between -10 to 10 standard deviations (bisection method)
        if probability > self.CDF(start) and \
        probability < self.CDF((start+end)/2):
            return self.inverseCDF(probability, start, (start+end)/2, error)
        if probability > self.CDF((start+end)/2) and \
        probability < self.CDF(end):
            return self.inverseCDF(probability, (start+end)/2, end, error)
        # case 3: higher than 10 standard deviations
        if probability > self.CDF(end):
            return self.inverseCDF(probability, end, end+5, error)
    def mean(self): 
        return self.mean
    def mode(self):
        return self.mean
    def kurtosis(self): 
        return 0.0
    def skew(self): 
        return 0.0
    def variance(self): 
        return self.stdev * self.stdev
    def random(self):
        """Gives a random number based on the distribution."""
        return random.gauss(self.mean, self.stdev)


class PoissonDistribution(Distribution):
    """
    Class for Poisson Distribution. Poisson distribution is binomial
    distribution with very low success - that is, for rare events.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, expectation=0.001):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameters:
        1. expectation (mean success probability; lambda)
        """
        self._mean = float(expectation)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        return NRPy.cdf_poisson(x + 1, self._mean)

    def PDF(self, x):
        """
        Partial Distribution Function, which gives the probability
        for particular value of x, or the area under probability
        distribution from x-h to x+h for continuous distribution.
        """
        return (math.exp(-1 ** self._mean) *
                (self._mean ** x)) / NRPy.factrl(x)

    def inverseCDF(self, probability, start=0.001, step=1):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return self._mean

    def mode(self):
        """
        Gives the mode of the sample.
        """
        return int(self._mean)

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return self._mean


class TDistribution(Distribution):
    """
    Class for Student's t-distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, location=0.0, scale=1.0, shape=2):
        """Constructor method. The parameters are used to construct
        the probability distribution.

        Parameter:
        1. location (default = 0.0)
        2. scale (default = 1.0)
        3. shape (degrees of freedom; default = 2)"""
        self._mean = float(location)
        self.stdev = float(scale)
        self.df = float(shape)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        t = (x - self._mean) / self.stdev
        a = NRPy.betai(self.df / 2.0, 0.5, self.df / (self.df + (t * t)))
        if t > 0:
            return 1 - 0.5 * a
        else:
            return 0.5 * a

    def PDF(self, x):
        """
        Calculates the density (probability) at x with n-th degrees of freedom
        as:
        f(x) = Gamma((n+1)/2) / (sqrt(n * pi) Gamma(n/2)) (1 +
                                 x^2/n)^-((n+1)/2)
        for all real x. It has mean 0 (for n > 1) and variance
        n/(n-2) (for n > 2)."""
        a = NRPy.gammln((self.df + 1) / 2)
        b = math.sqrt(math.pi * self.df) * NRPy.gammln(self.df / 2) * \
            self.stdev
        c = 1 + ((((x - self._mean) / self.stdev) ** 2) / self.df)
        return (a / b) * (c ** ((-1 - self.df) / 2))

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return self._mean

    def mode(self):
        """
        Gives the mode of the sample.
        """
        return self._mean

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        a = ((self.df - 2) ** 2) * NRPy.gammln((self.df / 2) - 2)
        return 3 * ((a / (4 * NRPy.gammln(self.df / 2))) - 1)

    def skew(self):
        """
        Gives the skew of the sample.
        """
        return 0.0

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return (self.df / (self.df - 2)) * self.stdev * self.stdev


class UniformDistribution(Distribution):
    """
    Class for Uniform distribution.
    
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python 
    Papers Source Codes 1:4
    """

    def __init__(self, location, scale):
        """
        Constructor method. The parameters are used to construct the
        probability distribution.

        Parameter:
        1. location
        2. scale
        """
        self.location = float(location)
        self.scale = float(scale)

    def CDF(self, x):
        """
        Cummulative Distribution Function, which gives the cummulative
        probability (area under the probability curve) from -infinity or 0 to
        a give x-value on the x-axis where y-axis is the probability.
        """
        return (x - self.location) / (self.scale - self.location)

    def PDF(self):
        """
        Partial Distribution Function, which gives the probability
        for particular value of x, or the area under probability
        distribution from x-h to x+h for continuous distribution.
        """
        return 1.0/(self.scale - self.location)

    def inverseCDF(self, probability, start=0.0, step=0.01):
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis.
        """
        cprob = self.CDF(start)
        if probability < cprob:
            return (start, cprob)
        while probability > cprob:
            start = start + step
            cprob = self.CDF(start)
        return (start, cprob)

    def mean(self):
        """
        Gives the arithmetic mean of the sample.
        """
        return (self.location + self.scale) / 2.0

    def median(self):
        """
        Gives the median of the sample.
        """
        return (self.location + self.scale) / 2

    def kurtosis(self):
        """
        Gives the kurtosis of the sample.
        """
        return -1.2

    def skew(self):
        """
        Gives the skew of the sample.
        """
        return 0.0

    def variance(self):
        """
        Gives the variance of the sample.
        """
        return ((self.scale - self.location) ** 2) / 12

    def quantile1(self):
        """
        Gives the 1st quantile of the sample.
        """
        return ((3 * self.location) + self.scale) / 4

    def quantile3(self):
        """
        Gives the 3rd quantile of the sample.
        """
        return (self.location + (3 * self.scale)) / 4

    def qmean(self):
        """
        Gives the quantile of the arithmetic mean of the sample.
        """
        return 0.5

    def random(self, lower, upper):
        """
        Gives a random number based on the distribution.
        """
        return random.uniform(lower, upper)
    
    
# ----------------------------------------------------------
# Untested Distributions
# ----------------------------------------------------------

def AntiLogNormalDistribution(**parameters):
    """
    Anti-Lognormal distribution is an alias of Lognormal distribution."""
    return LogNormalDistribution(**parameters)


class BernoulliDistribution(Distribution):
    """
    Bernoulli distribution is a special case of Binomial distribution where
    where number of trials = 1
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        @param success: probability of success; 0 <= success <= 1"""
        try: self.distribution = BinomialDistribution(succcess = 
                                                        parameters['success'], 
                                                        trial = 1)
        except KeyError: 
            raise DistributionParameterError('Bernoulli distribution \
            requires success parameter')
    def CDF(self, x): 
        """Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0, step = 1): 
        """It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()
#    def random(self):
#        """Gives a random number based on the distribution."""
#        return self.distribution.random()


def BilateralExponentialDistribution(**parameters):
    """
    Bilateral Exponential distribution is an alias of Laplace distribution."""
    return LaplaceDistribution(**parameters)


class BradfordDistribution(Distribution):
    def __init__(self, **parameters): 
        """
        Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameters:
        1. location
        2. scale (upper bound)
        3. shape"""
        self.location = kwargs['locatiopn']
        self.scale = kwargs['scale']
        self.shape = kwargs['shape']
        self.k = math.log10(self.shape + 1)
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        r = ((self.shape*(x - self.location)) / (self.scale - self.location))
        return math.log10(1 + r) / self.k
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution 
        from x-h to x+h for continuous distribution."""
        r = (self.shape * (x - self.location)) + self.scale - self.location
        return self.shape / (self.k * r)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        r = self.shape * (self.scale - self.location)
        r = r + (((self.shape + 1) * self.location - self.scale) * self.k)
        return r / (self.shape * self.k)
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        d = ((self.shape * (self.k - 2)) + (2 * self.k)) ** 2
        d = 3 * self.shape * d
        n = ((self.k * ((3 * self.k) - 16)) + 24)
        n = (self.shape ** 3) * (self.k - 3) * n
        n = n + ((self.k - 4) * (self.k - 3) * (12 * self.k * (self.k **2)))
        n = n + (6 * self.k * (self.k **2)) * ((3 * self.k) - 14)
        return (n + (12 * (self.k ** 3))) / d
    def skew(self): 
        """Gives the skew of the sample."""
        r = 12 * (self.shape ** 2)
        r = r - (9 * self.k * self.shape * (self.shape + 2))
        r = r + ((2 * k * k) * ((self.shape * (self.shape + 3)) + 3))
        d = self.shape * (((self.k - 2) * self.shape) + (2 * self.k))
        d = math.sqrt(d)
        d = d * ((3 * self.shape * (self.k - 2)) + (6 * self.k))
        return r / d
    def variance(self): 
        """Gives the variance of the sample."""
        r = (self.scale - self.location) ** 2
        r = r * (self.shape * (self.k - 2) +  (2 * self.k))
        return r / (2 * self.shape * self.k * self.k)
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        r = (self.location * (self.shape + 1)) - self.scale
        r = r + ((self.scale - self.location) * ((self.shape + 1)** 0.25))
        return r / self.shape
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        r = (self.location * (self.shape + 1)) - self.scale
        r = r + ((self.scale - self.location) * ((self.shape + 1)** 0.75))
        return r / self.shape
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        r = math.log10(self.shape / math.log10(self.shape + 1))
        return r / math.log10(self.shape + 1)
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.0
    def random(self, seed):
        """Gives a random number based on the distribution."""
        while 1:
            r = self.location * (self.shape + 1) - self.scale
            r = r + ((self.scale - self.location)*((self.shape + 1) ** seed))
            seed = r / self.shape
            yield seed


class BurrDistribution(Distribution):
    """
    Burr distribution is the generalization of Fisk distribution. Burr 
    distribution with D = 1 becomes Fisk distribution.
    """
    def __init__(self, **parameters): 
        """
        Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameters:
        1. location
        2. scale
        3. C (shape)
        4. D (shape)"""
        self.location = kwargs['location']
        self.scale = kwargs['scale']
        self.C = kwargs['C']
        self.D = kwargs['D']
        self.k = (NRPy.gammln(self.D) * \
                    NRPy.gammln(1 - (2/self.C)) * \
                    NRPy.gammln((2/self.C) + self.D)) - \
                ((NRPy.gammln(1 - (1/self.C)) ** 2) * \
                    (NRPy.gammln((1/self.C) + self.D) ** 2))
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return (1+(((x - self.location)/self.scale)**(-self.C)))**(-self.D)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution 
        from x-h to x+h for continuous distribution."""
        r = (1+(((x - self.location)/self.scale)**(-self.C)))**(-self.D - 1)
        r = r * ((self.C * self.D)/self.scale)
        return r * (((x - self.location)/self.scale)**(-self.C - 1))
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        r = NRPy.gammln(1 - (1/self.C)) * NRPy.gammln((1/self.C) + self.D)
        return self.location + ((r * self.scale) / NRPy.gammln(self.D))
    def mode(self): 
        """Gives the mode of the sample."""
        if ((self.C * self.D) < 1): return self.location
        else:
            r = (((self.C * self.D)-1)/(self.C + 1)) ** (1/self.C)
            return self.location + (self.scale * r)
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
    def variance(self): 
        """Gives the variance of the sample."""
        return (self.k * (self.scale ** 2)) / (NRPy.gammln(self.D) ** 2)
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        if ((self.C * self.D) < 1): return 0.0
        else:
            return (1 + ((self.C+1)/((self.C*self.D) - 1))) ** (-1*self.D)
    def random(self, seed):
        """Gives a random number based on the distribution."""
        while 1:
            r = ((1/(seed ** (1/self.D))) - 1) ** (-1/self.C)
            seed = self.location + self.scale * r
            yield seed




class ChiDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def CobbDouglasDistribution(**parameters):
    """
    Cobb-Douglas distribution is an alias of Lognormal distribution."""
    return LogNormalDistribution(**parameters)


class CosineDistribution(Distribution):
    """
    Cosine distribution is sometimes used as a simple approximation to 
    Normal distribution.
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (default = 0.0)
        2. scale (lambda; default = 1.0)"""
        try: self.location = parameters['location']
        except KeyError: self.location = 0.0
        try: self.scale = parameters['scale']
        except KeyError: self.scale = 1.0
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        n = PI + (x - self.location)/self.scale + \
            math.sin((x - self.location)/self.scale)
        return (1/PI2) * n
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (1/(PI2 * self.scale)) * \
                (1 + math.cos((x - self.location)/self.scale))
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def median(self): 
        """Gives the median of the sample."""
        return self.location
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return -0.5938
    def skew(self): 
        """Gives the skew of the sample."""
        return 0.0
    def variance(self): 
        """Gives the variance of the sample."""
        return (((PI * PI)/3) - 2) * (self.scale ** 2)
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location - (0.8317 * self.scale)
    def quantile3(self): 
        """Gives the 13rd quantile of the sample."""
        return self.location + (0.8317 * self.scale)
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.5
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.5
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def DoubleExponentialDistribution(**parameters):
    """
    Double Exponential distribution is an alias of Laplace distribution."""
    return LaplaceDistribution(**parameters)


class DoubleGammaDistribution(Distribution):
    """
    Double Gamma distribution is the signed version of Gamma distribution.
    """
    def __init__(self, **parameters): 
        """
        Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameters:
        1. location
        2. scale
        3. shape"""
        self.location = kwargs['location']
        self.scale = kwargs['scale']
        self.shape = kwargs['shape']
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        r = NRPy.gammp(self.shape ,abs((x - self.location)/self.scale))
        if x > self.location: return 0.5 + (0.5 * r)
        else: return 0.5 - (0.5 * r)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution 
        from x-h to x+h for continuous distribution."""
        r = math.exp(-1 * abs((x - self.location)/self.scale))
        r = r * (abs((x - self.location)/self.scale) ** (self.shape -1))
        return r / (2* self.scale * NRPy.gammln(self.shape))
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location
    def skew(self): 
        """Gives the skew of the sample."""
        return 0.0
    def variance(self): 
        """Gives the variance of the sample."""
        return self.shape * (self.shape + 1) * (self.scale ** 2)
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.5
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class DoubleWeibullDistribution(Distribution):
    """
    Double Weibull distribution is the signed version of Weibull distribution.
    """
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class ExponentialDistribution(Distribution):
    """
    Exponential distribution is the continuous version of Geometric 
    distribution. It is also a special case of Gamma distribution where 
    shape = 1
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (default = 0.0)
        2. scale (lambda; default = 1.0)"""
        try: self.location = parameters['location']
        except KeyError: self.location = 0.0
        try: self.scale = parameters['scale']
        except KeyError: self.scale = 1.0
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return 1 - math.exp((self.location - x)/self.scale)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (1/self.scale) * math.exp((self.location - x)/self.scale)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location + self.scale
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def median(self): 
        """Gives the median of the sample."""
        return self.location + (self.scale * math.log10(2))
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return 6.0
    def skew(self): 
        """Gives the skew of the sample."""
        return 2.0
    def variance(self): 
        """Gives the variance of the sample."""
        return self.scale * self.scale
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location + (self.scale * math.log10(1.333))
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        return self.location + (self.scale * math.log10(4))
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.6321
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.0
    def random(self):
        """Gives a random number based on the distribution."""
        return random.expovariate(1/self.location)


class ExtremeLBDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class FiskDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def FisherTippettDistribution(**parameters):
    """
    Fisher-Tippett distribution is an alias of Gumbel distribution."""
    return GumbelDistribution(**parameters)


class FoldedNormalDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def FrechetDistribution(**parameters):
    """
    Frechet distribution is an alias of Weibull distribution."""
    return WeibullDistribution(**parameters)


class GenLogisticDistribution(Distribution):
    """
    Generalized Logistic distribution is a generalization of Logistic 
    distribution. It becomes Logistic distribution when shape = 1
    """
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def GompertzDistribution(**parameters):
    """
    Gompertz distribution is an alias of Gumbel distribution."""
    return GumbelDistribution(**parameters)


class GumbelDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (eta)
        2. scale (theta)"""
        try:
            self.location = parameters['location']
            self.scale = parameters['scale']
        except KeyError: 
            raise DistributionParameterError('Gumbel distribution requires \
                location and scale.')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return math.exp(-1 * math.exp((self.location - x)/self.scale))
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (1/self.scale) * math.exp((self.location - x)/self.scale) * \
            self.CDF(x)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location + (GAMMA * self.scale)
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def median(self): 
        """Gives the median of the sample."""
        return self.location - self.scale * math.log10(math.log10(2))
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return 2.4
    def skew(self): 
        """Gives the skew of the sample."""
        return 1.1395
    def variance(self): 
        """Gives the variance of the sample."""
        return 1.667 * ((PI * self.scale) ** 2)
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location - self.scale * math.log10(math.log10(4))
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        return self.location - self.scale * math.log10(math.log10(1.333))
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.5704
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.3679
    def random(self, seed):
        """Gives a random number based on the distribution."""
        while 1:
            seed = self.location - \
                    (self.scale * math.log10(-1 * math.log10(seed)))
            yield seed


class HalfNormalDistribution(Distribution):
    """
    Half Normal distribution is a special case of Chi distribution where 
    shape (also degrees of freedom) = 1, and Folded Normal distribution
    where location = 0
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution."""
        try: self.distribution = ChiDistribution(location = 
                                                    parameters['location'],
                                                 scale = parameters['scale'],
                                                 shape = 1)
        except KeyError: 
            raise DistributionParameterError('Halfnormal distribution \
            requires location and scale parameters')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0.0, step =0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()


class HyperbolicSecantDistribution(Distribution):
    def __init__(self, **parameters): 
        """
        Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameters:
        1. location
        2. scale"""
        self.location = kwargs['location']
        self.scale = kwargs['scale']
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return (2/PI)*(1/math.tan(math.exp((x - self.location)/self.scale)))
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution 
        from x-h to x+h for continuous distribution."""
        return (1 / math.cosh((x - self.location)/self.scale)) / \
                (PI * math.scale)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return 2.0
    def skew(self): 
        """Gives the skew of the sample."""
        return 0.0
    def variance(self): 
        """Gives the variance of the sample."""
        return 0.25 * ((PI * self.scale) ** 2)
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.5
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.5
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class HypergeometricDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
            probability distribution."""
        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
#    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
#        """
#        It does the reverse of CDF() method, it takes a probability value 
#        and returns the corresponding value on the x-axis."""
#        cprob = self.CDF(start)
#        if probability < cprob: return (start, cprob)
#        while (probability > cprob):
#            start = start + step
#            cprob = self.CDF(start)
#            # print start, cprob
#        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class InverseNormalDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class LaplaceDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class LogisticDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class LogarithmicDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameters:
        1. shape"""
        try: self.shape = parameters['shape']
        except KeyError: 
            raise DistributionParameterError('Logarithmic distribution \
                requires share parameter')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        sum = 0.0
        for i in range(x): sum = sum + self.PDF(i)
        return sum
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (-1 * (self.shape ** x)) / (math.log10(1 - self.shape) * x)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return (-1 * self.shape)/((1 - self.shape) * \
                math.log10(1 - self.shape))
    def mode(self): 
        """Gives the mode of the sample."""
        return 1.0
    def variance(self): 
        """Gives the variance of the sample."""
        n = (-1 * self.shape) * (self.shape + math.log10(1 - self.shape))
        d = ((1 - self.shape) ** 2) * math.log10(1 - self.shape) * \
            math.log10(1 - self.shape)
        return n / d
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def LogLogisticDistribution(**parameters):
    """
    Log-Logistic distribution is an alias of Fisk distribution."""
    return FiskDistribution(**parameters)


class LogNormalDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#        probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#        """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 
#        to a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
    def random(self):
        """Gives a random number based on the distribution."""
        return random.lognormalvariate(self.location, self.scale)


def LogWeibullDistribution(**parameters):
    """
    Log-Weibull distribution is an alias of Gumbel distribution."""
    return GumbelDistribution(**parameters)


def LorentzDistribution(**parameters):
    """
    Lorentz distribution is an alias of Cauchy distribution."""
    return CauchyDistribution(**parameters)


class MaxwellDistribution(Distribution):
    """
    Maxwell distribution is a special case of Chi distribution where 
    location = 0 and shape (degrees of freedom) = 3
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution."""
        try: self.distribution = ChiDistribution(location = 0, 
                                                scale = parameters['scale'], 
                                                shape = 3)
        except KeyError: 
            raise DistributionParameterError('Maxwell distribution requires \
            scale parameter')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and
        the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()
#    def random(self):
#        """Gives a random number based on the distribution."""
#        return self.distribution.random()


class NakagamiDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class NegativeBinomialDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. success (probability of success; 0 <= success <= 1)
        2. target (a constant, target number of successes)"""
        try:
            self.success = parameters['success']
            self.target = parameters['target']
        except KeyError: 
            raise DistributionParameterError('Negative Binomial distribution \
            requires success and target parameters')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        sum = 0.0
        for i in range(x): sum = sum + self.PDF(i)
        return sum
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return NRPy.bico(x - 1, self.target - 1) * \
                (self.success ** self.target) * \
                ((1 - self.success) ** (x - self.target))
    def inverseCDF(self, probability, start = 0, step = 1): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.target / self.success
    def mode(self): 
        """Gives the mode of the sample."""
        return int((self.success + self.target - 1)/self.success)
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def NegativeExponentialDistribution(**parameters):
    """
    Negative-exponential distribution is an alias of Exponential distribution."""
    return ExponentialDistribution(**parameters)


class ParetoDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (also the scale; default = 1.0)
        2. scale (lambda; default = 1.0)"""
        try: self.location = parameters['location']
        except KeyError: self.location = 1.0
        try: self.shape = parameters['shape']
        except KeyError: self.shape = 1.0
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return 1 - (self.location/x) ** self.shape
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (self.shape * (self.location ** self.shape)) / \
                (x ** (self.shape + 1))
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return (self.location * self.shape) / (self.shape - 1)
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def median(self): 
        """Gives the median of the sample."""
        return self.location * (2 ** (1/self.shape))
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        n = 6 * (self.shape ** 3 + self.shape ** 2 + 6 * self.shape - 2)
        d = self.shape * (self.shape ** 2 - 7 * self.shape + 12)
        return n/d
    def skew(self): 
        """Gives the skew of the sample."""
        n = 2 * (self.shape + 1) * math.sqrt(self.shape - 2)
        d = (self.shape - 3) * math.sqrt(self.shape)
        return n/d
    def variance(self): 
        """Gives the variance of the sample."""
        n = (self.location ** 2) * self.shape
        d = (self.shape - 2) * ((self.shape - 1) ** 2)
        return n/d
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location * (1.333 ** (1/self.shape))
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        return self.location * (4 ** (1/self.shape))
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 1 - (((self.shape - 1)/self.shape) ** self.shape)
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.0
    def random(self):
        """Gives a random number based on the distribution."""
        return random.paretovariate(self.shape)   

    
class PascalDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution."""
        try: self.distribution = NegativeBinomialDistribution(
                                    parameters['success'],
                                    int(parameters['target']))
        except KeyError: 
            raise DistributionParameterError('Pascal distribution requires \
            success and target parameters')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0.0, step =0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()
#    def random(self):
#        """Gives a random number based on the distribution."""
#        return self.distribution.random()


def PolyaDistribution(**parameters):
    """
    Polya distribution is an alias of Negative-binomial distribution."""
    return NegativeBinomialDistribution(**parameters)


class PowerFunctionDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution."""
        try: self.distribution = BetaDistribution(0, 1, parameters['shape'], 
                                                    1)
        except KeyError: 
            raise DistributionParameterError('Power Function distribution \
            require shape parameter')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0.0, step =0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()
#    def random(self):
#        """Gives a random number based on the distribution."""
#        return self.distribution.random()


class RademacherDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
            probability distribution."""
        pass
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        if x < -1: 
            return 0.0
        elif x > -1 and x < 1: 
            return 0.5
        else: return 1.0
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution 
        from x-h to x+h for continuous distribution."""
        if x == -1 or x == 1: return 0.5
        else: return 0.0
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        if probability == 0.0: return (-1.0001, 0.0)
        if probability == 1.0: return (1.0, 1.0)
        else: return (0.999, 0.5)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return 0
    def skew(self): 
        """Gives the skew of the sample."""
        return 0
    def variance(self): 
        """Gives the variance of the sample."""
        return 1
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class RayleighDistribution(Distribution):
    """
    Rayleigh distribution is a special case of Chi distribution where 
    location = 0 and shape (degrees of freedom) = 2
    """
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution."""
        try: self.distribution = ChiDistribution(location = 0, 
                                                scale = parameters['scale'], 
                                                shape = 2)
        except KeyError: 
            raise DistributionParameterError('Rayleigh distribution requires \
            scale parameter')
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        return self.distribution.CDF(x)
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return self.distribution.PDF(x)
    def inverseCDF(self, probability, start = 0.0, step =0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        return self.distribution.inverseCDF(probability, start, step)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.distribution.mean()
    def mode(self): 
        """Gives the mode of the sample."""
        return self.distribution.mode()
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return self.distribution.kurtosis()
    def skew(self): 
        """Gives the skew of the sample."""
        return self.distribution.skew()
    def variance(self): 
        """Gives the variance of the sample."""
        return self.distribution.variance()
#    def random(self):
#        """Gives a random number based on the distribution."""
#        return self.distribution.random()


class ReciprocalDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def RectangularDistribution(**parameters):
    """
    Rectangular distribution is an alias of Uniform distribution."""
    return UniformDistribution(**parameters)


def SechSquaredDistribution(**parameters):
    """
    Sech-squared distribution is an alias of Logistic distribution."""
    return LogisticDistribution(**parameters)


class SemicircularDistribution(Distribution):
    def __init__(self, **parameters): 
        """Constructor method. The parameters are used to construct the 
        probability distribution.
        
        Parameter:
        1. location (default = 0.0)
        2. scale (default = 1.0)"""
        try:
            self.scale = parameters['scale']
        except KeyError: self.scale = 1.0
        try:
            self.location = parameters['location']
        except KeyError: self.location = 0.0
    def CDF(self, x): 
        """
        Cummulative Distribution Function, which gives the cummulative 
        probability (area under the probability curve) from -infinity or 0 to 
        a give x-value on the x-axis where y-axis is the probability."""
        t = ((x - self.location)/self.scale)**2
        return 0.5 + (1/PI) * (t * math.srqt(1 - (t ** 2)) + math.asin(t))
    def PDF(self, x): 
        """
        Partial Distribution Function, which gives the probability for the 
        particular value of x, or the area under probability distribution from 
        x-h to x+h for continuous distribution."""
        return (2/(self.scale * PI)) * \
                math.sqrt(1 - ((x - self.location)/self.scale)**2)
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
    def mean(self): 
        """Gives the arithmetic mean of the sample."""
        return self.location
    def mode(self): 
        """Gives the mode of the sample."""
        return self.location
    def kurtosis(self): 
        """Gives the kurtosis of the sample."""
        return -1.0
    def skew(self): 
        """Gives the skew of the sample."""
        return 0.0
    def variance(self): 
        """Gives the variance of the sample."""
        return 0.25 * (self.scale ** 2)
    def quantile1(self): 
        """Gives the 1st quantile of the sample."""
        return self.location - (0.404 * self.scale)
    def quantile3(self): 
        """Gives the 3rd quantile of the sample."""
        return self.location + (0.404 * self.scale)
    def qmean(self): 
        """Gives the quantile of the arithmetic mean of the sample."""
        return 0.5
    def qmode(self): 
        """Gives the quantile of the mode of the sample."""
        return 0.5
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


class TriangularDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value 
        and returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
#    def random(self):
#        """Gives a random number based on the distribution."""
#        raise DistributionFunctionError


def WaldDistribution(**parameters):
    """
    Wald distribution is an alias of Inverse Normal distribution."""
    return InverseNormalDistribution(**parameters)

    
class WeiBullDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#        probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#        """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the  probability curve) from -infinity or 0 
#        to a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
        """
        It does the reverse of CDF() method, it takes a probability value and 
        returns the corresponding value on the x-axis."""
        cprob = self.CDF(start)
        if probability < cprob: return (start, cprob)
        while (probability > cprob):
            start = start + step
            cprob = self.CDF(start)
            # print start, cprob
        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
    def random(self):
        """Gives a random number based on the distribution."""
        return random.weibullvariate(self.scale, self.shape)


#class DummyDistribution(Distribution):
#    def __init__(self, **parameters): 
#        """Constructor method. The parameters are used to construct the 
#            probability distribution."""
#        raise DistributionFunctionError
#    def CDF(self, x): 
#       """
#        Cummulative Distribution Function, which gives the cummulative 
#        probability (area under the probability curve) from -infinity or 0 to 
#        a give x-value on the x-axis where y-axis is the probability."""
#        raise DistributionFunctionError
#    def PDF(self, x): 
#        """
#        Partial Distribution Function, which gives the probability for the 
#        particular value of x, or the area under probability distribution 
#        from x-h to x+h for continuous distribution."""
#        raise DistributionFunctionError
#    def inverseCDF(self, probability, start = 0.0, step = 0.01): 
#        """
#        It does the reverse of CDF() method, it takes a probability value 
#        and returns the corresponding value on the x-axis."""
#        cprob = self.CDF(start)
#        if probability < cprob: return (start, cprob)
#        while (probability > cprob):
#            start = start + step
#            cprob = self.CDF(start)
#            # print start, cprob
#        return (start, cprob)
#    def mean(self): 
#        """Gives the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def mode(self): 
#        """Gives the mode of the sample."""
#        raise DistributionFunctionError
#    def kurtosis(self): 
#        """Gives the kurtosis of the sample."""
#        raise DistributionFunctionError
#    def skew(self): 
#        """Gives the skew of the sample."""
#        raise DistributionFunctionError
#    def variance(self): 
#        """Gives the variance of the sample."""
#        raise DistributionFunctionError
#    def quantile1(self): 
#        """Gives the 1st quantile of the sample."""
#        raise DistributionFunctionError
#    def quantile3(self): 
#        """Gives the 3rd quantile of the sample."""
#        raise DistributionFunctionError
#    def qmean(self): 
#        """Gives the quantile of the arithmetic mean of the sample."""
#        raise DistributionFunctionError
#    def qmode(self): 
#        """Gives the quantile of the mode of the sample."""
#        raise DistributionFunctionError
##    def random(self, seed):
##        """Gives a random number based on the distribution."""
##        while 1:
##            func
##            yield seed
