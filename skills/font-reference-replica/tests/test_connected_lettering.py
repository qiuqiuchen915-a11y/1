"""Local junction QA: global overlap can hide one missing connector pixel."""
import unittest
import numpy as np
import test_font_compare as fixtures

fc = fixtures.fc
glyph = fixtures.glyph


class ConnectedLetteringTests(unittest.TestCase):
    @staticmethod
    def pair():
        a = np.zeros((64, 64), dtype=bool)
        a[8:56, 8:30] = True
        a[8:56, 33:55] = True
        a[30, 30:33] = True
        b = a.copy()
        b[30, 31] = False
        return a, b

    def test_missing_thin_bridge_despite_high_global_iou(self):
        a, b = self.pair()
        self.assertGreater(fc.mask_iou(a, b), 0.985)
        iou, edges, rc, cc = fc.region_metrics(a, b, (28, 28, 35, 33))
        self.assertLess(iou, 1)
        self.assertLess(edges, 1)
        self.assertEqual((rc, cc), (1, 2))

    def test_added_bridge_is_also_detected(self):
        a, b = self.pair()
        self.assertEqual(fc.region_metrics(b, a, (28, 28, 35, 33))[2:], (2, 1))

    def test_matching_connection(self):
        a, _ = self.pair()
        metrics = fc.region_metrics(a, a, (28, 28, 35, 33))
        self.assertAlmostEqual(metrics[0], 1)
        self.assertAlmostEqual(metrics[1], 1)
        self.assertEqual(metrics[2:], (1, 1))

    def test_diagonal_and_empty_connectivity(self):
        self.assertEqual(fc.component_count(np.eye(3, dtype=bool)), 1)
        z = np.zeros((3, 3), dtype=bool)
        self.assertEqual(fc.region_metrics(z, z, (0, 0, 3, 3)), (None, 0.0, 0, 0))

    def test_invalid_regions(self):
        a, b = self.pair()
        for box in ((-1, 0, 2, 2), (0, 0, 65, 2), (2, 0, 2, 2), (2, 2, 1, 1)):
            with self.subTest(box=box), self.assertRaises(ValueError):
                fc.region_metrics(a, b, box)
        with self.assertRaises(ValueError):
            fc.region_metrics(a, b[:-1], (0, 0, 2, 2))

    def test_cli_repeated_roi_and_invalid_roi(self):
        run_cli = fixtures.FontCompareTests().run_cli
        result, _ = run_cli(glyph(), glyph(), '--roi', '8', '8', '20', '40',
                            '--roi', '20', '8', '40', '40')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('components(8)'), 2)
        result, diff = run_cli(glyph(), glyph(), '--roi', '0', '0', '100', '100')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ROI must be', result.stderr)
        self.assertIsNone(diff)


if __name__ == '__main__':
    unittest.main()
