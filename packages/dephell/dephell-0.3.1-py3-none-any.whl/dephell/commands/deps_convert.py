# built-in
from argparse import ArgumentParser

# app
from ..config import builders
from ..controllers import analize_conflict
from ..converters import CONVERTERS
from ..models import Requirement
from .base import BaseCommand


class DepsConvertCommand(BaseCommand):
    @classmethod
    def get_parser(cls):
        parser = ArgumentParser(
            prog='dephell deps convert',
            description='Convert dependencies between formats',
        )
        builders.build_config(parser)
        builders.build_from(parser)
        builders.build_to(parser)
        builders.build_resolver(parser)
        builders.build_api(parser)
        builders.build_output(parser)
        builders.build_other(parser)
        return parser

    def __call__(self):
        loader = CONVERTERS[self.config['from']['format']]
        dumper = CONVERTERS[self.config['to']['format']]
        self.logger.info('converting...', extra={
            'from-format':  self.config['from']['format'],
            'from-path':    self.config['from']['path'],
            'to-format':    self.config['to']['format'],
            'to-path':      self.config['to']['path'],
        })

        # load
        resolver = loader.load_resolver(path=self.config['from']['path'])
        should_be_resolved = not loader.lock and dumper.lock

        # attach
        if self.config.get('and'):
            for source in self.config['and']:
                loader = CONVERTERS[source['format']]
                root = loader.load(path=source['path'])
                resolver.graph.add(root)

            # merge (without full graph building)
            if not should_be_resolved:
                resolved = resolver.resolve(level=1)
                if not resolved:
                    conflict = analize_conflict(resolver=resolver)
                    self.logger.warning('conflict was found')
                    print(conflict)
                    return False
                self.logger.info('merged')

        # resolve (and merge)
        if should_be_resolved:
            resolved = resolver.resolve()
            if not resolved:
                conflict = analize_conflict(resolver=resolver)
                self.logger.warning('conflict was found')
                print(conflict)
                return False
            self.logger.info('resolved')

        # dump
        dumper.dump(
            path=self.config['to']['path'],
            reqs=Requirement.from_graph(resolver.graph, lock=dumper.lock),
            project=resolver.graph.metainfo,
        )
        self.logger.info('converted')
        return True
