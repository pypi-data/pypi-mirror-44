from __future__ import annotations

import os
from abc import ABCMeta
from string import Template
from configparser import ConfigParser
from typing import AnyStr, Dict, TYPE_CHECKING

from config_handler.constants import ConfigKeys
from config_handler.exceptions import ConfigHandlerFileReadException


if TYPE_CHECKING:
    from config_handler.handler import ConfigHandler


class ConfigFile(metaclass=ABCMeta):
    """Abstract method for ConfigFile consumers."""

    def __init__(self, config_handler: ConfigHandler):
        """:param config_handler: a ConfigHandler object
        """

        self._config_handler = config_handler

    def _check_config_path_exist(self) -> bool:
        """Check if the config file path exist.
        :return: True or False
        """

        return os.path.exists(self._config_handler.config_path)

    def _read_config_file(self) -> ConfigParser:
        """Reads contents of the config file for internal purposes.
        :return: ConfigParser object
        """

        config = ConfigParser()

        if self._check_config_path_exist():
            config.read(self._config_handler.config_path)
        else:
            config.read_dict({
                ConfigKeys.DEFAULT: {}
            })

        return config

    def _get_template_path(self) -> AnyStr:
        """Returns path to where the config file should be saved.
        Initialize it if one is not provided in __init__().
        :return: path
        """

        if not self._config_handler.template_path:
            self._config_handler.template_path = \
                f'{self._config_handler.config_path}.template'

        return self._config_handler.template_path

    def check_config_path(self) -> None:
        """Checks whether the config path exists or not.
        :return: None
        """

        if not self._config_handler.config_path:
            raise ConfigHandlerFileReadException('Config path not set')

    def check_template_path(self) -> None:
        """Checks whether the config path exists or not.
        :return: None
        """

        if not os.path.exists(self._get_template_path()):
            msg = f'Template file doesn\'t ' \
                  f'exist: {self._config_handler.template_path}'
            raise ConfigHandlerFileReadException(msg)

    def read_template_file(self, template_vars: Dict) -> ConfigParser:
        """Reads contents of the config template file.
        :param template_vars: variables for inserting into template config
        :return: ConfigParser object
        """

        with open(self._get_template_path()) as f:
            t = Template(f.read())
            template_string = t.safe_substitute(**template_vars)

        config = ConfigParser()
        config.read_string(template_string)

        return config


class Reader(ConfigFile):
    """A ConfigFile reader class."""

    def check_config_path(self) -> None:
        """Checks whether the config path exists or not.
        :return: None
        """

        if not self._config_handler.config_path:
            raise ConfigHandlerFileReadException('Config path not set')

        if not self._check_config_path_exist():
            msg = f'Config file doesn\'t ' \
                  f'exist: {self._config_handler.config_path}'
            raise ConfigHandlerFileReadException(msg)


class Writer(ConfigFile):
    """A ConfigFile writer class."""

    def check_config_path(self) -> None:
        """Checks whether the config path exists or not.
        :return: None
        """

        if not self._config_handler.config_path:
            raise ConfigHandlerFileReadException('Config path not set')

    def write_config_file(self, config: ConfigParser) -> None:
        """Writes contents into the config file using ConfigParser lib.
        :return: None
        """

        with open(self._config_handler.config_path, 'w') as f:
            config.write(f)
