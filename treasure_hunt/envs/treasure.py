import pygame
import math
import random

screen_width = 1200
screen_height = 1500
# check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Player:
    def __init__(self, ai_player_file, map_file, pos):
        self.map = pygame.image.load(map_file)
        self.player = pygame.image.load(ai_player_file)
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.pos = pos
        self.speed = 10

    def set_speed(self, speed):
        self.speed = speed


class Enemy(Player):
    def __init__(self, enemy_player_file, pos):
        self.enemy = pygame.image.load(enemy_player_file)
        self.pos = pos


class Treasure:
    def __init__(self, treasure_player_file, pos):
        self.treasure = pygame.image.load(treasure_player_file)
        self.pos = pos


class TreasureHunt:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.clock()
        self.open_positions = []
        self.player = Player('AIplayer.png', 'map.png', self.open_positions[random.randint(0, len(self.open_positions))])
        self.enemy = Enemy('Enemy.png', self.open_positions[random.randint(0, len(self.open_positions))])

    def set_open_positions(self):
        pass


def get_distance(p1, p2):
    return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))
