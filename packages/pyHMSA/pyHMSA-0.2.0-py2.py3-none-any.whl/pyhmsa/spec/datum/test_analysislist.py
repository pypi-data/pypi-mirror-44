""" """

# Standard library modules.
import unittest
import logging

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.spec.datum.analysislist import \
    AnalysisList0D, AnalysisList1D, AnalysisList2D
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class TestAnalysisList0D(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.datum = AnalysisList0D(3)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0] = 5.0

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(3, len(self.datum))
        self.assertEqual(3, self.datum.analysis_count)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(5.0, self.datum[0, 0], 4)

        self.assertEqual(3, self.datum.collection_dimensions['Analysis'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0)
        self.assertAlmostEqual(5.0, analysis, 4)
        self.assertEqual(1, len(analysis.conditions))

    def testxlabel(self):
        self.assertEqual('Analysis', self.datum.get_xlabel())

        self.datum.set_xlabel("Test", 'cps/nA')
        self.assertEqual('Test (cps/nA)', self.datum.get_xlabel())

    def testylabel(self):
        self.assertEqual('Values', self.datum.get_ylabel())

        self.datum.set_ylabel("Test", 'cps/nA')
        self.assertEqual('Test (cps/nA)', self.datum.get_ylabel())

class TestAnalysisList1D(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.datum = AnalysisList1D(3, 5)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0] = [1.0, 2.0, 3.0, 4.0, 5.0]

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(3, len(self.datum))
        self.assertEqual(3, self.datum.analysis_count)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertAlmostEqual(1.0, self.datum[0, 0], 4)
        self.assertAlmostEqual(5.0, self.datum[0, -1], 4)

        self.assertEqual(3, self.datum.collection_dimensions['Analysis'])
        self.assertEqual(5, self.datum.datum_dimensions['Channel'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0)
        self.assertAlmostEqual(1.0, analysis[0], 4)
        self.assertAlmostEqual(5.0, analysis[-1], 4)
        self.assertEqual(5, analysis.channels)
        self.assertEqual(1, len(analysis.conditions))

class TestAnalysisList2D(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.datum = AnalysisList2D(3, 5, 5)
        self.datum.conditions['Test'] = _Condition()
        self.datum[0] = np.ones((5, 5))

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual(3, len(self.datum))
        self.assertEqual(3, self.datum.analysis_count)
        self.assertEqual(1, len(self.datum.conditions))
        self.assertEqual(5, self.datum.u)
        self.assertEqual(5, self.datum.v)
        self.assertAlmostEqual(1.0, self.datum[0, 0, 0], 4)

        self.assertEqual(3, self.datum.collection_dimensions['Analysis'])
        self.assertEqual(5, self.datum.datum_dimensions['U'])
        self.assertEqual(5, self.datum.datum_dimensions['V'])

    def testtoanalysis(self):
        analysis = self.datum.toanalysis(0)
        self.assertAlmostEqual(1.0, analysis[0, 0], 4)
        self.assertEqual(5, analysis.u)
        self.assertEqual(5, analysis.v)
        self.assertEqual(1, len(analysis.conditions))

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
