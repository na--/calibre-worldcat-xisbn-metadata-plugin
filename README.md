# WorldCat xISBN metadata plugin for Calibre

A simple Calibre metadata source plugin that uses the [getMetadata](http://xisbn.worldcat.org/xisbnadmin/doc/api.htm#getmetadata) service
from http://xisbn.worldcat.org

### Limitations and caveats

- Searching is by ISBN only
- The returned metadata is limited to book title, authors, publisher, language and year (not the precise date)
- Other xISBN services like `getEditions` or searching the whole worldcat database are not supported
- The free publicly-accessible version of xISBN is limited to 1000 requests per day and the plugin does not have support for the subscription authentication
