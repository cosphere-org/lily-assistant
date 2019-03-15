
import os
from unittest import TestCase
from unittest.mock import call
import textwrap

from click.testing import CliRunner
import pytest

from lily_assistant.cli.cli import cli
from lily_assistant.cli.copier import Copier
from lily_assistant.checkers.structure import StructureChecker
from lily_assistant.checkers.repo import GitRepo
from lily_assistant.checkers.commit_message import CommitMessageChecker
from lily_assistant import __version__


class CliTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

    def setUp(self):
        self.runner = CliRunner()

    #
    # INIT
    #
    def test_init(self):

        copy = self.mocker.patch.object(Copier, 'copy')

        result = self.runner.invoke(cli, ['init', 'src_dir'])
        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            Please insert the following line at the top of your Makefile:

            include .lily/lily_assistant.makefile
        ''').strip()
        assert copy.call_args_list == [call('src_dir')]

    #
    # HAS_CORRECT_STRUCTURE
    #
    def test_has_correct_structure__valid(self):

        self.mocker.patch.object(
            StructureChecker, 'is_valid').return_value = True
        raise_errors = self.mocker.patch.object(
            StructureChecker, 'raise_errors')

        result = self.runner.invoke(cli, ['has_correct_structure'])

        assert result.exit_code == 0
        assert result.output == ''
        assert raise_errors.call_count == 0

    def test_has_correct_structure__invalid(self):

        self.mocker.patch.object(
            StructureChecker, 'is_valid').return_value = False
        raise_errors = self.mocker.patch.object(
            StructureChecker, 'raise_errors')

        result = self.runner.invoke(cli, ['has_correct_structure'])

        assert result.exit_code == 0
        assert result.output == ''
        assert raise_errors.call_args_list == [call()]

    #
    # IS_NOT_MASTER
    #
    def test_is_not_master__true(self):

        self.mocker.patch.object(GitRepo, 'active_branch', 'development')

        result = self.runner.invoke(cli, ['is_not_master'])

        assert result.exit_code == 0
        assert result.output == ''

    def test_is_not_master__false(self):

        self.mocker.patch.object(GitRepo, 'active_branch', 'master')

        result = self.runner.invoke(cli, ['is_not_master'])

        assert result.exit_code == -1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            you shouldn't perform this action on the master branch
        ''').strip()

    #
    # IS_COMMIT_MESSAGE_VALID
    #
    def test_is_commit_message_valid__valid(self):

        self.mocker.patch.object(
            CommitMessageChecker, 'is_valid').return_value = True
        commit_msg = self.tmpdir.join('message.txt')
        commit_msg.write('hello world')

        result = self.runner.invoke(
            cli, ['is_commit_message_valid', str(commit_msg)])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            [INFO]

            COMMIT MESSAGE: hello world
        ''').strip()

    def test_is_commit_message_valid__invalid(self):

        self.mocker.patch.object(
            CommitMessageChecker, 'is_valid').return_value = False
        commit_msg = self.tmpdir.join('message.txt')
        commit_msg.write('hello world')

        result = self.runner.invoke(
            cli, ['is_commit_message_valid', str(commit_msg)])

        assert result.exit_code == -1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            your commit message is not following the commit message convention.
        ''').strip()

    #
    # IS_VIRTUALENV
    #
    def test_is_virtualenv__false(self):

        os.environ['VIRTUAL_ENV'] = ''

        result = self.runner.invoke(cli, ['is_virtualenv'])

        assert result.exit_code == -1
        assert result.output.strip() == textwrap.dedent('''
            [ERROR]

            You must run your tests & code against VIRTUAL ENVIRONMENT
        ''').strip()

    def test_is_virtualenv__true(self):

        os.environ['VIRTUAL_ENV'] = 'something'

        result = self.runner.invoke(cli, ['is_virtualenv'])

        assert result.exit_code == 0
        assert result.output.strip() == ''

    #
    # VERSION
    #
    def test_version(self):
        result = self.runner.invoke(cli, ['version'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent(f'''
            [INFO]

            Lily-Assistant Version: {__version__}
        ''').strip()
