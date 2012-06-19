#! /usr/bin/env python

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 127, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

def is_valid_set(c1, c2=None, c3=None):
    # permit passing of a single list as well
    if c2 == c3 == None:
        c1, c2, c3 = c1
    
    num_comp = False
    color_comp = False
    sym_comp = False
    
    if c1.num == c2.num == c3.num:
        num_comp = True
    elif c1.num != c2.num != c3.num:
        num_comp = True

    if c1.color == c2.color == c3.color:
        color_comp = True
    elif c1.color != c2.color != c3.color:
        color_comp = True

    if c1.sym == c2.sym == c3.sym:
        sym_comp = True
    elif c1.sym != c2.sym != c3.sym:
        sym_comp = True

    return (num_comp and color_comp and sym_comp)
