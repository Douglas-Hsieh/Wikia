# -*- coding: utf-8 -*-
import unittest

from collections import defaultdict

from wikia import wikia
from request_mock_data import mock_data


# mock out _wiki_request
class _wiki_request(object):

  calls = defaultdict(int)

  @classmethod
  def __call__(cls, params):
    cls.calls[params.__str__()] += 1
    return mock_data["_wiki_request calls"][tuple(sorted(params.items()))]

wikia._wiki_request = _wiki_request()


class TestSearch(unittest.TestCase):
  """Test the functionality of wikia.search."""

  def test_search(self):
    """Test parsing a Wikipedia request result."""
    self.assertEqual(wikia.search("Barack Obama"), mock_data['data']["barack.search"])

  def test_limit(self):
    """Test limiting a request results."""
    self.assertEqual(wikia.search("Porsche", results=3), mock_data['data']["porsche.search"])
