"""
Unit tests for WhatsApp Tag All Tool
"""

import unittest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestTagAllStructure(unittest.TestCase):
    """Test the basic structure of the tagall module."""
    
    def test_file_exists(self):
        """Test that tagall.py file exists."""
        self.assertTrue(os.path.exists('tagall.py'))
    
    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        self.assertTrue(os.path.exists('requirements.txt'))
        
    def test_requirements_content(self):
        """Test that requirements.txt has necessary dependencies."""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            self.assertIn('selenium', content)
            self.assertIn('webdriver-manager', content)
    
    def test_readme_exists(self):
        """Test that README.md exists and has content."""
        self.assertTrue(os.path.exists('README.md'))
        with open('README.md', 'r') as f:
            content = f.read()
            self.assertIn('WhatsApp', content)
            self.assertIn('@all', content)
    
    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        self.assertTrue(os.path.exists('.gitignore'))
        with open('.gitignore', 'r') as f:
            content = f.read()
            self.assertIn('User_Data', content)
    
    def test_batch_files_exist(self):
        """Test that Windows batch files exist."""
        self.assertTrue(os.path.exists('setup.bat'))
        self.assertTrue(os.path.exists('run.bat'))


if __name__ == '__main__':
    unittest.main()
