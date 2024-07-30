# myapp/tests.py
from django.test import TestCase
from .utils import normaliseURL

class NormaliseURLTests(TestCase):

    def test_normalizes_scheme_and_netloc(self):
        url = "HTTP://Example.Com/some/path/"
        expected = "example.com/some/path"
        self.assertEqual(normaliseURL(url), expected)

    def test_for_https(self):
        url = "HTTPs://Example.Com/some/path/"
        expected = "example.com/some/path"
        self.assertEqual(normaliseURL(url), expected)

    def test_trailing_slash_removed(self):
        url = "http://example.com/some/path/"
        expected = "example.com/some/path"
        self.assertEqual(normaliseURL(url), expected)

    def test_no_scheme(self):
        url = "example.com/some/path"
        expected = "example.com/some/path"
        self.assertEqual(normaliseURL(url), expected)

    def test_complex_url(self):
        url = "HTTP://Example.Com:80/Some/Path/?query=test#fragment"
        expected = "example.com:80/Some/Path/?query=test#fragment"
        self.assertEqual(normaliseURL(url), expected)

    def test_complex_url_with_single_word_query(self):
        url = "HTTP://Example.Com:80/Some/Path/?query=t"
        expected = "example.com:80/Some/Path/?query=t"
        self.assertEqual(normaliseURL(url), expected)

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
