#!/usr/bin/env python2

__license__ = 'GPL v3'
__copyright__ = '2017, Nedyalko Andreev <nedyalko.andreev@gmail.com>'
__docformat__ = 'en'

import json, datetime

from calibre.ebooks.metadata.sources.base import Source
from calibre.ebooks.metadata import check_isbn
from calibre.ebooks.metadata.book.base import Metadata

class WorldCatxISBN(Source):

    name = 'WorldCat xISBN'
    description = 'Downloads metadata from WorldCat\'s xISBN public serive'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Nedyalko Andreev'
    version = (1, 0, 0)
    minimum_calibre_version = (0, 8, 0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title', 'authors', 'publisher', 'pubdate', 'languages'])

    QURL = 'http://xisbn.worldcat.org/webservices/xid/isbn/%s?method=getMetadata&format=json&fl=*'

    def is_customizable(self):
        return False

    def identify(self, log, result_queue, abort, title=None, authors=None,
                 identifiers={}, timeout=30):
        isbn = check_isbn(identifiers.get('isbn', None))
        if isbn is None:
            log.info("The plugin can only look up data by ISBN")
            return None

        url = self.QURL%isbn
        log.info('Querying: %s' % url)
        data = json.loads(self.browser.open_novisit(url, timeout=timeout).read())
        log.info('Got JSON data: %s' % data)

        if data.get('stat', None) != 'ok':
            return None
        data = data.get('list', [])
        if len(data) == 0:
            return None
        data = data[0]

        log.info("Book JSON data: %s" % data)

        title = data.get("title", None)
        authors = data.get("author", None)
        if title is None or authors is None:
            return None

        authors = authors.rstrip('.').replace(' and ', ',').replace(';', ',').split(',')

        mi = Metadata(title, [a.strip() for a in authors])
        mi.publisher = data.get("publisher", None)
        mi.languages = data.get("lang", None).split(',')

        year = data.get("year", None)
        if year is not None:
            mi.pubdate = datetime.date(int(year), 1, 1)

        log.info("Final formatted result: %s" % mi)
        result_queue.put(mi)


if __name__ == '__main__': # tests
    # To run these test use:
    # calibre-debug -e __init__.py
    from calibre.ebooks.metadata.sources.test import (
        test_identify_plugin, title_test, authors_test, series_test)

    test_identify_plugin(WorldCatxISBN.name, [
        (# A book with an ISBN
            {'identifiers':{'isbn': '9780380789016'}},
            [title_test('Neverwhere', exact=True),
             authors_test(['Neil Gaiman'])]
        ),
        (# A book with two authors
            {'identifiers':{'isbn': '0765325950'}},
            [title_test('A memory of light', exact=True),
             authors_test(['Robert Jordan', 'Brandon Sanderson'])]
        ),
    ])
    #TODO: test for errors when no ISBN is supplied?
