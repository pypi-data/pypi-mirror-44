# built-in
from argparse import ArgumentParser

# app
from ..config import builders
from ..controllers import analize_conflict
from ..converters import CONVERTERS
from ..models import Requirement
from .base import BaseCommand


DUMPERS = (
    ('setuppy', 'setup.py'),
    ('egginfo', '.'),
    ('sdist', 'dist/'),
    ('wheel', 'dist/'),
)


class BuildCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='dephell build',
            description='Create dist archives for project',
        )
        builders.build_config(parser)
        builders.build_from(parser)
        builders.build_resolver(parser)
        builders.build_api(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        return parser

    def __call__(self):
        loader = CONVERTERS[self.config['from']['format']]
        resolver = loader.load_resolver(path=self.config['from']['path'])

        # attach
        if self.config.get('and'):
            for source in self.config['and']:
                loader = CONVERTERS[source['format']]
                root = loader.load(path=source['path'])
                resolver.graph.add(root)

            # merge (without full graph building)
            resolved = resolver.resolve(level=1)
            if not resolved:
                conflict = analize_conflict(resolver=resolver)
                self.logger.warning('conflict was found')
                print(conflict)
                return False
            self.logger.info('merged')

        # dump
        for to_format, to_path in DUMPERS:
            if to_format == self.config['from']['format']:
                continue
            self.logger.info('dumping...', extra=dict(format=to_format))
            dumper = CONVERTERS[to_format]
            dumper.dump(
                path=to_path,
                reqs=Requirement.from_graph(resolver.graph, lock=False),
                project=resolver.graph.metainfo,
            )

        self.logger.info('builded')
        return True
