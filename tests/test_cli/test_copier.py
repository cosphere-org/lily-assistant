
import os
from unittest import TestCase
from unittest.mock import call
import textwrap

import pytest

from lily_assistant.cli.copier import Copier
from lily_assistant import settings, __version__


class CopierTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, tmpdir, mocker):
        self.tmpdir = tmpdir
        self.mocker = mocker

    def setUp(self):
        self.lily_assistant_dir = self.tmpdir.mkdir('lily_assistant')
        self.project_dir = self.tmpdir.mkdir('project')

    #
    # COPY
    #
    def test_copy__makes_the_right_calls(self):

        copy_hooks = self.mocker.patch.object(Copier, 'copy_hooks')
        copy_makefile = self.mocker.patch.object(Copier, 'copy_makefile')

        Copier().copy('my_code')

        assert copy_hooks.call_args_list == [call()]
        assert copy_makefile.call_args_list == [call('my_code')]

    #
    # COPY_HOOKS
    #
    def test_copy_hooks__copies_all_hooks(self):

        os.chdir(str(self.project_dir))
        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('pre commit it')
        hooks_dir.join('surprise').write('surprise me')
        self.mocker.patch.object(settings, 'HOOKS_DIR', str(hooks_dir))
        copy_hooks_dir = gitdir.mkdir('hooks')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])

    def test_copy_hooks__not_root(self):

        self.project_dir.mkdir('.git')
        no_root_dir = self.project_dir.mkdir('not_root')
        os.chdir(str(no_root_dir))

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('surprise').write('surprise me')
        self.mocker.patch.object(settings, 'HOOKS_DIR', str(hooks_dir))

        try:
            Copier().copy_hooks()

        except Copier.NotProjectRootException as e:
            assert e.args[0] == (
                'it seems that you\'ve executed not from the root of '
                'the project.')

        else:
            raise AssertionError('should raise exception')

    def test_copy_hooks__copies_all_hooks__with_override(self):

        os.chdir(str(self.project_dir))
        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('NEW pre commit it')
        hooks_dir.join('surprise').write('NEW surprise me')
        self.mocker.patch.object(settings, 'HOOKS_DIR', str(hooks_dir))
        copy_hooks_dir = os.path.join(str(gitdir), 'hooks')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])
        assert (
            open(os.path.join(str(copy_hooks_dir), 'pre-commit')).read() ==
            'NEW pre commit it')
        assert (
            open(os.path.join(str(copy_hooks_dir), 'surprise')).read() ==
            'NEW surprise me')

    def test_copy_hooks__copies_all_hooks__when_hooks_do_not_exist(self):

        os.chdir(str(self.project_dir))
        gitdir = self.project_dir.mkdir('.git')

        hooks_dir = self.lily_assistant_dir.mkdir('hooks')
        hooks_dir.join('pre-commit').write('NEW pre commit it')
        hooks_dir.join('surprise').write('NEW surprise me')
        self.mocker.patch.object(settings, 'HOOKS_DIR', str(hooks_dir))
        copy_hooks_dir = gitdir.mkdir('hooks')
        copy_hooks_dir.join('pre-commit').write('OLD pre commit it')

        Copier().copy_hooks()

        assert os.listdir(str(gitdir)) == ['hooks']
        assert set(os.listdir(str(copy_hooks_dir))) == set([
            'pre-commit',
            'surprise',
        ])
        assert (
            open(os.path.join(str(copy_hooks_dir), 'pre-commit')).read() ==
            'NEW pre commit it')
        assert (
            open(os.path.join(str(copy_hooks_dir), 'surprise')).read() ==
            'NEW surprise me')

    #
    # COPY_MAKEFILE
    #
    def test_copy_makefile__copies_makefile(self):

        os.chdir(str(self.project_dir))

        makefile = self.lily_assistant_dir.join('lily_assistant.makefile')
        makefile.write(textwrap.dedent('''
            ## GENERATED FOR VERSION: {% VERSION %}

            lint:  ## lint the {% SRC_DIR %} & tests
                source env.sh && \
                flake8 --ignore D100,D101 tests && \
                flake8 --ignore D100,D101 {% SRC_DIR %}
        '''))
        self.mocker.patch.object(settings, 'MAKEFILE_PATH', str(makefile))

        Copier().copy_makefile(str('gigly'))

        result_makefile_content = (
            self.project_dir.join('.lily/lily_assistant.makefile').read())
        assert result_makefile_content == textwrap.dedent(f'''
            ## GENERATED FOR VERSION: {__version__}

            lint:  ## lint the gigly & tests
                source env.sh && \
                flake8 --ignore D100,D101 tests && \
                flake8 --ignore D100,D101 gigly
        ''')

    def test_copy_makefile__copies_makefile__with_override(self):

        os.chdir(str(self.project_dir))

        makefile = self.lily_assistant_dir.join('lily_assistant.makefile')
        makefile.write('NEW make it')
        self.mocker.patch.object(settings, 'MAKEFILE_PATH', str(makefile))
        self.project_dir.mkdir('.lily')
        self.project_dir.join(
            '.lily/lily_assistant.makefile').write('OLD make it')

        Copier().copy_makefile(str('gigly'))

        assert (
            self.project_dir.join('.lily/lily_assistant.makefile').read() ==
            'NEW make it')
