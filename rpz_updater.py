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


class BindAdblockError(Exception):
    """App specific base class for all errors."""


class ConfigFileNotFoundError(BindAdblockError):

    def __init__(self, message, files_not_found, *args):
        """Just overwriting the constructor to provide a custom error
        variable (files_not_found)."""

        # extract the parameters for this error
        self.message = message
        self.files_not_found = files_not_found

        # call the base class constructor with all parameters
        super().__init__(message, files_not_found, *args)


def load_and_check_config(config_file, logger=logging.getLogger(__name__)):
    """Loads the configuration from a yaml file and checks, if the minimal
    required values are included."""

    # no config file specified, assume a default location
    if config_file is None:
        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'config.yml'
        )

    try:
        config = yaml.safe_load(open(config_file))
    except FileNotFoundError as e:
        logger.debug('Specified configuration file not found: {}'.format(e))

        files_not_found = [config_file]

        # look for the file in script's parent directory and assume, that
        # config_file is just the filename
        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            config_file
        )
        try:
            config = yaml.safe_load(open(config_file))
        except FileNotFoundError as e:
            logger.debug('Specified configuration file not found: {}'.format(e))

            files_not_found.append(config_file)

            raise ConfigFileNotFoundError(
                'Could not find configuration file!',
                files_not_found
            )

    # TODO: Insert checks for required values here!

    return config


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


def main():
    """Provides the main logic.

    This is put into its own function to ease future test coverage."""

    # setup a default logger
    logger = setup_logging_default()

    try:
        config = load_and_check_config(None)
    except ConfigFileNotFoundError as e:
        logger.error('Could not load configuration. Exiting now!')
        for f in e.files_not_found:
            logger.error('  - tried {} and got FileNotFoundError'.format(f))
        sys.exit(1)

    # this is just for debugging
    foo = HttpBlocklistProvider('http://mischback.de')


if __name__ == '__main__':
    # Let there be magic...
    main()
