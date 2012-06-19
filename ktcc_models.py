#! /usr/bin/env python

import ktcc_utils as utils

class Card_Model(object):
    """Model of a card in the game of SET."""
    NUMBERS = (1, 2, 3)
    COLORS = ('green', 'red', 'blue')
    SYMBOLS = ('X', 'Y', 'Z')
    
    def __init__(self, num, color, sym):
        assert num in Card_Model.NUMBERS
        assert color in Card_Model.COLORS
        assert sym in Card_Model.SYMBOLS
        
        self.num = num
        self.color = color
        self.sym = sym

    def __repr__(self):
        return "Card_Model(%s, '%s', '%s')" % (self.num, self.color, self.sym)

    def __str__(self):
        return "%s" % (self.sym * self.num)


class Player_Model(object):
    """Model of a player in the game of SET."""
    GOOD_SCORE = 30
    BAD_SCORE = -10
    
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

        self.score = 0

    def __repr__(self):
        return "Player_Model(%r)" % self.cards

    @property
    def has_proper_set(self):
        return utils.is_valid_set(self.cards)

    def update(self):
        if len(self.cards) == 3:
            if self.has_proper_set:
                self.score += Player_Model.GOOD_SCORE
            else:
                self.score += Player_Model.BAD_SCORE
            self.cards = []
            
