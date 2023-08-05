# built-in
from argparse import ArgumentParser
from pathlib import Path

# external
from dephell_shells import Shells

# app
from ..config import builders
from ..venvs import VEnvs
from .base import BaseCommand
from .helpers import get_python


class VenvShellCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='dephell venv shell',
            description='Activate virtual environment for current project.',
        )
        builders.build_config(parser)
        builders.build_from(parser)
        builders.build_venv(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        return parser

    def __call__(self) -> bool:
        venvs = VEnvs(path=self.config['venv'])
        venv = venvs.get(Path(self.config['project']), env=self.config.env)
        if not venv.exists():
            self.logger.info('Creating venv for project...')
            python = get_python(self.config)
            self.logger.debug('choosen python', extra=dict(version=python.version))
            venv.create(python_path=python.path)

        shells = Shells(bin_path=venv.bin_path)
        shells.run()
        return True
