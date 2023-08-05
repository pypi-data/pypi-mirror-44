# built-in
from argparse import ArgumentParser
from pathlib import Path

# app
from ..config import builders
from ..venvs import VEnvs
from .base import BaseCommand
from .helpers import get_python


class VenvCreateCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='dephell venv create',
            description='Create virtual environment for current project.',
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
        if venv.exists():
            self.logger.warning('venv already exists', extra=dict(path=venv.path))
            return False

        self.logger.info('creating venv for project...', extra=dict(path=venv.path))
        python = get_python(self.config)
        self.logger.debug('choosen python', extra=dict(version=python.version))
        venv.create(python_path=python.path)
        self.logger.info('venv created', extra=dict(path=venv.path))
        return True
