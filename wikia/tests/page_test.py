# -*- coding: utf-8 -*-
from decimal import Decimal
import unittest

from wikia import wikia
from request_mock_data import mock_data


# mock out _wiki_request
def _wiki_request(params):
  return mock_data["_wiki_request calls"][tuple(sorted(params.items()))]
wikia._wiki_request = _wiki_request


class TestPageSetUp(unittest.TestCase):
  """Test the functionality of wikia.page's __init__ and load functions."""

  def test_missing(self):
    """Test that page raises a PageError for a nonexistant page."""
    # Callicarpa?
    purpleberry = lambda: wikia.page("purpleberry")
    self.assertRaises(wikia.PageError, purpleberry)

  def test_redirect_true(self):
    """Test that a page successfully redirects a query."""
    # no error should be raised if redirect is test_redirect_true
    mp = wikia.page("Menlo Park, New Jersey")

    self.assertEqual(mp.title, "Edison, New Jersey")
    self.assertEqual(mp.url, "http://en.wikia.org/wiki/Edison,_New_Jersey")

  def test_redirect_false(self):
    """Test that page raises an error on a redirect when redirect == False."""
    mp = lambda: wikia.page("Menlo Park, New Jersey", redirect=False)
    self.assertRaises(wikia.RedirectError, mp)

  def test_redirect_no_normalization(self):
    """Test that a page with redirects but no normalization query loads correctly"""
    the_party = wikia.page("Communist Party")
    self.assertIsInstance(the_party, wikia.WikiaPage)
    self.assertEqual(the_party.title, "Communist party")

  def test_redirect_with_normalization(self):
    """Test that a page redirect with a normalized query loads correctly"""
    the_party = wikia.page("communist Party")
    self.assertIsInstance(the_party, wikia.WikiaPage)
    self.assertEqual(the_party.title, "Communist party")

  def test_redirect_normalization(self):
    """Test that a page redirect loads correctly with or without a query normalization"""
    capital_party = wikia.page("Communist Party")
    lower_party = wikia.page("communist Party")

    self.assertIsInstance(capital_party, wikia.WikiaPage)
    self.assertIsInstance(lower_party, wikia.WikiaPage)
    self.assertEqual(capital_party.title, "Communist party")
    self.assertEqual(capital_party, lower_party)

class TestPage(unittest.TestCase):
  """Test the functionality of the rest of wikia.page."""

  def setUp(self):
    # some random wikia articles with images and sections
    self.dog = wikia.page("runescape", "Dog")
    # This is one of the longest articles on wikia, though that might change...
    self.palpatine = wikia.page("starwars", "Palpatine")

  def test_from_page_id(self):
    """Test loading from a page id"""
    self.assertEqual(self.dog, wikia.page(pageid=26173))

  def test_title(self):
    """Test the title."""
    self.assertEqual(self.dog.title, "Dog")
    self.assertEqual(self.palpatine.title, "Palpatine")

  def test_url(self):
    """Test the url."""
    self.assertEqual(self.dog.url, "http://runescape.wikia.com/wiki/Dog")
    self.assertEqual(self.palpatine.url, "http://en.wikia.org/wiki/Tropical_Depression_Ten_(2005)")

  def test_content(self):
    """Test the plain text content."""
    self.assertEqual(self.dog.content, mock_data['data']["dog.content"])
    self.assertEqual(self.palpatine.content, mock_data['data']["cyclone.content"])

  def test_revision_id(self):
    """Test the revision id."""
    self.assertEqual(self.dog.revision_id, mock_data['data']["dog.revid"])
    self.assertEqual(self.palpatine.revision_id, mock_data['data']["cyclone.revid"])

  def test_summary(self):
    """Test the summary."""
    self.assertEqual(self.dog.summary, mock_data['data']["dog.summary"])
    self.assertEqual(self.palpatine.summary, mock_data['data']["cyclone.summary"])

  def test_images(self):
    """Test the list of image URLs."""
    self.assertEqual(sorted(self.dog.images), mock_data['data']["dog.images"])
    self.assertEqual(sorted(self.palpatine.images), mock_data['data']["cyclone.images"])

  def test_references(self):
    """Test the list of reference URLs."""
    self.assertEqual(self.dog.references, mock_data['data']["dog.references"])
    self.assertEqual(self.palpatine.references, mock_data['data']["cyclone.references"])

  def test_links(self):
    """Test the list of titles of links to Wikia pages."""
    self.assertEqual(self.dog.links, mock_data['data']["dog.links"])
    self.assertEqual(self.palpatine.links, mock_data['data']["cyclone.links"])

  def test_html(self):
    """Test the full HTML method."""
    self.assertEqual(self.dog.html(), mock_data['data']["dog.html"])

  def test_sections(self):
    """Test the list of section titles."""
    self.assertEqual(self.dog.sections, mock_data['data']["dog.sections"])
    self.assertEqual(sorted(self.palpatine.sections), mock_data['data']["cyclone.sections"])

  def test_section(self):
    """Test text content of a single section."""
    self.assertEqual(self.dog.section("Dog"), mock_data['data']["dog.section.dog"])
    self.assertEqual(self.dog.section("Cat"), None)
    self.assertEqual(self.palpatine.section("Impact"), mock_data['data']["cyclone.section.impact"])
    self.assertEqual(self.palpatine.section("History"), None)
