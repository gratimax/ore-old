from unittest import TestCase as UnitTestTestCase

import re
from ore.core import regexs


class RegexTestCase(object):
    REGEX = None

    def assertMatches(self, thing, *args, **kwargs):
        self.assertIsNotNone(re.match(self.REGEX, thing), *args, **kwargs)

    def assertDoesNotMatch(self, thing, *args, **kwargs):
        self.assertIsNone(re.match(self.REGEX, thing), *args, **kwargs)


class ExtendedNameRegexTest(RegexTestCase, UnitTestTestCase):
    REGEX = regexs.EXTENDED_NAME_REGEX

    def test_allows_ascii_lower(self):
        self.assertMatches("abcdefghijklmnopqrstuvwxyz")

    def test_allows_ascii_upper(self):
        self.assertMatches("ABCDEFGHIJKLMNOPQRSTVUWXYZ")

    def test_allows_numbers(self):
        self.assertMatches("1234567890")

    def test_allows_some_symbols(self):
        for symbol in "-_.":
            self.assertMatches(
                'x' + symbol, msg="Didn't match {} but should've".format(symbol))

    def test_allows_symbols_at_start(self):
        for symbol in "_.":
            self.assertMatches(
                symbol, msg="Didn't match {} but should've".format(symbol))

    def test_disallows_hyphens_at_start(self):
        for symbol in "-":
            self.assertDoesNotMatch(
                symbol, msg="Didn't match {} but should've".format(symbol))

    def test_disallows_symbols(self):
        for symbol in "!#$%^&/*()[]=;'\",/+@":
            self.assertDoesNotMatch(
                symbol, msg="Matched {} but shouldn't".format(symbol))


class TrimNameRegexTest(ExtendedNameRegexTest):
    REGEX = regexs.TRIM_NAME_REGEX

    def test_allows_space_in_middle(self):
        self.assertMatches("heaven soda")

    def test_allows_multiple_spaces_in_middle(self):
        self.assertMatches("heaven soda with lime and ice")

    def test_allows_multiple_contiguous_spaces_in_middle(self):
        self.assertMatches("heaven        soda")

    def test_disallows_spaces_at_start(self):
        self.assertDoesNotMatch(" heaven soda")

    def test_disallows_spaces_at_end(self):
        self.assertDoesNotMatch("heaven soda ")
