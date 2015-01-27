"""A small script to display text from NPR's rss feeds.
"""
import urllib2
import xml.etree.ElementTree as ElementTree

class NprFeed(object):
    def __init__(self, rss_id):
        """An object that fetches the specified rss feed from NPR.org
        and parses the XLM into an ElementTree object.

        Args:
            rss_id (int): The NPR.org RSS feed ID as an integer
        """
        npr_url = "http://www.npr.org/rss/rss.php?id=%s" % rss_id
        self._root = ElementTree.fromstring(urllib2.urlopen(npr_url).read())

    def display(self, tag):
        """Return a list of strings of the tag from RSS feed.

        Args:
            tag (str): A tag from the RSS feed to be fetched from the
            ElementTree root.
        """
        items = []
        for item in self._root.iter(tag):
            items.append(item)
        return items


def main():
    """User interface to get NPR.org RSS feed and display the titles
    and descriptions in a terminal.
    """
    feed_id = raw_input("\nPlease enter the NPR.org RSS feed ID to fetch. > ")
    try:
        npr_headlines = NprFeed(feed_id)
    except urllib2.HTTPError:
        print "Error fetching NPR.org RSS feed: ", feed_id
        return

    zipped = zip(npr_headlines.display('title')[1:],
        npr_headlines.display('description'))
    
    print "\n\n"
    for title, description in zipped:
        print "\n**", title.text, "**"
        print description.text

main()