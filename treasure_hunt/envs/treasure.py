import pygame
import math
import random

screen_width = 500
screen_height = 800
# check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Player:
    def __init__(self, ai_player_file, map_file):
        self.map = pygame.image.load(map_file)
        self.player = pygame.image.load(ai_player_file)
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.pos = (0, 0)
        self.speed = 10
        self.direction

    def is_alive(self):
        return True

    def set_speed(self, speed):
        self.speed = speed

    def set_position(self, pos):
        self.pos = pos

    def proximity(self):
        pass

    def treasure(self):
        # if position of player is same as treasure, treasure should return true
        return False

    def update(self):
        pass


class Enemy(Player):
    def __init__(self, enemy_player_file):
        self.enemy = pygame.image.load(enemy_player_file)
        self.pos = (0,0)
        self.speed = 10

class Treasure:
    def __init__(self, treasure_player_file):
        self.treasure = pygame.image.load(treasure_player_file)
        self.pos = (0, 0)

    def set_position(self, pos):
        self.pos = pos

    
class TreasureHunt:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.clock()
        self.game_speed = 60
        self.player = Player('AIplayer.png', 'map.png')
        self.enemy = Enemy('Enemy.png')
        self.treasure = Treasure('treasure.png')

    def find_positions(self, treasure):
        if treasure:
            width = 40
            height = 40
        else:
            width = 20
            height = 20
        pos = (0,0)
        found = False
        while not found:
            x = random.randint(0, 500 - width)
            y = random.randint(0, 800 - height)
            open = True
            for w in range(width):
                for h in range(height):
                    if map.get_at((x+w, y+h)) == (0,0,0):
                        open = False
            if open:
                pos = (x, y)
                found = True
            return pos

    def set_positions(self):
        self.player.set_position(self.find_positions(False)) # AI positions
        self.enemy.set_position(self.find_positions(False)) # Enemy Position
        self.treasure.set_position(self.find_positions(True)) # Treasure Position

    def action(self, action):
        if action == 0:
            self.player.direction = 90
        if action == 1:
            self.player.direction += -90

        self.player.update()

    def evaluate(self):
        reward = 0
        if not self.player.is_alive:
            reward = -10000 + self.player.proximity
        elif self.player.treasure:
            reward = 100
        return reward

    def is_done(self):
        if not self.player.is_alive or self.player.treasure:
            self.player.current_check = 0
            self.player.distance = 0
            return True
        return False

    def observe(self):
        pass

    def view(self):
        
        self.screen.blit(self.player.map, (0, 0))
        self.screen.fill((0, 0, 0))

        pygame.display.flip()
        self.clock.tick(self.game_speed)

    def end(self):
        pass


def get_distance(p1, p2):
    return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Treasure Hunt AI")
map = pygame.image.load('map.png')
active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            pygame.quit()
            quit()

    screen.blit(map, (0,0))
    screen.blit(pygame.image.load('AIplayer.png'), (13, 476))
    screen.blit(pygame.image.load('enemy.png'), (473,273))
    screen.blit(pygame.image.load('treasure.png'), (459,633))
    
    pygame.display.update()