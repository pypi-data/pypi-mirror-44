import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from PillowImage import PillowImage, img_adjust
from tests import *


class TestPillowImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.wtrmrk_path = wtr_path
        cls.pdf = None

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_PillowImage_draw_text(self):
        """Draw text onto an image."""
        draw = PillowImage(tempdir=self.temp.name)
        draw.draw_text('Here is the first text', y=10, opacity=50)
        draw.draw_text('Here is the second text', y=50, opacity=50)
        d = draw.save(destination=test_data_dir, file_name='draw_text')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img(self):
        """Draw text onto an image."""
        draw = PillowImage(tempdir=self.temp.name)
        draw.draw_img(self.img_path)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
        d = draw.save(destination=test_data_dir, file_name='draw_img')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img_fromimg(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
        d = draw.save(destination=test_data_dir, file_name='draw_img_fromimg')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img_fromimg_centered(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x='center', y='center')
        d = draw.save(destination=test_data_dir, file_name='draw_img_fromimg_centered')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img_fromimg_negbound(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x=-2000, y=-2000)
        d = draw.save(destination=test_data_dir, file_name='draw_img_fromimg_negbound')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img_fromimg_percentage(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30, x=.5, y=.1)
        d = draw.save(destination=test_data_dir, file_name='draw_img_fromimg_percentage')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_draw_img_fromimg_resized(self):
        """Draw text onto an image."""
        longest_side = 500
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
        draw.resize(longest_side)
        d = draw.save(destination=test_data_dir, file_name='draw_img_fromimg_resized')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert actual longest edge is equal to target longest edge
        self.assertEqual(longest_side, draw.longest_side)
        return d

    @Timer.decorator
    def test_PillowImage_rotate(self):
        """Draw text onto an image."""
        draw = PillowImage(tempdir=self.temp.name)
        draw.draw_img(self.img_path)
        draw.rotate(30)
        d = draw.save(destination=test_data_dir, file_name='rotate')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_PillowImage_size(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        size = draw.size
        d = draw.save(destination=test_data_dir, file_name='size')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertIsInstance(size, tuple)
        self.assertTrue(size == (2706, 2226))
        return d

    @Timer.decorator
    def test_PillowImage_width(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        width = draw.width
        d = draw.save(destination=test_data_dir, file_name='size')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertTrue(width == 2706)
        return d

    @Timer.decorator
    def test_PillowImage_height(self):
        """Draw text onto an image."""
        draw = PillowImage(img=self.img_path, tempdir=self.temp.name)
        height = draw.height
        d = draw.save(destination=test_data_dir, file_name='size')

        # Assert file exists
        self.assertTrue(os.path.exists(d))

        # Assert image size is correct
        self.assertTrue(height == 2226)
        return d

    @Timer.decorator
    def test_img_adjust_rotate(self):
        """Test the function 'img_rotate.'"""
        rotated = img_adjust(self.wtrmrk_path, rotate=30, fit=1)

        # Assert file exists
        self.assertTrue(os.path.exists(rotated))
        return rotated


if __name__ == '__main__':
    unittest.main()
