"""
Tests for the selector module.
"""
from datetime import date
from unittest.mock import patch, MagicMock, mock_open, call
import os
import tempfile
import unittest
import yaml

from selector import selector

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
                    "last-dl": date(2010, 1, 1)
                }
            }
        }
        mock_config_file = tempfile.mkstemp()
        with os.fdopen(mock_config_file[0], "r+") as f:
            f.write(yaml.dump(self.config))

        self.selector = selector.Selector(mock_config_file[1])

    @patch("selector.selector.urllib.request", autospec=True)
    def test_get_backlog(self, mock_urllib):
        """Test the get_backlog method.
        """

        mock_file_iterator = MagicMock()
        mock_file_iterator.__iter__.return_value = iter([
            b"foobar",
            b"foobaz",
            (b'<a href='
                b'"http://podcast.dgen.net/rinsefm/podcast/FooBarBaz131211.mp3"'
                b'></a>'),
            (b'<a href="http://podcast.dgen.net/rinsefm/podcast/'
                b'FooBarBaz090101.mp3"'
                b'download="http://podcast.dgen.net/rinsefm/podcast/'
                b'FooBarBaz090101.mp3" '
                b'target="_blank" class="bglavender"'
                b'title="Right Click and Save As to Download">&nbsp;</a>')])

        mock_urllib.urlopen.return_value = mock_file_iterator
        results = self.selector.get_backlog()

        assert len(results) == 1
        assert results["FooBar"] == \
            ["http://podcast.dgen.net/rinsefm/podcast/FooBarBaz131211.mp3"]

        mock_urllib.urlopen.assert_called_once_with(selector.RINSE_URL + \
            str(self.config["shows"]["FooBar"]["id"]))

    @patch("selector.selector.urllib.request", autospec=True)
    def test_download_shows(self, mock_urllib):
        """Test the download_shows method.
        """
        mock_config = {
            "shows": {
                "show1": {
                    "dir": "home/foo",
                },
                "show2": {},
            },
            "directory": "/foo",
        }

        backlog = {
            "show1": ["foobar.com/foo", "barqux.com/bar"],
            "show2": ["barfoo.com/foo1", "quxfoo.com/bar2"]
        }

        expected_downloads = [
            call("foobar.com/foo", "/foo/home/foo/foo"),
            call("barqux.com/bar", "/foo/home/foo/bar"),
            call("barfoo.com/foo1", "/foo/foo1"),
            call("quxfoo.com/bar2", "/foo/bar2"),
        ]

        self.selector.config = mock_config
        self.selector.download_shows(backlog)

        mock_urllib.urlretrieve.assert_has_calls(expected_downloads, True)

    @patch("selector.selector.yaml", autospec=True)
    def test_update_config(self, mock_yaml):
        """Test update_config.
        """
        mock_config = {
            "shows": {
                "show1": {
                    "last-dl": date(200, 12, 12) # Do not test before year 200!
                },
                "show2": {},
            },
            "directory": "/foo",
        }

        written_config = mock_config.copy()
        written_config["shows"]["show1"]["last_dl"] = date.today()
        written_config["shows"]["show2"]["last_dl"] = date.today()

        self.selector.config = mock_config
        mock_file = mock_open()
        mock_yaml.return_value = "foobar"

        with patch("selector.selector.open", mock_file, create=True):
            self.selector.update_config()

        mock_yaml.dump.assert_called_once_with(written_config,
            mock_file.return_value, default_flow_style=False)
        mock_file.return_value.write.assert_called_once_with("%YAML 1.2\n---\n")

    @patch("selector.selector.Selector", autospec=True)
    @patch("selector.selector.os.path.exists", autospec=True)
    def test_main(self, mock_exists, mock_selector):
        """Test the main method.
        """
        mock_backlog = list(range(0, 4))
        mock_selector.return_value.get_backlog.return_value = mock_backlog

        mock_exists.return_value = True

        selector.main()

        mock_selector.assert_called_once_with(selector.CONFIGS[0])
        mock_selector.return_value.get_backlog.assert_called_once_with()
        mock_selector.return_value.download_shows.assert_called_once_with(mock_backlog)
        mock_selector.return_value.update_config.assert_called_once_with()

class TestHelperMethods(unittest.TestCase):
    """Test the helper methods in the selector module.
    """

    def test_get_url_date(self):
        """Test the get_url_data method.
        """
        url = "http://podcast.dgen.net/rinsefm/podcast/NType310314.mp3"
        key = date(2014, 3, 31)

        assert selector.get_url_date(url) == key

