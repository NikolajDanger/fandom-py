# -*- coding: utf-8 -*-
import unittest

import fandom

class TestPageSetUp(unittest.TestCase):
  """Test the functionality of fandom.page's __init__ and load functions."""

  def test_missing(self):
    """Test that page raises a PageError for a nonexistant page."""
    purpleberry = lambda: fandom.page(subfandom="harrypotter", title="purpleberry")
    self.assertRaises(fandom.error.PageError, purpleberry)

  def test_redirect_true(self):
    """Test that a page successfully redirects a query."""
    # no error should be raised if redirect is test_redirect_true
    mp = fandom.page(subfandom="harrypotter", title="Professor Slughorn")

    self.assertEqual(mp.title, "Horace Slughorn")
    self.assertEqual(mp.url, "https://harrypotter.fandom.com/en/wiki/Horace_Slughorn")

  def test_redirect_false(self):
    """Test that page raises an error on a redirect when redirect == False."""
    mp = lambda: fandom.page(subfandom="harrypotter", title="The Potters", redirect=False)
    self.assertRaises(fandom.error.RedirectError, mp)

  def test_redirect_no_normalization(self):
    """Test that a page with redirects but no normalization query loads correctly"""
    the_party = fandom.page(subfandom="elderscrolls", title="Stormcloaks")
    self.assertIsInstance(the_party, fandom.FandomPage)
    self.assertEqual(the_party.title, "Stormcloaks")

  def test_redirect_with_normalization(self):
    """Test that a page redirect with a normalized query loads correctly"""
    the_party = fandom.page(subfandom="elderscrolls", title="stormcloaks")
    self.assertIsInstance(the_party, fandom.FandomPage)
    self.assertEqual(the_party.title, "Stormcloaks")

  def test_redirect_normalization(self):
    """Test that a page redirect loads correctly with or without a query normalization"""
    capital_party = fandom.page(subfandom="elderscrolls", title="Stormcloaks")
    lower_party = fandom.page(subfandom="elderscrolls", title="stormcloaks")

    self.assertIsInstance(capital_party, fandom.FandomPage)
    self.assertIsInstance(lower_party, fandom.FandomPage)
    self.assertEqual(capital_party.title, "Stormcloaks")
    self.assertEqual(capital_party, lower_party)

class TestPage(unittest.TestCase):
  """Test the functionality of the rest of fandom.page."""

  def setUp(self):
    self.grass = fandom.page(subfandom="starwars", title="Grass")
    self.moisture_farm = fandom.page(subfandom="starwars", title="Moisture farm")
    self.Boba_Fett= fandom.page(subfandom="starwars", title="Boba Fett")

  def test_from_page_id(self):
    """Test loading from a page id"""
    self.assertEqual(self.grass, fandom.page(subfandom="starwars", pageid=508340))

  def test_title(self):
    """Test the title."""
    self.assertEqual(self.grass.title, "Grass")
    self.assertEqual(self.moisture_farm.title, "Moisture farm")

  def test_url(self):
    """Test the url."""
    self.assertEqual(self.grass.url, "https://starwars.fandom.com/en/wiki/Grass")
    self.assertEqual(self.moisture_farm.url, "https://starwars.fandom.com/en/wiki/Moisture_farm")

  def test_content(self):
    """Test the plain text content."""
    self.assertIsInstance(self.grass.content, dict)
    self.assertIsInstance(self.moisture_farm.content, dict)

  def test_revision_id(self):
    """Test the revision id."""
    self.assertIsInstance(self.grass.revision_id, int)
    self.assertIsInstance(self.moisture_farm.revision_id, int)

  def test_summary(self):
    """Test the summary."""
    self.assertIsInstance(self.grass.summary, str)
    self.assertLessEqual(len(self.grass.summary), 500)
    self.assertIsInstance(self.moisture_farm.summary, str)
    self.assertLessEqual(len(self.moisture_farm.summary), 500)

  def test_images(self):
    """Test the list of image URLs."""
    self.assertIsInstance(sorted(self.grass.images), list)
    self.assertIsInstance(sorted(self.moisture_farm.images), list)
    self.assertLessEqual(1, len(self.grass.images))
    self.assertLessEqual(1, len(self.moisture_farm.images))

  def test_html(self):
    """Test the full HTML property."""
    self.assertIsInstance(self.grass.html, str)

  def test_sections(self):
    """Test the list of section titles."""
    self.assertIsInstance(sorted(self.moisture_farm.sections), list)

  def test_section(self):
    """Test text content of a single section."""
    self.assertIsInstance(self.Boba_Fett.section("survival"), str)
    self.assertEqual(self.Boba_Fett.section("sexual encounter with the sarlacc"), None)

  def test_infobox(self):
    """Test if page has an infobox"""
    self.assertIn('infobox', self.grass.content)
    self.assertNotIn('infobox', self.moisture_farm.content)
