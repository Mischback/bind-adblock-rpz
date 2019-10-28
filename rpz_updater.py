#!/usr/bin/env python3

# Python imports
import logging
from logging.handlers import SysLogHandler
import os
import requests
import sys
import yaml

# ### Basic logging setup ###
# This sets up a logger attached to syslog and provides a very basic mean of
# logging.
# This logger will get replaced by a user provided logging configuration, that
# is specified in a configuration file. Alternatively, logging is disabled by
# attaching a NullLogger handler.
logger = logging.getLogger('rpz-updater')
# logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)
syslogh = SysLogHandler(address='/dev/log')
syslogf = logging.Formatter(fmt='rpz-updater.py: %(levelname)s: %(message)s')
syslogh.setFormatter(syslogf)
logger.addHandler(syslogh)

# assume a default location and filename for configuration
parent_dir = os.path.dirname(os.path.realpath(__file__))
default_conf_file = os.path.join(parent_dir, 'config.yml')


class BlocklistProviderException(Exception):
    pass

class BlocklistProviderExceptionNotImplemented(BlocklistProviderException):
    pass

class BlocklistProvider(object):

    def __init__(self):
        """Creates an instance of BlocklistProvider.

        Upon object creation, the list is fetched and processed to provide
        just a list of domain names."""

        self.blocklist = self.convert(self.fetch())

    def convert(self, raw):
        """This method converts a blocklist into a list of domains."""

        raise BlocklistProviderException(
            'This method has to be implemented!'
        )

    def fetch(self):
        """This method fetches a blocklist."""

        raise BlocklistProviderException(
            'This method has to be implemented!'
        )

    def get_blocklist(self):
        """This method returns the converted blocklist."""

        return self.blocklist

class HttpBlocklistProvider(BlocklistProvider):

    def __init__(self, url):
        logger.debug(
            'Creating HttpBlocklistProvider for url {}'.format(self.url)
        )

        # store the URL in the object
        self.url = url

        # call parent constructor
        super().__init__()

    def fetch(self):

        headers = {
            'User-Agent': 'bind-adblock-rpz'
        }

        try:
            logger.debug('Trying to fetch {}'.format(self.url))
            # TODO: Make timeout configurable!
            response = requests.get(self.url, headers=headers, timeout=10)

            if response.status_code == 200:
                logger.debug('Successfully fetched from url {}'.format(self.url))
                return response.text
        except requests.exceptions.RequestException as e:
            logger.debug(
                'RequestException while fetching from {}: {}'.format(self.url, e)
            )
            return None

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
