"""
Unit tests for file_manager module
"""

import unittest
import os
import sys
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.file_manager import allowed_file, save_temp, delete_temp


class TestFileManager(unittest.TestCase):
    """Test cases for file manager functionality"""
    
    def test_allowed_file_valid(self):
        """Test that valid file extensions are allowed"""
        self.assertTrue(allowed_file('test.jpg'))
        self.assertTrue(allowed_file('test.jpeg'))
        self.assertTrue(allowed_file('test.png'))
        self.assertTrue(allowed_file('TEST.PNG'))  # Case insensitive
    
    def test_allowed_file_invalid(self):
        """Test that invalid file extensions are rejected"""
        self.assertFalse(allowed_file('test.gif'))
        self.assertFalse(allowed_file('test.pdf'))
        self.assertFalse(allowed_file('test.exe'))
        self.assertFalse(allowed_file('test'))  # No extension
    
    def test_delete_temp_nonexistent(self):
        """Test deleting non-existent file"""
        result = delete_temp('nonexistent_file.jpg')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
