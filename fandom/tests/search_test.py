# -*- coding: utf-8 -*-
import unittest

import fandom

class TestSearch(unittest.TestCase):
  """Test the functionality of fandom.search."""

  def test_search(self):
    """Test parsing a Wikipedia request result."""
    search = fandom.search("Albus Dumbledore", language="en", wiki = "harrypotter")
    self.assertIsInstance(search, list)
    self.assertEqual(len(search), 10)
    self.assertIsInstance(search[0], tuple)
    self.assertEqual(len(search[0]), 2)

  def test_limit(self):
    """Test limiting a request results."""
    search = fandom.search("wands", wiki = "harrypotter", language = "en", results=3)
    self.assertIsInstance(search, list)
    self.assertEqual(len(search), 3)

  def test_random(self):
    """Test the random function."""
    random1 = fandom.random(wiki = "runescape")
    random2 = fandom.random(pages = 10, wiki = "runescape")
    self.assertIsInstance(random1, tuple)
    self.assertIsInstance(random1[0], str)
    self.assertIsInstance(random1[1], int)
    self.assertIsInstance(random2, list)
    self.assertIsInstance(random2[0], tuple)
    self.assertEqual(len(random2), 10)

