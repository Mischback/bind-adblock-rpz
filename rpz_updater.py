#!/usr/bin/env python3

class BlocklistProvider(object):

    class BlocklistProviderException(Exception):
        pass

    class BlocklistProviderExceptionNotImplemented(BlocklistProviderException):
        pass

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
