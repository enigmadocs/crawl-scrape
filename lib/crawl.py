import requests
from bs4 import BeautifulSoup

import parsekit


class CrawlPages(parsekit.Step):

    base_url = parsekit.Argument(
        "The root of the site.",
        required=True,
        type=basestring)

    @property
    def last_page(self):
        # Establish a ceiling to iterate up to.
        soup = self._make_soup(self._get_page(self.options.base_url).content)
        return int(soup.find('li', class_='next').previous_sibling.string)

    def _get_page(self, url):
        resp = requests.get(url)
        resp.raise_for_status()
        return resp

    def _make_soup(self, html):
        return BeautifulSoup(html, 'html.parser')

    def run(self, _, metadata):
        for page in xrange(1, self.last_page+1):
            page_url = '{}/?page={}'.format(self.options.base_url, page)
            yield page_url, metadata
