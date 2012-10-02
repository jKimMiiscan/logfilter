import os
import sys
import unittest

log_analyzer_path = '/Development/virtualenvs/miiscanLogAnalyzer/src/log_analyzer'
sys.path.append(log_analyzer_path)

from handler.filter import *

class ApacheErrorFilterTestCase(unittest.TestCase):

    def setUp(self):
        self.log_dump = """[Tue Oct 02 10:14:15 2012] [error] [client 157.56.93.153] File does not exist: /var/www/miiscan.com/html/robots.txt
[Tue Oct 02 10:15:59 2012] [error] [client 157.56.93.153] File does not exist: /var/www/miiscan.com/html/svc
[Tue Oct 02 10:53:55 2012] [error] [client 38.104.209.14] File does not exist: /var/www/miiscan.com/html/invite
[Tue Oct 02 10:53:55 2012] [error] [client 38.104.209.14] File does not exist: /var/www/miiscan.com/html/favicon.ico
[Tue Oct 02 10:56:24 2012] [error] [client 74.125.186.37] File does not exist: /var/www/miiscan.com/html/favicon.ico
[Tue Oct 02 13:14:16 2012] [error] [client 220.181.108.159] File does not exist: /var/www/miiscan.com/html/static
[Tue Oct 02 14:22:52 2012] [error] [client 180.76.5.165] File does not exist: /var/www/miiscan.com/html/robots.txt
[Tue Oct 02 14:22:52 2012] [error] [client 180.76.6.212] File does not exist: /var/www/miiscan.com/html/robots.txt
[Tue Oct 02 15:25:52 2012] [error] [client 74.125.183.25] File does not exist: /var/www/miiscan.com/html/favicon.ico
"""
        self.filtering_words = [".txt", ".ico", ".jpg", ".jpeg", ".png", ".gif"]
        self.line_contains_txt = """[Tue Oct 02 14:22:52 2012] [error] [client 180.76.5.165] File does not exist: /var/www/miiscan.com/html/robots.txt"""
        self.line_contains_txt_only = """[Tue Oct 02 14:22:52 2012] [error] [client 180.76.5.165] var/www/miiscan.com/html/robots.txt"""
        self.line_contains_ico = """[Tue Oct 02 10:56:24 2012] [error] [client 74.125.186.37] File does not exist: /var/www/miiscan.com/html/favicon.ico"""

    def tearDown(self):
        self.log_dump = None
        self.filtering_words = None
        self.line_contains_txt = None
        self.line_contains_txt_only = None
        self.line_contains_ico = None

    def test_one_line_has_no_filtering_words_returns_the_line(self):
        test_line = "TEST line"
        log_filename = "test.log"
        filtered_log_filename = "logs/filtered_test.log"
        apache_filter = ApacheErrorFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, apache_filter.filter_log_each_line(test_line))

    def test_one_line_has_ico_filtering_words_returns_false(self):
        test_line = self.line_contains_ico
        log_filename = "test.log"
        filtered_log_filename = "logs/filtered_test.log"
        apache_filter = ApacheErrorFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertFalse(apache_filter.filter_log_each_line(test_line))

    def test_one_line_has_txt_filtering_words_returns_false(self):
        test_line = self.line_contains_txt
        log_filename = "test.log"
        filtered_log_filename = "logs/filtered_test.log"
        apache_filter = ApacheErrorFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertFalse(apache_filter.filter_log_each_line(test_line))

    def test_one_line_has_txt_only_filtering_words_returns_the_line(self):
        test_line = self.line_contains_txt_only
        log_filename = "test.log"
        filtered_log_filename = "logs/filtered_test.log"
        apache_filter = ApacheErrorFilter(log_filename, filtered_log_filename, self.filtering_words)
        self.assertEqual(test_line, apache_filter.filter_log_each_line(test_line))


if __name__ == '__main__':
    unittest.main()
