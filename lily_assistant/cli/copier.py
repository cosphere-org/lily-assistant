
import os
import re
import shutil

import click

from lily_assistant import settings, __version__


class Copier:

    class NotProjectRootException(Exception):
        pass

    def __init__(self):
        self.root_dir = os.getcwd()

    def copy(self, src_dir):

        # -- copy hooks
        self.copy_hooks()

        # -- copy Makefile
        self.copy_makefile(src_dir)

    def copy_hooks(self):

        git_dir = os.path.join(self.root_dir, '.git')
        copy_hooks_dir = os.path.join(git_dir, 'hooks')
        if os.path.exists(git_dir):
            if os.path.exists(copy_hooks_dir):
                shutil.rmtree(copy_hooks_dir)

        else:
            raise Copier.NotProjectRootException(
                'it seems that you\'ve executed not from the root of the '
                'project.')

        shutil.copytree(settings.HOOKS_DIR, copy_hooks_dir)

        click.secho(
            'copied git hooks to {copy_hooks_dir}'.format(
                copy_hooks_dir=copy_hooks_dir),
            fg='blue')

    def copy_makefile(self, src_dir):

        current_version = __version__

        with open(settings.MAKEFILE_PATH, 'r') as makefile:
            content = makefile.read()
            content = re.sub(r'{%\s*SRC_DIR\s*%}', src_dir, content)
            content = re.sub(r'{%\s*VERSION\s*%}', current_version, content)

        if not os.path.exists(os.path.join(self.root_dir, '.lily')):
            os.mkdir(os.path.join(self.root_dir, '.lily'))

        makefile_path = os.path.join(
            self.root_dir, '.lily', 'lily_assistant.makefile')

        with open(makefile_path, 'w') as f:
            f.write(content)

        click.secho(
            'copied lily_assistant makefile to {makefile_path}'.format(
                makefile_path=makefile_path),
            fg='blue')
