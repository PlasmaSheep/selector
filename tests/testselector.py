"""
Test everything in selector.py
"""

from datetime import date
import unittest

import selector

class TestSelector(unittest.TestCase):
    """Test the methods in the selector module.
    """
    def setUp(self):
        """Instantiate the Selector class.
        """
        self.selector = selector.Selector()

    def test_get_url_date(self):
        """Test the get_url_data method.
        """
        url = "http://podcast.dgen.net/rinsefm/podcast/NType310314.mp3"
        key = date(2014, 03, 31)

        self.failUnless(selector.get_url_date(url) == key)
