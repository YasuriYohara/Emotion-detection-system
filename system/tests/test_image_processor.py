"""
Unit tests for image_processor module
"""

import unittest
import os
import sys
import numpy as np
import cv2

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Test cases for image processor functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = ImageProcessor()
        # Create a simple test image
        self.test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        self.test_image.fill(128)  # Gray image
    
    def test_validate_image_valid(self):
        """Test validation of valid image"""
        result = self.processor.validate_image(self.test_image)
        self.assertTrue(result)
    
    def test_validate_image_too_small(self):
        """Test validation rejects too small images"""
        small_image = np.zeros((30, 30, 3), dtype=np.uint8)
        result = self.processor.validate_image(small_image)
        self.assertFalse(result)
    
    def test_validate_image_too_dark(self):
        """Test validation rejects too dark images"""
        dark_image = np.zeros((480, 640, 3), dtype=np.uint8)
        dark_image.fill(10)  # Very dark
        result = self.processor.validate_image(dark_image)
        self.assertFalse(result)
    
    def test_validate_image_none(self):
        """Test validation rejects None input"""
        result = self.processor.validate_image(None)
        self.assertFalse(result)
    
    def test_preprocess_face(self):
        """Test face preprocessing"""
        face_box = (100, 100, 200, 200)
        processed = self.processor.preprocess_face(self.test_image, face_box)
        
        # Check output is 48x48 (default target size)
        self.assertEqual(processed.shape, (48, 48))


if __name__ == '__main__':
    unittest.main()
