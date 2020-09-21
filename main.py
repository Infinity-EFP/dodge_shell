# version <1.3.1-beta> <pre-release>
# ==========project from github organization "Infinity-EFP"=========
# code by Infinity-Energy
# art by Felixqwq
# test by Infinity-Energy

# imports
import time
import sys
import pygame
import pygame.locals
import game_func as gf
from settings import Settings
from Steve import Steve, Health
from pygame.sprite import Group
from tnt import TNT
from launcher import *
from scoreboard import Scoreboard, CoolDown, Magic
from game_stats import GameStats
import random


def run_game(piano, frame):
    # init game
    hard = 1
    ele_time = 0
    clock = pygame.time.Clock()
    pygame.init()
    settings = Settings()
    gs = GameStats()
    gs.reset()
    if sys.platform == "win32" or sys.platform == "cygwin":
        my_font = pygame.font.SysFont("kaiti", 100)
    else:
        my_font = pygame.font.SysFont("kaitif", 100)
    tnts = Group()

    # init window
    screen = pygame.display.set_mode((settings.width, settings.height))
    screen_rect = screen.get_rect()
    icon = pygame.image.load("icon.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("dodge tnt")

    # init player
    steve = Steve(screen, skin)

    # heal instruction
    h1 = Health(screen, 1)
    h2 = Health(screen, 2)
    h3 = Health(screen, 3)
    magic = Magic(screen)
    t1 = time.time()
    start_rec = t1
    tnt_num = 0

    pygame.mouse.set_visible(False)
    heal = 3
    # main loop
    while True:
        clock.tick(frame)
        h1.update(heal)
        h2.update(heal)
        h3.update(heal)
        t2 = time.time()
        nowrec = t2
        nhard = int((nowrec + 20 - start_rec) / (20 + int(hard / 2)))
        if nhard > hard:
            hard = nhard
        tntw = int(nowrec + 70 - start_rec) / (hard * 41)
        steve_tnt = False
        r1 = 0 - hard + 1
        r2 = 10 - hard * 2
        while r2 - r1 >= 30 - hard:
            r1 += 1
        if random.randint(r1, r2) == 0:
            steve_tnt = True
        sb = Scoreboard(screen, gs, hard)
        cool_down = CoolDown(screen, steve)
        magic.prep_display(steve.magic)
        steve.speed = hard * 1.3
        if t2 - t1 > tntw:
            if tnt_num <= 3:
                tnt_num += 1
                new_tnt = TNT(screen)
                new_tnt.speed += hard * 0.6
                if steve_tnt:
                    new_tnt.rect.centerx = steve.rect.centerx
                tnts.add(new_tnt)
                t1 = t2

        func_return = gf.check_events(steve, start_rec, screen, my_font, piano, hard, ele_time)
        start_rec = func_return[0]
        ele_time = func_return[1]
        steve.update()

        tnts.update()
        gf.kick_minus(steve)
        gf.check_kick(steve, hard)
        steve.magic = gf.magic_return(steve.magic, hard)
        steve.speed = gf.speed_check(steve, hard)
        ctcsl = gf.check_tnt_c_steve(tnts, steve, heal, tnt_num, screen, gs.score, hard)
        heal = ctcsl[0]
        tnt_num = ctcsl[1]
        gs.score = ctcsl[2]
        con = gf.check_die(heal, gs.score, hard, ele_time, start_rec, nowrec)
        if con:
            run_game(pianos, frame)
        for tnt in tnts.copy():
            if tnt.rect.top >= screen_rect.bottom:
                tnt_num -= 1
                tnts.remove(tnt)
                gs.score += hard
        gf.update_screen(screen, steve, tnts, sb, h1, h2, h3, cool_down, magic)


data_for_game = launcher()
pianos = data_for_game[0]
skin = data_for_game[1]
frame = data_for_game[2]

run_game(pianos, frame)
