
import os
import setuptools
from lily_assistant import __version__


requirements_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')


def parse_requirements(requirements):

    return [
        r.strip()
        for r in requirements
        if not r.strip().startswith('#') and r.strip()
    ]


requirements = []
with open(requirements_path) as f:
    requirements.extend(parse_requirements(f.readlines()))


# -- SETUP
setuptools.setup(
    name='lily-assistant',
    version=__version__,
    author='CoSphere Team',
    description='Lily compatible code quality checking tool',
    url='https://github.com/cosphere-org/lily-assistant.git',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        lily_assistant=lily_assistant.cli.cli:cli
    '''
)
