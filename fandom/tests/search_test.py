# -*- coding: utf-8 -*-
import unittest

import fandom

class TestSearch(unittest.TestCase):
  """Test the functionality of fandom.search."""

  def test_search(self):
    """Test parsing a Wikipedia request result."""
    search = fandom.search("Albus Dumbledore", language="en", subfandom = "harrypotter")
    self.assertIsInstance(search, list)
    self.assertEqual(len(search), 10)

  def test_limit(self):
    """Test limiting a request results."""
    search = fandom.search("wands", subfandom = "harrypotter", language = "en", results=3)
    self.assertIsInstance(search, list)
    self.assertEqual(len(search), 3)
  
  def test_random(self):
    """Test the random function."""
    random1 = fandom.random(subfandom = "runescape")
    random2 = fandom.random(pages = 10, subfandom = "runescape")
    self.assertIsInstance(random1, str)
    self.assertIsInstance(random2, list)
    self.assertEqual(len(random2), 10)

