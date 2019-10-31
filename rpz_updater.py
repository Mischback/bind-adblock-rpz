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

# assume a default location and filename for configuration
parent_dir = os.path.dirname(os.path.realpath(__file__))
default_conf_file = os.path.join(parent_dir, 'config.yml')

def setup_logging_default():
    """Provides a default configuration for logging, that is used during the
    first stage of the script, specifically before the config file could be
    read and user-specified logging is set up.

    This logger is attached to syslog and provides a very basic mean of
    logging. It will only handle messages of WARNING and above.

    This logger will be replaced by any user defined logging configuration."""

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    syslogf = logging.Formatter(fmt='rpz-updater.py: %(levelname)s: %(message)s')
    syslogh = SysLogHandler(address='/dev/log')
    syslogh.setLevel(logging.WARNING)
    syslogh.setFormatter(syslogf)
    logger.addHandler(syslogh)

    return logger

def load_and_check_config(conf_file, logger=logging.getLogger(__name__)):
    """Loads the configuration from a yaml file and checks, if the minimal
    required values are included."""

    try:
        config = yaml.safe_load(open(conf_file))
    except FileNotFoundError as e:
        logger.debug('Specified configuration file not found: {}'.format(e))
        config = None
    # TODO: Insert checks for required values here!

    return config

def main():
    """Provides the main logic.

    This is put into its own function to ease future test coverage."""

    # setup a default logger
    logger = setup_logging_default()

    conf_file=default_conf_file # TODO: Make the conf-file configurable by command line
    configuration = load_and_check_config(conf_file)
    if configuration is None:
        logger.error('Could not load configuration. Exiting now!')
        sys.exit(1)

    # this is just for debugging
    foo = HttpBlocklistProvider('http://mischback.de')

if __name__ == '__main__':
    # Let there be magic...
    main()
