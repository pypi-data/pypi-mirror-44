import os
from collections import namedtuple

import yaml

Config = namedtuple('Config', ['username', 'password'])


def get_config():
    config = _read_from_env()

    if not config.username or not config.password:
        config = _read_from_file(config)

    _validate_config(config)

    return config


def _read_from_env():
    """
    Try to get values from ENV
    :return: Config object that may contain None values
    """
    username, password = [os.environ.get(e)
                          for e in ["N26_USER", "N26_PASSWORD"]]
    return Config(username, password)


def _read_from_file(config):
    """
    Read config file (if possible) and merge it's content with the given config.
    If the given config already contains values they will be preserved.

    :param config: a config object that might already contain values
    :return: Config object with added values from config file (if any)
    """
    config_file = os.path.expanduser('~/.config/n26.yml')
    if not os.path.exists(config_file):
        # config file doesn't exist
        return config

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        if not cfg:
            raise ValueError("Config file is missing or empty")

        if 'n26' not in cfg:
            raise ValueError("Config file is missing 'n26' node")

        root_node = cfg['n26']
        if root_node:
            if not config.username:
                config = config._replace(username=root_node.get('username', config.username))
            if not config.password:
                config = config._replace(password=root_node.get('password', config.password))

    return config


def _validate_config(config):
    if not config:
        raise ValueError("Config is None!")
    if not config.username:
        raise ValueError('Missing config param: username')
    if not config.password:
        raise ValueError('Missing config param: password')
