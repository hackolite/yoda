import unittest
import argparse

from mock import Mock
from .utils import mock_config
from yoda.subcmd_workspace import workspace


class TestSubcommandsWorkspace(unittest.TestCase):
    """ Workspace subcommand test suite """
    parser = None
    workspace = None

    def setUp(self):
        """ Setup test suite """
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        subparser = self.parser.add_subparsers(dest="subcommand_test")

        config_data = "{workspaces: {}}"
        self.workspace = workspace()
        self.workspace.setup(mock_config(config_data), subparser)

    def tearDown(self):
        """ Tear down test suite """
        self.parser = None
        self.workspace = None

    def test_parse_add(self):
        """ Test workspace add parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "add", "foo", "/tmp/foo"])

        self.assertEqual("add", args.workspace_subcommand)
        self.assertEqual("foo", args.name)
        self.assertEqual("/tmp/foo", args.path)

    def test_parse_remove(self):
        """ Test workspace remove parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "remove", "foo"])

        self.assertEqual("remove", args.workspace_subcommand)
        self.assertEqual("foo", args.name)

    def test_parse_list(self):
        """ Test workspace list parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "list"])
        self.assertEqual("list", args.workspace_subcommand)

    def test_exec_add(self):
        """ Test workspace add execution """
        ws = Mock()
        ws.add = Mock()

        args = Mock()
        args.workspace_subcommand = "add"
        args.name = "foo"
        args.path = "/foo"

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.add.assert_called_with("foo", "/foo")

    def test_exec_remove(self):
        """ Test workspace remove execution """
        ws = Mock()
        ws.remove = Mock()

        args = Mock()
        args.workspace_subcommand = "remove"
        args.name = "foo"

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.remove.assert_called_with("foo")

    def test_exec_list(self):
        """ Test workspace list execution """
        ws = Mock()
        ws.list = Mock(return_value={})

        args = Mock()
        args.workspace_subcommand = "list"

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.list.assert_called_with()