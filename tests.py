# -*- coding: utf-8 -*-

import unittest
import log
class TestLine(unittest.TestCase):

    def test_processing(self):
        text = 'you @.hit @+goblin@- with a @+sword@-! Okay'
        l = log.Line(text, 0, (1, 2))
        self.assertEqual(l.tokens, ['You ', '@hit ', 1, 'goblin', 0, ' ', 'with ', 'a ', 2, 'sword', 0, '! ', 'Okay.'])
