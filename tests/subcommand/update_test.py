# This source file is part of Yoda.
#
# Yoda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yoda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yoda. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import argparse
import unittest

from mock import call
from mock import Mock
from mock import patch
from tests.utils import Sandbox
from yoda import Config
from yoda.subcommand import Update


class TestSubcommandUpdate(unittest.TestCase):
    """Update subcommand test suite."""
    sandbox = None
    config = None
    parser = None
    subparser = None
    update = None

    def setUp(self):
        """Setup test suite."""
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand_test")

        self.update = Update()
        config_data = {
            "workspaces": {
                "yoda": {
                    "path": "/yoda",
                    "repositories": {
                        "yoda": "/project/yoda"
                    }
                }
            }
        }

        self.sandbox = Sandbox()
        self.config = Config(self.sandbox.path + "/config")
        self.config.update(config_data)
        self.update.setup("update", self.config, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        self.sandbox.destroy()
        self.parser = None
        self.update = None

    def test_parse_update(self):
        """Test parse update subcommand."""
        self.update.parse()

        args = self.parser.parse_args(["update", "ws1/repo1"])

        self.assertEqual("update", args.subcommand_test)
        self.assertEqual("ws1/repo1", args.name)

        args = self.parser.parse_args(["update", "--all"])

        self.assertEqual("update", args.subcommand_test)
        self.assertEqual(True, args.all)

        self.assertRaises(
            SystemExit,
            self.parser.parse_args, ["update", "--all", "ws1/repo1"]
        )

    def test_exec_update_workspace_only(self):
        """Test exec update subcommand."""
        args = Mock()
        args.name = "foo/bar"

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.update.print_update = Mock()

        with patch("yoda.subcommand.update.find_path",
                   return_value=mock_path) as patch_fp:
            self.update.execute(args)
            patch_fp.assert_called_once_with("foo/bar", self.update.config)
            self.update.print_update.assert_called_once_with(
                "foo/bar", "/tmp/foo/bar")

    def test_exec_update_all_workspaces(self):
        """Test exec with all workspaces."""
        args = Mock()
        args.name = None
        args.all = True

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.update.print_update = Mock()

        with patch("yoda.subcommand.update.find_path",
                   return_value=mock_path):
            self.update.execute(args)

    def test_exec_update_no_matches(self):
        """Test exec update subcommand with no matches."""
        args = Mock()
        args.name = "foobar"

        self.update.logger = Mock()
        self.update.print_update = Mock()

        with patch("yoda.subcommand.update.find_path", return_value={}):
            self.assertFalse(self.update.execute(args))
            self.update.logger.error.assert_called_once_with(
                "No matches for `foobar`")

    def test_print_update(self):
        """Test print_update."""
        self.update.logger = Mock()
        with patch("yoda.subcommand.update.Repository"):
            self.update.print_update("foo", "bar")
            self.update.logger.info.assert_has_calls(
                [call("\033[32m=> [foo] bar\033[0m")])
