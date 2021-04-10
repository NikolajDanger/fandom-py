# -*- coding: utf-8 -*-
import unittest
import fandom
from unittest.mock import patch

class TestLang(unittest.TestCase):
  """Test the ability for fandom to change the language of the API being accessed."""

  def tearDown(self):
    fandom.set_lang("en")

  def test_lang(self):
    fandom.set_lang("nl")
    self.assertEqual(fandom.default_url(), 'https://fandom.com/nl/')
    fandom.set_subfandom("runescape")
    self.assertEqual(fandom.default_url(), 'https://runescape.fandom.com/nl/')
    page = fandom.page("runes")
    self.assertEqual(page.language, "nl")

  def test_wrong_lang(self):
    fandom.set_lang("ln")
    fandom.set_subfandom("runescape")
    rp = lambda: fandom.page("runes")
    self.assertRaises(fandom.error.RequestError, rp)
