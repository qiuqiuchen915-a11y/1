"""A filled intentional cut and a severed bridge can cancel in component counts."""
import unittest
import numpy as np
from PIL import Image
import test_font_compare as fixtures

fc = fixtures.fc


class BrokenConnectedTests(unittest.TestCase):
    @staticmethod
    def masks():
        a = np.zeros((48, 48), dtype=bool)
        a[8:20, 8:14] = True
        a[8:20, 17:23] = True  # intentional cut between these fragments
        a[28:40, 8:14] = True
        a[28:40, 17:23] = True
        a[33, 14:17] = True  # intended lower bridge
        b = a.copy()
        b[13, 14:17] = True  # wrong: fill the upper cut
        b[33, 14:17] = False  # wrong: remove the lower bridge
        return a, b

    @staticmethod
    def picture(mask, transparent=False):
        a = np.zeros((*mask.shape, 4), dtype=np.uint8)
        a[..., :3] = mask[..., None] * 255
        a[..., 3] = mask * 255 if transparent else 255
        return Image.fromarray(a)

    def run_case(self, a, b, transparent=False):
        result, _ = fixtures.FontCompareTests().run_cli(
            self.picture(a, transparent), self.picture(b, transparent),
            '--roi', '12', '11', '19', '16',
            '--roi', '12', '31', '19', '36')
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_same_component_count_does_not_hide_swapped_junctions(self):
        a, b = self.masks()
        self.assertEqual(fc.component_count(a), fc.component_count(b))
        for transparent in (False, True):
            with self.subTest(transparent=transparent):
                out = self.run_case(a, b, transparent)
                self.assertIn('missing foreground=0; added foreground=3', out)
                self.assertIn('missing foreground=3; added foreground=0', out)
                self.assertIn('components(8)=2/1', out)
                self.assertIn('components(8)=1/2', out)
                self.assertEqual(out.count('Background IoU=0.800000'), 2)

    def test_identical_mixed_design_preserves_cuts_and_bridges(self):
        a, _ = self.masks()
        out = self.run_case(a, a)
        self.assertEqual(out.count('Background IoU=1.000000'), 2)
        self.assertEqual(out.count('missing foreground=0; added foreground=0'), 2)
        self.assertNotIn('Warning: ROI connectivity', out)

    def test_widened_cut_detected_without_component_count_change(self):
        a, _ = self.masks()
        b = a.copy()
        b[11:16, 13] = False
        self.assertEqual(fc.component_count(a), fc.component_count(b))
        out = self.run_case(a, b)
        self.assertIn('missing foreground=5; added foreground=0', out)
        self.assertIn('Background IoU=0.750000', out)

    def test_no_negative_space_is_unavailable_not_perfect(self):
        a = np.ones((48, 48), dtype=bool)
        # Image has opaque white foreground, defined with an explicit mask.
        # Use alpha background outside the ROI to make foreground unambiguous.
        a[0, :] = False
        out = self.run_case(a, a, True)
        self.assertEqual(out.count('Background IoU=N/A (no background)'), 2)


if __name__ == '__main__':
    unittest.main()
