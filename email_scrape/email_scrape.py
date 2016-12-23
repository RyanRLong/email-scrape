#!/usr/bin/env python
"""

This module is used to recursively extract email addressed from
a url.

Example:


Todo:

"""

from __future__ import print_function

import re
import sys
import urllib
import urlparse
import warnings

import bs4
import mechanize

class EmailScraper(object):
    """ Scrape emails from URL """

    def __init__(self):
        warnings.filterwarnings('ignore') #ignore warnings
        self.browser = self.init_mechanize()
        self.url = {}

    @classmethod
    def init_mechanize(cls):
        """ Initialize and return a mechanize browser instance """
        browser = mechanize.Browser()
        #pylint: disable=maybe-no-member
        browser.set_handle_robots(False)
        browser.set_handle_refresh(False)
        browser.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]
        return browser

    @classmethod
    def eprint(cls, *args, **kwargs):
        """ for printing to stderr """
        print(*args, file=sys.stderr, **kwargs)

    def extract_and_normalize_hrefs(self, html):
        """ Extracts all hrefs from a page and returns as list """
        urls = self.extract_hrefs_from_html(html)
        return self.normalize_url_list(urls)

    @classmethod
    def extract_hrefs_from_html(cls, html):
        """ Returns a list of all hrefs from html """
        urls = []
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for link in soup.find_all(href=True):
            if len(link['href']) > 0:
                urls.append(link['href'])
        return urls

    @classmethod
    def extract_email_from_html(cls, html):
        """ Extracts all email addressed from page """
        email_pattern = "(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$| \
            \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\b)"
        email_list = []
        soup = bs4.BeautifulSoup(html, 'html.parser')

        for tag in soup.find_all(string=re.compile(email_pattern)):
            email_list.append(tag)

        return email_list

    @classmethod
    def get_unique_list(cls, original_list):
        """ Returns a unique list """
        return list(set(original_list))

    @classmethod
    def print_status(cls, visited, not_visited, current_url):
        """ Prints status to the terminal """
        cls.eprint("Remaining: " + str(len(not_visited))
                   + "  Visited: " + str(len(visited))
                   + "  Current: " + current_url, end='\r')

    def normalize_url_list(self, urls):
        """ Normalizes all urls in list """
        formatted_urls = []
        for url in urls:
            link = self.normalize_url(url)
            if link:
                formatted_urls.append(link)
        return self.get_unique_list(formatted_urls)

    def normalize_url(self, url):
        """ Appends the base domain to relative URLs and removes
        undesired URLs such as files """
        base_url = self.url.scheme + '://' + self.url.netloc
        file_identifier_pattern = re.compile(r'\.(css|ppt|jpg|gif|png|js|pdf|docx)$')
        url = url.strip()

        if url[0] == '/' or url[0] == '#':
            url = base_url + url
        if 'mailto:' in url:
            return
        elif not url.startswith(base_url):
            return
        elif file_identifier_pattern.search(url):
            return
        else:
            return url

    def extract_emails_from_url(self, seed_url):
        """ scrapes for email addresses recursively through a domain """
        self.url = urlparse.urlparse(seed_url)

        visited = []
        not_visited = []
        collected_email_addresses = []

        not_visited.append(seed_url)
        while len(not_visited) > 0:
            url = not_visited.pop()
            visited.append(url)
            url = urllib.quote(url, ':/#?')

            try:
                response = self.browser.open(url)
                html = response.read()

                not_visited = not_visited + self.extract_and_normalize_hrefs(html)
                collected_email_addresses = collected_email_addresses + \
                    self.extract_email_from_html(html)

                not_visited = [x for x in list(set(not_visited)) if x not in visited]
                self.print_status(visited, not_visited, url)
            except (mechanize.HTTPError, mechanize.URLError) as error:
                self.eprint(error, url)

        return self.get_unique_list(collected_email_addresses)


if __name__ == '__main__':

    import argparse

    PARSER = argparse.ArgumentParser(description='Recursively scrape email addresses from a url')
    PARSER.add_argument('url', help="the fully qualified domain name (http://www.example.com)")
    ARGS = PARSER.parse_args()

    SCRAPER = EmailScraper()
    print(SCRAPER.extract_emails_from_url(ARGS.url))
