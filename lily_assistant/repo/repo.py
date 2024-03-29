
import os
import re
from subprocess import Popen, PIPE, STDOUT
import shlex

import click

from lily_assistant.config import Config


class Repo:

    def __init__(self):
        self.base_path = Config.get_project_path()
        self.cd_to_repo()

    def cd_to_repo(self):
        os.chdir(self.base_path)

    #
    # GIT
    #
    def clone(self, destination):
        self.git(f'clone {self.origin} {destination}')

    def push(self):
        self.git(f'push origin {self.current_branch}')

    def stash(self):
        self.git('stash')

    def pull(self):
        self.git(f'pull origin {self.current_branch}')

    @property
    def current_branch(self):
        return self.git('rev-parse --abbrev-ref HEAD').strip()

    @property
    def current_commit_hash(self):
        return self.git('rev-parse HEAD').strip()

    def add_all(self):
        self.git('add .')
        self.git('add -u .')

    def add(self, path):
        self.git(f'add {path}')

    def commit(self, message):
        self.git(f'commit --no-verify -m "{message}"')

    def all_changes_commited(self):
        changed = self.git('status --porcelain').strip()
        if changed:
            files = changed.split('\n')
            not_lily_changes = [f for f in files if '.lily/' not in f]

            return not bool(not_lily_changes)

        return True

    def git(self, command):
        return self.execute(f'git {command}')

    #
    # DIR / FILES
    #
    def clear_dir(self, path):

        path = re.sub('^/', '', path)
        path = os.path.join(os.getcwd(), path)

        for filename in os.listdir(path):
            os.remove(os.path.join(path, filename))

    def create_dir(self, path):
        path = re.sub('^/', '', path)
        path = os.path.join(os.getcwd(), path)

        try:
            os.mkdir(path)

        except FileExistsError:
            pass

    #
    # GENERIC
    #
    def execute(self, command):

        click.secho(f'[EXECUTE] {command}', fg='blue')
        captured = ''

        p = Popen(
            self.split_command(command),
            stdout=PIPE,
            stderr=STDOUT,
            bufsize=1,
            universal_newlines=True)

        while p.poll() is not None:
            line = p.stdout.readline()
            captured += line
            click.secho(line, fg='white')

        # -- final read
        line = p.stdout.read()
        captured += line
        click.secho(line, fg='white')

        # -- fetch return code
        p.communicate()
        if p.returncode != 0:
            raise OSError(
                f'Command: {command} return exit code: {p.returncode}')

        return captured

    def split_command(self, command):

        return shlex.split(command)
