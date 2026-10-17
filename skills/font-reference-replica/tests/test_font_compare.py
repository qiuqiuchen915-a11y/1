"""Synthetic stroke fixtures require no font files or network."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
from PIL import Image, ImageDraw

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/font_compare.py'
spec = importlib.util.spec_from_file_location('font_compare', SCRIPT)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def glyph(transparent=False, different=False, background='white', ink='black'):
    im = Image.new('RGBA', (48, 48), (123, 45, 67, 0) if transparent else background)
    d = ImageDraw.Draw(im)
    d.rectangle((10, 8, 15, 39), fill=ink)
    d.rectangle((10, 8 if not different else 33, 36, 14 if not different else 39), fill=ink)
    return im


class FontCompareTests(unittest.TestCase):
    def test_same_and_different_for_both_backgrounds(self):
        for transparent in (False, True):
            with self.subTest(transparent=transparent):
                a, source = fc.glyph_mask(glyph(transparent))
                b, _ = fc.glyph_mask(glyph(transparent, True))
                self.assertEqual(source, 'alpha' if transparent else 'border-rgb')
                self.assertAlmostEqual(fc.mask_iou(a, a), 1.0)
                self.assertLess(fc.mask_iou(a, b), 0.5)
                self.assertLess(a.sum(), a.size)

    def test_rgb_image_and_light_ink_on_dark_background(self):
        a, _ = fc.glyph_mask(glyph().convert('RGB').convert('RGBA'))
        b, _ = fc.glyph_mask(glyph(background='black', ink='white'))
        np.testing.assert_array_equal(a, b)

    def test_transparent_and_opaque_have_same_geometry(self):
        a, _ = fc.glyph_mask(glyph(True))
        b, _ = fc.glyph_mask(glyph())
        np.testing.assert_array_equal(a, b)

    def test_hidden_rgb_is_ignored(self):
        a = glyph(True)
        b = np.asarray(a).copy()
        b[b[..., 3] == 0, :3] = (0, 255, 0)
        np.testing.assert_array_equal(fc.arr_rgb(a), fc.arr_rgb(Image.fromarray(b)))

    def test_uniform_partial_alpha_is_not_a_full_mask(self):
        im = glyph()
        im.putalpha(200)
        mask, source = fc.glyph_mask(im)
        self.assertEqual(source, 'border-rgb')
        self.assertLess(mask.sum(), mask.size)

    def test_complex_border_rejected_and_explicit_mask_supported(self):
        im = glyph()
        ImageDraw.Draw(im).rectangle((0, 0, 20, 2), fill='red')
        with self.assertRaisesRegex(ValueError, 'Non-uniform border'):
            fc.glyph_mask(im)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'mask.png'
            expected, _ = fc.glyph_mask(glyph())
            Image.fromarray(expected.astype('uint8') * 255).save(path)
            actual, source = fc.glyph_mask(im, path)
            self.assertEqual(source, 'explicit')
            np.testing.assert_array_equal(actual, expected)
            Image.new('L', (2, 2)).save(path)
            with self.assertRaisesRegex(ValueError, 'Mask size mismatch'):
                fc.glyph_mask(im, path)

    def run_cli(self, a, b, *extra):
        with tempfile.TemporaryDirectory() as td:
            r, c, diff = [Path(td) / x for x in ('r.png', 'c.png', 'diff.png')]
            a.save(r)
            b.save(c)
            result = subprocess.run([sys.executable, str(SCRIPT), str(r), str(c),
                                     '--diff', str(diff), *extra], capture_output=True, text=True)
            pixels = np.asarray(Image.open(diff)).copy() if diff.exists() else None
            return result, pixels

    def test_cli_different_opaque_shapes_and_visible_diff(self):
        result, diff = self.run_cli(glyph(), glyph(different=True))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Glyph mask IoU:', result.stdout)
        self.assertNotIn('Alpha IoU:', result.stdout)
        self.assertIn('border-rgb / border-rgb', result.stdout)
        self.assertEqual(diff.shape[2], 3)
        self.assertGreater(diff.max(), 0)

    def test_size_mismatch_rejected_without_diff(self):
        result, diff = self.run_cli(glyph(), Image.new('RGB', (20, 20)))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Size mismatch', result.stderr)
        self.assertIsNone(diff)

    def test_empty_masks_are_not_reported_as_perfect(self):
        result, _ = self.run_cli(Image.new('RGB', (48, 48), 'white'),
                                 Image.new('RGB', (48, 48), 'white'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Glyph mask IoU: N/A (empty masks)', result.stdout)

    def test_invalid_tolerance(self):
        result, _ = self.run_cli(glyph(), glyph(), '--background-tolerance', '255')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be between', result.stderr)

    def test_ssim_optional_dependency_missing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'a.png'
            glyph().save(p)
            with mock.patch.object(sys, 'argv', [str(SCRIPT), str(p), str(p),
                                                '--diff', str(Path(td) / 'd.png')]), \
                 mock.patch.dict(sys.modules, {'skimage.metrics': None}), \
                 mock.patch('builtins.print') as output:
                fc.main()
            self.assertIn(mock.call('SSIM:', 'N/A'), output.call_args_list)

    def test_small_images_ssim_is_explicitly_unavailable(self):
        result, _ = self.run_cli(Image.new('RGB', (3, 3), 'white'),
                                 Image.new('RGB', (3, 3), 'white'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SSIM:', result.stdout)
        try:
            import skimage.metrics
        except ImportError:
            pass
        else:
            self.assertIn('SSIM unavailable:', result.stdout)
            self.assertIn('SSIM: N/A', result.stdout)

    def test_ssim_numerical_when_installed(self):
        try:
            import skimage.metrics
        except ImportError:
            self.skipTest('optional scikit-image is not installed')
        same, _ = self.run_cli(glyph(), glyph())
        different, _ = self.run_cli(glyph(), glyph(different=True))
        self.assertEqual(same.returncode, 0, same.stderr)
        self.assertEqual(different.returncode, 0, different.stderr)
        self.assertIn('SSIM: 1.000000', same.stdout)
        score = float(next(line.split(':')[1] for line in different.stdout.splitlines()
                           if line.startswith('SSIM:')))
        self.assertLess(score, 0.9)


if __name__ == '__main__':
    unittest.main()
