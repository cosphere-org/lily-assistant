
import json
import os


class Config:

    def __init__(self):
        with open(self.get_config_path()) as f:
            self.config = json.loads(f.read())

    @classmethod
    def get_project_path(cls):
        return os.getcwd()

    @classmethod
    def get_config_path(cls):
        return os.path.join(cls.get_lily_path(), 'config.json')

    @classmethod
    def get_lily_path(cls):
        return os.path.join(os.getcwd(), '.lily')

    @classmethod
    def exists(cls):
        return os.path.exists(cls.get_config_path())

    @classmethod
    def create_empty(cls, src_dir):
        if not os.path.exists(cls.get_lily_path()):
            os.mkdir(cls.get_lily_path())

        with open(cls.get_config_path(), 'w') as f:
            f.write(
                json.dumps(
                    {
                        'name': '... PUT HERE NAME OF YOUR PROJECT ...',
                        'src_dir': src_dir,
                        'repository': '... PUT HERE URL OF REPOSITORY ...',
                        'version': '... PUT HERE INITIAL VERSION ...',
                        'last_commit_hash': (
                            '... THIS WILL BE FILLED AUTOMATICALLY ...'),
                        'next_version': None,
                        'next_last_commit_hash': None,
                    },
                    indent=4,
                    sort_keys=False))

        return cls()

    def _save(self):
        with open(self.get_config_path(), 'w') as f:
            f.write(
                json.dumps(
                    {
                        'name': self.name,
                        'src_dir': self.src_dir,
                        'repository': self.repository,
                        'version': self.version,
                        'next_version': self.next_version,
                        'last_commit_hash': self.last_commit_hash,
                        'next_last_commit_hash': self.next_last_commit_hash,
                    },
                    indent=4,
                    sort_keys=False))

    @property
    def name(self):
        return self.config['name']

    #
    # REPOSITORY
    #
    @property
    def repository(self):
        return self.config['repository']

    #
    # SRC_DIR
    #
    @property
    def src_dir(self):
        return self.config['src_dir']

    @src_dir.setter
    def src_dir(self, value):
        self.config['src_dir'] = value
        self._save()

    @property
    def src_path(self):
        return os.path.join(
            self.get_project_path(), self.config['src_dir'])

    #
    # VERSION
    #
    @property
    def version(self):
        return self.config['version']

    @version.setter
    def version(self, value):
        self.config['version'] = value
        self._save()

    @property
    def next_version(self):
        return self.config.get('next_version')

    @next_version.setter
    def next_version(self, value):
        self.config['next_version'] = value
        self._save()

    #
    # LAST_COMMIT_HASH
    #
    @property
    def last_commit_hash(self):
        return self.config['last_commit_hash'].split('#')[0].strip()

    @last_commit_hash.setter
    def last_commit_hash(self, value):
        self.config['last_commit_hash'] = value
        self._save()

    @property
    def next_last_commit_hash(self):
        return self.config.get('next_last_commit_hash')

    @next_last_commit_hash.setter
    def next_last_commit_hash(self, value):
        self.config['next_last_commit_hash'] = value
        self._save()
