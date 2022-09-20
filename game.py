import pygame  # For window
import random  # randome generation
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()  # start initialiazation
font = pygame.font.Font('AGENCYR.TTF', 25)  # define font

# reset

# reward

# play(action) -> direction

# game_iteration

# is_collision


class Direction(Enum):  # enum for movement
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')  # 2D Vector
# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20  # Size of the single block. means a single part of squre of snake or food
SPEED = 10  # speed of the game


class SnakeGameAI:  # the game class
    def __init__(self, w=640, h=480):  # w means wide and h means height
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode(
            (self.w, self.h))  # asign the display
        pygame.display.set_caption('Snake')  # title of the game
        self.clock = pygame.time.Clock()  # set Tick
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT  # at start snake will go right side

        self.head = Point(self.w/2, self.h/2)  # initialize snake head size

        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]  # snake body 1st head 2nd head with moved 40 unit from heand 3rd moved 40*2 times from head

        self.score = 0  # score is set to 0 while game starts
        self.food = None
        self._Place_Food()  # place food on random place
        self.frame_iteration = 0

    def _Place_Food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._Place_Food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move
        self._move(action)  # should update head
        self.snake.insert(0, self.head)

        # 3. Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Place new Food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._Place_Food()
        else:
            self.snake.pop()

        # 5. Update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6 return game over and score

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits Boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > pt - BLOCK_SIZE or pt.y < 0:
            return True
        # hit itself
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(
                pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # This is automate movement based on clock wise direction move

        #[stright, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN,
                      Direction.LEFT, Direction.UP]  # setting a clocl wise direction for movement
        # getting the index from the clock wise list
        idx = clock_wise.index(self.direction)
        # first 0 th element (Direction.Right)

        # asigning the direction with action
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d-> l -> u
        else:  # [0,0,1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u-> l -> d

        self .direction = new_dir

        x = self.head.x
        y = self.head.y

        if self .direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self .direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self .direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self .direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
