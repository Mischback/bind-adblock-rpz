#!/usr/bin/env python3
# -*- utf-8 -*-

# Python imports
import logging
from logging.handlers import SysLogHandler
import os
import sys
import yaml

# app imports
from bind_adblock.provider import HttpBlocklistProvider

# ### Basic logging setup ###
# This sets up a logger attached to syslog and provides a very basic mean of
# logging.
# This logger will get replaced by a user provided logging configuration, that
# is specified in a configuration file. Alternatively, logging is disabled by
# attaching a NullLogger handler.
logger = logging.getLogger('')
# logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)
syslogf = logging.Formatter(fmt='rpz-updater.py: %(levelname)s: %(message)s')
syslogh = SysLogHandler(address='/dev/log')
syslogh.setFormatter(syslogf)
logger.addHandler(syslogh)

# assume a default location and filename for configuration
parent_dir = os.path.dirname(os.path.realpath(__file__))
default_conf_file = os.path.join(parent_dir, 'config.yml')



def load_and_check_config(conf_file):
    """Loads the configuration from a yaml file and checks, if the minimal
    required values are included."""

    try:
        config = yaml.safe_load(open(conf_file))
    except FileNotFoundError as e:
        logger.debug('Specified configuration file not found: {}'.format(e))
        config = None
    # TODO: Insert checks for required values here!

    return config


if __name__ == '__main__':
    logger.debug('rpz-updater.py started')

    conf_file=default_conf_file # TODO: Make the conf-file configurable by command line
    configuration = load_and_check_config(conf_file)
    if configuration is None:
        logger.error('Could not load configuration. Exiting now!')
        sys.exit(1)

    foo = HttpBlocklistProvider('http://mischback.de')
