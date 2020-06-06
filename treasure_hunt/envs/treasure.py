import pygame
import math
import random
import time

screen_width = 400 # Med=600 Hard=500
screen_height = 400 # Med=400 Hard=800

class Player:
    def __init__(self, ai_player_file, map_file):
        self.map = pygame.image.load(map_file)
        self.player = pygame.image.load(ai_player_file)
        self.pos = [0, 0]
        self.speed_x = 1
        self.speed_y = 1
        self.proximity = 0
        self.alive = True

    def is_player(self):
        return True

    def set_speed(self, x, speed):
        if x:
            self.speed_x = speed
        else:
            self.speed_y = speed

    def set_position(self, pos):
        self.pos = pos

    def set_proximity(self, target):
        self.proximity = int(math.sqrt(math.pow((target.pos[0] - self.pos[0]), 2) + math.pow((target.pos[1] - self.pos[1]), 2)))

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
                self.pos[0] = 1
            else:
                self.pos[0] = 479 
            x_bound = True
        if self.pos[1] <= 0 or self.pos[1] >= 780: # Check for y boundaries of game, top and bottom sides
            if self.pos[1] <= 0:
                self.pos[1] = 1
            else:
                self.pos[1] = 779
            y_bound = True
        for i in range(21):
            if (self.pos[1] + i >= 0 and self.pos[1] + i <= 780) and not x_bound and ((self.map.get_at((self.pos[0], self.pos[1] + i)) == (0,0,0)) or (self.map.get_at((self.pos[0] + 20, self.pos[1] + i)) == (0,0,0))):
                x_bound = True
                self.alive = False
            if (self.pos[0] + i >= 0 and self.pos[0] + i <= 480) and not y_bound and ((self.map.get_at((self.pos[0] + i, self.pos[1])) == (0,0,0)) or (self.map.get_at((self.pos[0] + i, self.pos[1] + 20)) == (0,0,0))):
                y_bound = True
                self.alive = False

        if x_direction != 0 and not x_bound:
            self.pos[0] += x_direction * self.speed_x
        if y_direction and not y_bound:
            self.pos[1] += y_direction * self.speed_y

    '''
    Calculates distance up to 10 in a certain direction, returns the length of next object and what type of object
    Parameter: direction = string of cardinal direction in acronym form i.e. "N", "SE", "W", etc.
    Return: [distance, object_type]
        object_type: 
            0 = no object
            1 = black borders
            2 = enemy
            3 = treasure
    '''
    def cardinal(self, direction):
        center = [self.pos[0]+10, self.pos[1]+10]
        offset = []
        length = 0  # diagonal lengths will be longer, since a length of 10 would be 7 pixels along the diagonal, so must set differently based on given direction
        if direction == "N":
            offset = [0, -10]
            length = 100
        elif direction == "NE":
            offset = [10, -10]
            length = 70
        elif direction == "E":
            offset = [10, 0]
            length = 100
        elif direction == "SE":
            offset = [10, 10]
            length = 70
        elif direction == "S":
            offset = [0, 10]
            length = 100
        elif direction == "SW":
            offset = [-10, 10]
            length = 70
        elif direction == "W":
            offset = [-10, 0]
            length = 100
        elif direction == "NW":
            offset = [-10, -10]
            length = 70

        x = center[0] + offset[0]
        y = center[1] + offset[1]
        length = min(499 - x, x - 0, 799 - y, y - 0, length)
        # print(min(499 - x, x - 0, 799 - y, y - 0, length), direction, x, y)
        return (offset, length, x, y)
    '''
    Represents the distance of the next object in the 8 Cardinal Directions, max distance is 10
    0 means no object at any length up to 10 in a given direction; all other integers(1,...,10) means
    that there exists an object at that distance
    '''
    def surroundings(self):
        env = [] #surrounding environment
        for direction in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
            env.append(self.cardinal(direction))
        return env


class Enemy(Player):
    def __init__(self, enemy_player_file):
        self.enemy = pygame.image.load(enemy_player_file)
        self.pos = [0, 0]
        self.speed_x = 1
        self.speed_y = 1
    
    def is_player(self):
        return False

    '''
    Determines if object (player) has reached the enemy by checking if the positions of both overlap somewhere
    '''
    def found(self, obj=None, pixel=None):
        if obj != None:
            pos = obj.pos
        elif pixel != None:
            pos = pixel
        else:
            pos = [0, 0]
        if (abs(self.pos[0] - pos[0]) < 20) and (abs(self.pos[1] - pos[1]) < 20):
            return True
        return False


class Treasure:
    def __init__(self, treasure_player_file):
        self.treasure = pygame.image.load(treasure_player_file)
        self.pos = [0, 0]

    def set_position(self, pos):
        self.pos = pos

    '''
    Determines if object (player) has reached the treasure by checking if the positions of both overlap somewhere
    '''
    def found(self, obj=None, pixel=None):
        if obj != None:
            pos = obj.pos
        elif pixel != None:
            pos = pixel
        else:
            pos = [0, 0]
        if ((abs(self.pos[0] - pos[0]) < 20) or (abs(pos[0] - self.pos[0]) < 40)) and ((abs(self.pos[1] - pos[1]) < 20) or (abs(pos[1] - self.pos[1]) < 40)):
            if (obj != None) and obj.is_player():
                obj.proximity = 0
            return True
        return False

class TreasureHunt:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.game_speed = 1000
        self.player = Player('AIplayer.png', 'map_easy.png')
        self.enemy = Enemy('Enemy.png')
        self.treasure = Treasure('treasure.png')
        # self.set_positions() randomizes positions of player, enemy, and treasure
        self.player.set_position([20, 10])
        self.enemy.set_position([20, 360])
        self.treasure.set_position([150, 340])
        self.player.set_proximity(self.treasure)
        self.og_relative = self.player.proximity
        self.best_prox = self.player.proximity

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
                    if self.player.map.get_at((x+w, y+h)) == (0,0,0):
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
            if self.treasure.found(self.player):
                self.treasure.set_position(self.find_positions(True)) # new treasure position since its current is shared with AI's position
            elif self.treasure.found(self.enemy):
                self.treasure.set_position(self.find_positions(True)) # new treasure position since its current is shared with Enemy's position
            else:
                taken = False


    def action(self, val):
        x = y = 0
        if val == 0:
            x = -1
        elif val == 1:
            x = 1
        elif val == 2:
            y = -1
        elif val == 3:
            y = 1
        self.player.update(x, y)

    def evaluate(self):
        reward = 0
        self.player.set_proximity(self.treasure)
        if not self.player.alive:
            reward = -10000 + (5000 - self.player.proximity)
        elif self.enemy.found(self.player):
            reward = -20000
        elif self.treasure.found(self.player):
            reward = 10000
        else:
            temp = self.best_prox
            if self.player.proximity > self.best_prox:
                reward = -5
            elif self.player.proximity < self.best_prox:
                self.best_prox = self.player.proximity
        return reward

    def observe(self):
        local = []
        for check in self.player.surroundings():
            offset = check[0]
            length = check[1]
            x = check[2]
            y = check[3]
            obj_found = False
            for i in range(1, length+1): 
                scale_x = offset[0] // 10
                scale_y = offset[1] // 10
                pix = (x + (i * scale_x), y + (i * scale_y))
                if self.player.map.get_at(pix) == (0, 0, 0): # black border
                    local.append(1)
                    obj_found = True
                    break
                # elif self.enemy.found(pixel=pix): # enemy
                #     local.append(2)
                #     obj_found = True
                #     break
                # elif self.treasure.found(pixel=pix): #treasure
                #     local.append(1)
                #     obj_found = True
                #     break
            if not obj_found:
                local.append(0)
        return local

    def view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()
                quit()

        self.screen.blit(self.player.map, [0, 0])
        self.screen.blit(self.treasure.treasure, self.get_positions(self.treasure))
        self.screen.blit(self.player.player, self.get_positions(self.player))
        self.screen.blit(self.enemy.enemy, self.get_positions(self.enemy))

        pygame.display.update()

        pygame.display.flip()
        self.clock.tick(self.game_speed)

    def end(self):
        if not self.player.alive or self.treasure.found(self.player) or  self.enemy.found(self.player):
            return True
        return False 


# pygame.init()
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Treasure Hunt AI")
# map = pygame.image.load('map.png')
# TH = TreasureHunt()
# TH.set_positions()
# alive = TH.player.alive
# active = True
# while alive and active:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             active = False
#             pygame.quit()
#             quit()

#     screen.blit(TH.player.map, [0, 0])
#     screen.blit(TH.treasure.treasure, TH.get_positions(TH.treasure))
#     screen.blit(TH.player.player, TH.get_positions(TH.player))
#     screen.blit(TH.enemy.enemy, TH.get_positions(TH.enemy))
#     TH.player.update(1, 1)
#     print(TH.player.surroundings())
#     alive = TH.player.alive
#     time.sleep(.01)
    
#     pygame.display.update()

# print(TH.enemy.enemy.get_at((0,0)))
# print(TH.treasure.treasure.get_at((0,0)))