
from unittest import TestCase
import json
import os

import pytest

from lily_assistant.config import Config


class ConfigTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker, tmpdir):
        self.mocker = mocker

        self.tmpdir = tmpdir

    def setUp(self):

        self.lily_dir = self.tmpdir.mkdir('.lily')
        self.mocker.patch.object(
            os, 'getcwd').return_value = str(self.tmpdir)

        self.lily_dir.join('config.json').write(json.dumps({
            'name': 'hello',
            'src_dir': 'some_service',
            'repository': 'bithub',
            'version': '0.1.9',
            'last_commit_hash': '940594',
            'next_version': '0.2.1',
            'next_last_commit_hash': 'fd898fd',
        }))

    #
    # GET_PROJECT_PATH
    #
    def test_get_project_path(self):

        assert Config.get_project_path() == str(self.tmpdir)

    #
    # GET_CONFIG_PATH
    #
    def test_get_config_path(self):

        assert Config.get_config_path() == str(
            self.tmpdir.join('.lily').join('config.json'))

    #
    # GET_LILY_PATH
    #
    def test_get_lily_path(self):

        assert Config.get_lily_path() == str(self.tmpdir.join('.lily'))

    #
    # EXISTS
    #
    def test_exists(self):

        assert Config.exists() is True

        os.remove(str(self.tmpdir.join('.lily').join('config.json')))

        assert Config.exists() is False

    #
    # CREATE_EMPTY
    #
    def test_create_empty(self):

        os.remove(str(self.tmpdir.join('.lily').join('config.json')))

        Config.create_empty('some_service')

        assert json.loads(
            self.tmpdir.join('.lily').join('config.json').read()
        ) == {
            'last_commit_hash': '... THIS WILL BE FILLED AUTOMATICALLY ...',
            'name': '... PUT HERE NAME OF YOUR PROJECT ...',
            'repository': '... PUT HERE URL OF REPOSITORY ...',
            'src_dir': 'some_service',
            'version': '... PUT HERE INITIAL VERSION ...',
            'next_version': None,
            'next_last_commit_hash': None,
        }

    def test_create_empty__lily_folder_does_not_exist(self):

        self.tmpdir.join('.lily').remove()

        Config.create_empty('some_service')

        assert json.loads(
            self.tmpdir.join('.lily').join('config.json').read()
        ) == {
            'last_commit_hash': '... THIS WILL BE FILLED AUTOMATICALLY ...',
            'name': '... PUT HERE NAME OF YOUR PROJECT ...',
            'repository': '... PUT HERE URL OF REPOSITORY ...',
            'src_dir': 'some_service',
            'version': '... PUT HERE INITIAL VERSION ...',
            'next_version': None,
            'next_last_commit_hash': None,
        }

    #
    # PROPERTIES: GETTERS & SETTERS
    #
    def test_properties__getters(self):

        config = Config()

        assert config.name == 'hello'
        assert config.src_dir == 'some_service'
        assert config.src_path == str(self.tmpdir.join('some_service'))
        assert config.repository == 'bithub'
        assert config.version == '0.1.9'
        assert config.last_commit_hash == '940594'
        assert config.next_version == '0.2.1'
        assert config.next_last_commit_hash == 'fd898fd'

    def test_properties__setters(self):

        def read_from_conf(prop):
            conf = json.loads(self.lily_dir.join('config.json').read())

            return conf[prop]

        config = Config()

        # -- version
        config.version = '9.9.1'
        assert read_from_conf('version') == '9.9.1'

        # -- next_version
        config.next_version = '9.0.8'
        assert read_from_conf('next_version') == '9.0.8'

        # -- src_dir
        config.src_dir = 'entity_service'
        assert read_from_conf('src_dir') == 'entity_service'

        # -- last_commit_hash
        config.last_commit_hash = 'f7d87cd78'
        assert read_from_conf('last_commit_hash') == 'f7d87cd78'

        # -- next_last_commit_hash
        config.next_last_commit_hash = 'f7d87cd78'
        assert read_from_conf('next_last_commit_hash') == 'f7d87cd78'
