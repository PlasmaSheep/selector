"""
Tests for the selector module.
"""

from datetime import date
import mock
import os
import tempfile
import unittest
import yaml

import selector

class TestSelector(unittest.TestCase):
    """Test the methods in the Selector class.
    """
    def setUp(self):
        """Instantiate the Selector class.
        """

        self.config = {
            "directory": "/foo/bar",
            "shows": {
                "FooBar": {
                    "dir": "FooBar",
                    "id": 113,
                    "last-dl": date(2010, 01, 01)
                }
            }
        }
        mock_config_file = tempfile.mkstemp()
        with os.fdopen(mock_config_file[0], "r+") as f:
            f.write(yaml.dump(self.config))

        self.selector = selector.Selector(mock_config_file[1])

    @mock.patch("selector.urllib", autospec=True)
    def test_get_backlog(self, mock_urllib):
        """Test the get_backlog method.
        """

        mock_file_iterator = mock.MagicMock()
        mock_file_iterator.__iter__.return_value = iter([
            "foobar",
            "foobaz",
            ('<a href='
                '"http://podcast.dgen.net/rinsefm/podcast/FooBarBaz131211.mp3"'
                '></a>'),
            ('<a href="http://podcast.dgen.net/rinsefm/podcast/'
                'FooBarBaz090101.mp3"'
                'download="http://podcast.dgen.net/rinsefm/podcast/'
                'FooBarBaz090101.mp3" '
                'target="_blank" class="bglavender"'
                'title="Right Click and Save As to Download">&nbsp;</a>'
            )])
        mock_urllib.urlopen.return_value = mock_file_iterator
        results = self.selector.get_backlog()

        assert len(results) == 1
        assert results["FooBar"] == \
            ["http://podcast.dgen.net/rinsefm/podcast/FooBarBaz131211.mp3"]

        mock_urllib.urlopen.assert_called_once_with(selector.RINSE_URL + \
            str(self.config["shows"]["FooBar"]["id"]))

class TestHelperMethods(unittest.TestCase):
    """Test the helper methods in the selector module.
    """

    def test_get_url_date(self):
        """Test the get_url_data method.
        """
        url = "http://podcast.dgen.net/rinsefm/podcast/NType310314.mp3"
        key = date(2014, 03, 31)

        self.failUnless(selector.get_url_date(url) == key)

