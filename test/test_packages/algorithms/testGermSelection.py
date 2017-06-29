from pygsti.construction import std1Q_XYI as std
import pygsti

import numpy as np
import sys, os

from .algorithmsTestCase import AlgorithmTestCase

class GermSelectionTestCase(AlgorithmTestCase):

    def test_germsel_tests(self):
        germsToTest = pygsti.construction.list_all_gatestrings_without_powers_and_cycles(
            list(std.gs_target.gates.keys()), 2)

        bSuccess, eigvals_finiteL = pygsti.alg.test_germ_list_finitel(
            self.gs_target_noisy, germsToTest, L=16, returnSpectrum=True, tol=1e-3)
        self.assertFalse(bSuccess)

        bSuccess,eigvals_infiniteL = pygsti.alg.test_germ_list_infl(
            self.gs_target_noisy, germsToTest, returnSpectrum=True, check=True)
        self.assertFalse(bSuccess)


    def test_germsel_slack(self):
      
        germsToTest = pygsti.construction.list_all_gatestrings_without_powers_and_cycles(
            list(std.gs_target.gates.keys()), 3)

        germsToTest2 = pygsti.construction.list_all_gatestrings_without_powers_and_cycles(
            list(std.gs_target.gates.keys()), 4) + std.germs

        finalGerms = pygsti.alg.optimize_integer_germs_slack(
            self.gs_target_noisy, germsToTest, initialWeights=None,
            fixedSlack=0.1, slackFrac=False, returnAll=False, tol=1e-6, verbosity=4)

        finalGerms, wts, scoreDict = pygsti.alg.optimize_integer_germs_slack(
            self.gs_target_noisy, germsToTest2, initialWeights=np.ones( len(germsToTest2), 'd' ),
            fixedSlack=False, slackFrac=0.1, returnAll=True, tol=1e-6, verbosity=4)

        self.runSilent(pygsti.alg.optimize_integer_germs_slack,
                       self.gs_target_noisy, germsToTest,
                       initialWeights=np.ones( len(germsToTest), 'd' ),
                       fixedSlack=False, slackFrac=0.1,
                       returnAll=True, tol=1e-6, verbosity=4, maxIter=1)
                       # test hitting max iterations

        with self.assertRaises(ValueError):
            pygsti.alg.optimize_integer_germs_slack(
                self.gs_target_noisy, germsToTest,
                initialWeights=np.ones( len(germsToTest), 'd' ),
                returnAll=True, tol=1e-6, verbosity=4)
                # must specify either fixedSlack or slackFrac


    def test_germsel_grasp(self):
        threshold             = 1e6
        randomizationStrength = 1e-3
        neighborhoodSize      = 5
        gatesetNeighborhood   = pygsti.alg.randomizeGatesetList([std.gs_target],
                                  randomizationStrength=randomizationStrength,
                                  numCopies=neighborhoodSize, seed=2014)

        max_length   = 6
        gates        = std.gs_target.gates.keys()
        superGermSet = pygsti.construction.list_all_gatestrings_without_powers_and_cycles(gates, max_length)
        pygsti.alg.grasp_germ_set_optimization(gatesetList=gatesetNeighborhood, germsList=superGermSet,
                                            alpha=0.1, randomize=False, seed=2014, scoreFunc='all',
                                            threshold=threshold, verbosity=1, iterations=1,
                                            l1Penalty=1.0, returnAll=True)



    def test_germsel_greedy(self):
        threshold             = 1e6
        randomizationStrength = 1e-3
        neighborhoodSize      = 5
        gatesetNeighborhood   = pygsti.alg.randomizeGatesetList([std.gs_target],
                                  randomizationStrength=randomizationStrength,
                                  numCopies=neighborhoodSize, seed=2014)

        max_length   = 6
        gates        = std.gs_target.gates.keys()
        superGermSet = pygsti.construction.list_all_gatestrings_without_powers_and_cycles(gates, max_length)

        #Depth first
        pygsti.alg.build_up(gatesetNeighborhood, superGermSet,
                                    randomize=False, seed=2014, scoreFunc='all',
                                    threshold=threshold, verbosity=1, gatePenalty=1.0)

        #Breadth first
        pygsti.alg.build_up_breadth(gatesetNeighborhood, superGermSet,
                                    randomize=False, seed=2014, scoreFunc='all',
                                    threshold=threshold, verbosity=1, gatePenalty=1.0)
          # with small memory limit
        with self.assertRaises(MemoryError):
            pygsti.alg.build_up_breadth(gatesetNeighborhood, superGermSet,
                                        randomize=False, seed=2014, scoreFunc='all',
                                        threshold=threshold, verbosity=1, gatePenalty=1.0,
                                        memLimit=1024)

        pygsti.alg.build_up_breadth(gatesetNeighborhood, superGermSet,
                                    randomize=False, seed=2014, scoreFunc='all',
                                    threshold=threshold, verbosity=1, gatePenalty=1.0,
                                    memLimit=1024000)


    def test_germsel_driver(self):
        #GREEDY
        options = {'threshold': 1e6 }
        germs = pygsti.alg.generate_germs(std.gs_target, randomize=True, randomizationStrength=1e-3,
                               numGSCopies=5, seed=2017, maxGermLength=6,
                               force="singletons", algorithm='greedy',
	                       algorithm_kwargs=options, memLimit=None, comm=None,
		               profiler=None, verbosity=1)

        #GRASP
        options = dict(l1Penalty=1e-2,
                       gatePenalty=1.0,
                       scoreFunc='all',
                       tol=1e-6, threshold=1e6,
                       iterations=2)
        germs = pygsti.alg.generate_germs(std.gs_target, randomize=True, randomizationStrength=1e-3,
                               numGSCopies=5, seed=2017, maxGermLength=6,
                               force="singletons", algorithm='grasp',
	                       algorithm_kwargs=options, memLimit=None, comm=None,
		               profiler=None, verbosity=1)

        #SLACK
        options = dict(fixedSlack=False, slackFrac=0.1)
        germs = pygsti.alg.generate_germs(std.gs_target, randomize=True, randomizationStrength=1e-3,
                               numGSCopies=5, seed=2017, maxGermLength=6,
                               force="singletons", algorithm='slack',
	                       algorithm_kwargs=options, memLimit=None, comm=None,
		               profiler=None, verbosity=1)
