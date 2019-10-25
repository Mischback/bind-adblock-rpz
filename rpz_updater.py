#!/usr/bin/env python3

# Python imports
import requests

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

        # store the URL in the object
        self.url = url

        # call parent constructor
        super().__init__()

    def fetch(self):

        headers = {
            'User-Agent': 'bind-adblock-rpz'
        }

        try:
            # TODO: Make timeout configurable!
            response = requests.get(self.url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException as e:
            print(e)    # TODO: fix this! Should be logged to logfile!
            return None


if __name__ == '__main__':
    foo = HttpBlocklistProvider('http://mischback.de')
