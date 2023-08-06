from __future__ import annotations

from typing import AnyStr, Dict
from configparser import ConfigParser, MissingSectionHeaderError

from config_handler.config_file import Reader, Writer
from config_handler.exceptions import ConfigHandlerFileReadException


class ConfigHandler:
    """Config handler class"""

    def __init__(self, config_path: AnyStr = None):
        """:param config_path: a path to actual config file
        """

        self.template_path = None
        self.config_path = config_path

    def sync(self, template_vars: Dict = None) -> ConfigHandler:
        """Sync template config with actual config.
        :param template_vars: variables for inserting into template config
        :return:
        """

        writer = Writer(self)

        writer.check_config_path()
        writer.check_template_path()

        if template_vars is None:
            template_vars = {}

        # read config template using template variables
        config = writer.read_template_file(template_vars)

        # merge config template with config
        config.read(self.config_path)

        # write merged config dict to file
        writer.write_config_file(config)

        return self

    def read(self) -> ConfigParser:
        """Reads actual config file for external purposes.
        :return: config dict
        """

        reader = Reader(self)

        reader.check_config_path()

        try:
            config = ConfigParser()
            config.read(self.config_path)
            return config

        except MissingSectionHeaderError:
            raise ConfigHandlerFileReadException('Missing sections in config')
