# -*- coding: utf-8 -*-
import unittest

from wikia import wikia


class TestLang(unittest.TestCase):
  """Test the ability for wikia to change the language of the API being accessed."""

  def test_lang(self):
    wikia.set_lang("fr")
    self.assertEqual(wikia.API_URL, 'http://fr.www.wikia.com/api/v1')
    wikia.set_subwikia("runescape")
    self.assertEqual(wikia.API_URL, 'http://fr.runescape.wikia.com/api/v1')
