import pygame
import math
import random
import time

screen_width = 500
screen_height = 800
# check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Player:
    def __init__(self, ai_player_file, map_file):
        self.map = pygame.image.load(map_file)
        self.player = pygame.image.load(ai_player_file)
        self.pos = [0, 0]
        self.speed_x = 1
        self.speed_y = 1
        self.alive = True

    def set_speed(self, x, speed):
        if x:
            self.speed_x = speed
        else:
            self.speed_y = speed

    def set_position(self, pos):
        self.pos = pos

    def proximity(self, target):
        return math.sqrt(math.pow((target.pos[0] - self.pos[0]), 2) + math.pow((target.pos[1] - self.pos[1]), 2))

    def treasure(self):
        # if position of player is same as treasure, treasure should return true
        return False

    ''' 
    Parameters are int values (typically: -1, 0, or 1), determining the movement in either direction
    x_direction:
        0 = No change
        -1 = left
        1 = right
    y_direction:
        0 = No change
        -1 = up
        1 = down
    '''
    def update(self, x_direction, y_direction):
        x_bound = False
        y_bound = False
        if self.pos[0] <= 0 or self.pos[0] >= 480: # Check for x boundaries of game, left and right sides
            if self.pos[0] <= 0:
                self.pos[0] = 0
            else:
                self.pos[0] = 480 
            x_bound = True
        if self.pos[1] <= 0 or self.pos[1] >= 780: # Check for y boundaries of game, top and bottom sides
            if self.pos[1] <= 0:
                self.pos[1] = 0
            else:
                self.pos[1] = 780
            y_bound = True
        for i in range(21):
            if (self.pos[1] + i >= 0 and self.pos[1] + i <= 780) and not x_bound and ((map.get_at((self.pos[0], self.pos[1] + i)) == (0,0,0)) or (map.get_at((self.pos[0] + 20, self.pos[1] + i)) == (0,0,0))):
                x_bound = True
                self.alive = False
            if (self.pos[0] + i >= 0 and self.pos[0] + i <= 480) and not y_bound and ((map.get_at((self.pos[0] + i, self.pos[1])) == (0,0,0)) or (map.get_at((self.pos[0] + i, self.pos[1] + 20)) == (0,0,0))):
                y_bound = True
                self.alive = False

        if x_direction != 0 and not x_bound:
            self.pos[0] += x_direction * self.speed_x
        if y_direction and not y_bound:
            self.pos[1] += y_direction * self.speed_y



class Enemy(Player):
    def __init__(self, enemy_player_file):
        self.enemy = pygame.image.load(enemy_player_file)
        self.pos = [0, 0]
        self.speed_x = 1
        self.speed_y = 1

class Treasure:
    def __init__(self, treasure_player_file):
        self.treasure = pygame.image.load(treasure_player_file)
        self.pos = [0, 0]

    def set_position(self, pos):
        self.pos = pos

    
class TreasureHunt:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        self.player = Player('AIplayer.png', 'map.png')
        self.enemy = Enemy('Enemy.png')
        self.treasure = Treasure('treasure.png')

    def get_positions(self, obj):
        return obj.pos

    def find_positions(self, treasure):
        if treasure:
            width = 40
            height = 40
        else:
            width = 20
            height = 20
        pos = [0, 0]
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
                pos = [x, y]
                found = True
        return pos

    def set_positions(self):
        self.player.set_position(self.find_positions(False)) # AI positions
        self.enemy.set_position(self.find_positions(False)) # Enemy Position
        taken = True
        while taken:
            if (abs(self.enemy.pos[0] - self.player.pos[0]) < 20) and (abs(self.enemy.pos[1] - self.player.pos[1]) < 20):
                self.enemy.set_position(self.find_positions(False)) # new enemy position since its current is shared with AI's position
            else:
                taken = False
        self.treasure.set_position(self.find_positions(True)) # Treasure Position
        taken = True
        while taken:
            if ((abs(self.treasure.pos[0] - self.player.pos[0]) < 20) or (abs(self.player.pos[0] - self.treasure.pos[0]) < 40)) and ((abs(self.treasure.pos[1] - self.player.pos[1]) < 20) or (abs(self.player.pos[1] - self.treasure.pos[1]) < 40)):
                self.treasure.set_position(self.find_positions(True)) # new treasure position since its current is shared with AI's position
            elif ((abs(self.treasure.pos[0] - self.enemy.pos[0]) < 20) or (abs(self.enemy.pos[0] - self.treasure.pos[0]) < 40)) and ((abs(self.treasure.pos[1] - self.enemy.pos[1]) < 20) or (abs(self.enemy.pos[1] - self.treasure.pos[1]) < 40)):
                self.treasure.set_position(self.find_positions(True)) # new treasure position since its current is shared with Enemy's position
            else:
                taken = False


    def action(self, action_x, action_y):
        x = y = 0
        if action_x == 0:
            x = -1
        elif action_x == 1:
            x = 1
        if action_y == 0:
            y = -1
        elif action_y == 1:
            y = 1
        self.player.update(x, y)

    def evaluate(self):
        reward = 0
        if not self.player.alive:
            reward = -10000 + (1000 * (1/(self.player.proximity + 1)))
        elif self.player.treasure:
            reward = 100
        return reward

    def is_done(self):
        if not self.player.alive or self.player.treasure:
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


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Treasure Hunt AI")
map = pygame.image.load('map.png')
TH = TreasureHunt()
TH.set_positions()
alive = TH.player.alive
active = True
while alive and active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            pygame.quit()
            quit()

    screen.blit(TH.player.map, [0, 0])
    screen.blit(TH.treasure.treasure, TH.get_positions(TH.treasure))
    screen.blit(TH.player.player, TH.get_positions(TH.player))
    screen.blit(TH.enemy.enemy, TH.get_positions(TH.enemy))
    TH.player.update(1, 1)
    TH.enemy.update(1, 0)
    alive = TH.player.alive
    time.sleep(.01)
    
    pygame.display.update()

print(TH.player.proximity(TH.treasure))