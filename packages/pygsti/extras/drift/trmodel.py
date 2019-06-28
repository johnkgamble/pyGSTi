from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""Functions for Fourier analysis of equally spaced time-series data"""

from . import signal as _sig
from . import probtrajectory as _ptraj

import numpy as _np
import time as _tm
import copy as _copy

from scipy.optimize import minimize as _minimize


class TimeResolvedModel(object):
    """
    Encapsulates a basic form of time-resolved model, for implementing simple types
    of time-resolved characterization, e.g., time-resolved Ramsey spectroscopy.
    """

    def __init__(self, hyperparameters, parameters):
        """
        Initializes a TimResolvedModel object.

        Parameters
        ----------
        hyperparameters: list
            A set of meta-parameters, that define the model. For example, these could
            be frequencies to include in a Fourier decomposition.

        parameters: list
           The values for the parameters of the model. For example, these could be
           the amplitudes for each frequency in a Fourier decomposition.

        Returns
        -------
        TimeResolvedModel

        """
        self.hyperparameters = hyperparameters
        self.parameters = parameters

        return None

    def set_hyperparameters(self, hyperparameters):
        self.hyperparameters = _copy.deepcopy(hyperparameters)

    def set_parameters(self, parameters):
        self.parameters = _copy.deepcopy(parameters)

    def get_parameters(self):
        return _copy.deepcopy(self.parameters)

    def get_probabilities(self, circuit, times):
        """
        todo
        """
        raise NotImplementedError("Derived classes need to implement this!")

    def copy(self):
        return _copy.deepcopy(self)


def negloglikelihood(trmodel, ds, minp=0, maxp=1):
    """
    The negative loglikelihood for a TimeResolvedModel given the data.

    Parameters
    ----------
    timeresolvedmodel: TimeResolvedModel
        The TimeResolvedModel to calculate the likelihood of.

    ds: DataSet
        A DataSet, containing time-series data.

    minp, maxp: float, optional
        Value used to smooth the 0 and 1 probability boundaries for
        the likelihood function. Useful in optimization routines.

    Returns
    -------
    float
        The negative loglikelihood of the model.

    """
    negll = 0.
    for circuit in ds.keys():
        times, clickstreams = ds[circuit].get_timeseries_for_outcomes()
        probs = trmodel.get_probabilities(circuit, times)
        negll += _ptraj.probsdict_negloglikelihood(probs, clickstreams, minp, maxp)

    return negll


def maxlikelihood(trmodel, ds, minp=1e-4, maxp=1 - 1e-6, bounds=None, optout=False,
                  optoptions={}, verbosity=1):
    """
    Finds the maximum likelihood TimeResolvedModel given the data.

    Parameters
    ----------
    timeresolvedmodel: TimeResolvedModel
        The TimeResolvedModel that is used as the seed, and which defines
        the class of parameterized models to optimize over.

    ds: DataSet
        A DataSet, containing time-series data.

    minp, maxp: float, optional
        Value used to smooth the 0 and 1 probability boundaries for
        the likelihood function.

    bounds: list or None, optional
        Bounds on the parameters, as specified in scipy.optimize.minimize

    optout: bool, optional
        Wether to return the output of scipy.optimize.minimize

    optoptions: dict, optional
        Optional arguments for scipy.optimize.minimize.

    Returns
    -------
    float
        The maximum loglikelihood model

    """
    maxlmodel = trmodel.copy()

    def objfunc(parameters):
        maxlmodel.set_parameters(parameters)
        return negloglikelihood(maxlmodel, ds, minp, maxp)

    if verbosity > 0:
        print("- Performing MLE over {} parameters...".format(len(maxlmodel.get_parameters())), end='')
    if verbosity > 1:
        print("")

    seed = maxlmodel.get_parameters()
    start = _tm.time()
    optout = _minimize(objfunc, seed, options=optoptions, bounds=bounds)
    maxlparameters = optout.x
    maxlmodel.set_parameters(maxlparameters)
    end = _tm.time()

    if verbosity == 1:
        print("complete.")
    if verbosity > 0:
        print("- Time taken: {} seconds".format(end - start)),

    if optout:
        return maxlmodel, optout
    else:
        return maxlmodel