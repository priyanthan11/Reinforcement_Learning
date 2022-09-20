import pygame  # For window
import random  # randome generation
from enum import Enum
from collections import namedtuple

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

    def _Place_Food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._Place_Food()

    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  # if user press a key
                if event.key == pygame.K_a:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_w:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # 2. Move
        self._move(self.direction)  # should update head
        self.snake.insert(0, self.head)

        # 3. Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. Place new Food or just move
        if self.head == self.food:
            self.score += 1
            self._Place_Food()
        else:
            self.snake.pop()

        # 5. Update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6 return game over and score

        return game_over, self.score

    def _is_collision(self):
        # hits Boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hit itself
        if self.head in self.snake[1:]:
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

        # break if game over
    print('Final Score ', score)
    pygame.quit()
