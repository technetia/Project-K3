#! /usr/bin/env python

import random

import pygame
from pygame.locals import *

pygame.init()

import ktcc_utils as utils
import ktcc_models as models

RESOLUTION = SCR_WIDTH, SCR_HEIGHT = 640, 480
SCREEN = pygame.display.set_mode(RESOLUTION)
BACKGROUND = pygame.Surface(RESOLUTION)
pygame.display.set_caption("KT Coding Challenge")
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

SCOREBOARD_BORDER = SCR_WIDTH - 120

class Card(pygame.sprite.Sprite):
    FONT_SIZE = 25

    def __init__(self, num, color, sym, pos, fall_speed):
        super(Card, self).__init__()
        self.model = models.Card_Model(num, color, sym)
        self.x, self.y = pos
        self.image = self._render()
        self.size = self.image.get_size()
        self.dy = fall_speed

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, *self.size)
    
    def update(self):
        self.y += self.dy
        if self.y > SCR_HEIGHT:
            self.kill()
    
    def _render(self):
        card_surf = pygame.Surface((Card.FONT_SIZE*2, Card.FONT_SIZE))
        card_background = getattr(utils, self.model.color)
        card_surf.fill(card_background)
        
        font = pygame.font.Font(None, Card.FONT_SIZE)
        font_surf = font.render(str(self.model), True, utils.white, card_background)
        
        x = (card_surf.get_width()-font_surf.get_width()) / 2
        y = (card_surf.get_height()-font_surf.get_height()) / 2
        card_surf.blit(font_surf, (x, y))
        return card_surf

class Player(pygame.sprite.Sprite):
    
    def __init__(self, color, pos, player_controls):
        super(Player, self).__init__()
        self.model = models.Player_Model()
        self.x, self.y = pos
        self.dx = 3
        self.dy = 3
        self.player_controls = player_controls
        self.color = color
        self.image = self._render()
        self.size = self.image.get_size()

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y+9, 80, 1)

    def update(self, cards_captured):
        self._handle_movement()

        for card in cards_captured:
            self.model.cards.append(card.model)
            self.model.update()

    def _handle_movement(self):
        if pygame.key.get_pressed()[self.player_controls[0]]:
            self.x -= self.dx
        if pygame.key.get_pressed()[self.player_controls[1]]:
            self.x += self.dx

        if pygame.key.get_pressed()[self.player_controls[2]]:
            self.y -= self.dy
        if pygame.key.get_pressed()[self.player_controls[3]]:
            self.y += self.dy

        if self.x < -self.size[0]:
            self.x = -self.size[0]
        if self.x > SCOREBOARD_BORDER-self.size[0]:
            self.x = SCOREBOARD_BORDER-self.size[0]

        if self.y < -self.size[1]+10:
            self.y = -self.size[1]+10
        if self.y > SCR_HEIGHT-10:
            self.y = SCR_HEIGHT-10
        
    def _render(self):
        player_surf = pygame.Surface((100, 20))
        player_surf.fill(self.color, (0, 0, 10, 20))
        player_surf.fill(self.color, (10, 10, 80, 10))
        player_surf.fill(self.color, (90, 0, 10, 20))
        return player_surf



def update_scoreboard(players):
    y = 20

    score_font = pygame.font.Font(None, 20)

    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.fill(utils.white, (SCOREBOARD_BORDER, 0, 5, SCR_HEIGHT))
    for i, p in enumerate(players):
        score_surf = score_font.render(
            "Player %s" % (i+1), True, p.color)
        SCREEN.blit(score_surf, (SCOREBOARD_BORDER+10, y))

        y += 20
        score_surf = score_font.render(
            "Score: %s" % p.model.score, True, p.color)
        SCREEN.blit(score_surf, (SCOREBOARD_BORDER+10, y))

        y += 40
        score_surf = score_font.render(
            "Current Cards:", True, p.color)
        SCREEN.blit(score_surf, (SCOREBOARD_BORDER+10, y))

        y += 20
        for j, c_m in enumerate(p.model.cards):
            c = Card(c_m.num, c_m.color, c_m.sym, (0, 0), 0)
            SCREEN.blit(c.image, (SCOREBOARD_BORDER+10, y+j*50))
            
        y += 100

    rect = pygame.Rect(SCOREBOARD_BORDER, 0, SCR_WIDTH-SCOREBOARD_BORDER, SCR_HEIGHT)
    return rect

def main():

    p1 = Player(utils.yellow, (100, 450), (K_LEFT, K_RIGHT, K_UP, K_DOWN))
    p2 = Player(utils.cyan, (200, 450), (K_a, K_d, K_w, K_s))
    
    player_group = pygame.sprite.OrderedUpdates()
    card_group = pygame.sprite.RenderUpdates()

    player_group.add(p1, p2)
    
    clock = pygame.time.Clock()
    while True:
        dirty_rects = []
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        chance_ball = random.randrange(100)
        if chance_ball == 0:
            c = Card(random.choice(models.Card_Model.NUMBERS),
                     random.choice(models.Card_Model.COLORS),
                     random.choice(models.Card_Model.SYMBOLS),
                     (random.randint(100, 300), -50), random.randint(1, 4))
            card_group.add(c)
        
        card_group.update()
        
        for p in player_group:
            cards_captured = pygame.sprite.spritecollide(p, card_group, True)
            p.update(cards_captured)

        dirty_rects.append(update_scoreboard(player_group))
        
        player_group.clear(SCREEN, BACKGROUND)
        card_group.clear(SCREEN, BACKGROUND)
        dirty_rects.extend(player_group.draw(SCREEN))
        dirty_rects.extend(card_group.draw(SCREEN))
        pygame.display.update(dirty_rects)

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
