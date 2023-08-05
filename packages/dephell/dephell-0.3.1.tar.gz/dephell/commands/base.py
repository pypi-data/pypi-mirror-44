# built-in
import json
import os.path
from functools import reduce
from logging import getLogger
from operator import getitem
from typing import Optional

# app
from ..config import config


class BaseCommand:
    logger = getLogger('dephell.commands')

    def __init__(self, argv):
        parser = self.get_parser()
        self.args = parser.parse_args(argv)
        self.config = self.get_config(self.args)

    @classmethod
    def get_parser(cls):
        return cls.parser

    @classmethod
    def get_config(cls, args):
        config.setup_logging()
        if args.config:
            config.attach_file(path=args.config, env=args.env)
        elif os.path.exists('pyproject.toml'):
            data = config.attach_file(path='pyproject.toml', env=args.env, silent=True)
            if data is None:
                cls.logger.warning('cannot find tool.dephell section in the config')
        else:
            cls.logger.warning('cannot find config file')
        config.attach_cli(args)
        config.setup_logging()
        return config

    def validate(self):
        is_valid = self.config.validate()
        if not is_valid:
            self.logger.error('invalid config')
            print(self.config.format_errors())
        return is_valid

    @staticmethod
    def get_value(data, key, sep: Optional[str] = '-'):
        # print all config
        if not key:
            return json.dumps(data, indent=2, sort_keys=True)

        if sep is None:
            return json.dumps(data[key], indent=2, sort_keys=True)

        keys = key.split(sep)
        value = reduce(getitem, keys, data)
        # print config section
        if type(value) is dict:
            return json.dumps(value, indent=2, sort_keys=True)

        # print one value
        return value
