import pygame as pg
import numpy as np
import random
from enum import Enum
from collections import namedtuple
pg.init()
font = pg.font.Font(pg.font.get_default_font(), 24)
# credit goes to https://github.com/vedantgoswami/SnakeGameAI/blob/main/snake_game.py
# I didn't want to just copy and paste without understanding, but it ended up being a copy anyhow

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
 
Point = namedtuple('Point','x , y')

BLOCK_SIZE=20
SPEED = 20
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

class SnakeGame:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        # initialise display
        self.display = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

        # initialise game state
        self.direction = Direction.RIGHT
        self.head = Point(self.width/2, self.height/2)
        self.snake = [
            self.head,
            Point(self.head.x-BLOCK_SIZE, self.head.y)
        ]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if (self.food in self.snake):
            self._place_food()#smart
    
    def play_step(self):
        # 1. collect user input
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
                quit()
            if(event.type == pg.KEYDOWN):
                if(event.key == pg.K_LEFT):
                    self.direction = Direction.LEFT
                elif(event.key == pg.K_RIGHT):
                    self.direction = Direction.RIGHT
                elif(event.key == pg.K_UP):
                    self.direction = Direction.UP
                elif(event.key == pg.K_DOWN):
                    self.direction = Direction.DOWN
        
        # 2. Move
        self.move(self.direction)
        self.snake.insert(0,self.head)# what does this line do?

        # 3. Check if game is over
        game_over = False 
        if(self._is_collision()):
            game_over=True
            return game_over,self.score
        # 4. Place new Food or just move
        if(self.head == self.food):
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Return game Over and Display Score
        return game_over,self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        for point in self.snake:
            pg.draw.rect(self.display, BLUE1, pg.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pg.draw.rect(self.display, BLUE2, pg.Rect(point.x+4, point.y+4, 12, 12))
        pg.draw.rect(self.display,RED,pg.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, (0,0))
        pg.display.flip()

    def move(self, direction):
        x = self.head.x
        y = self.head.y
        if(direction == Direction.RIGHT):
            x+=BLOCK_SIZE
        elif(direction == Direction.LEFT):
            x-=BLOCK_SIZE
        elif(direction == Direction.DOWN):
            y+=BLOCK_SIZE
        elif(direction == Direction.UP):
            y-=BLOCK_SIZE
        self.head = Point(x,y)
    
    def _is_collision(self):
        #hit boundary
        if(self.head.x>self.width-BLOCK_SIZE or self.head.x<0 or self.head.y>self.height - BLOCK_SIZE or self.head.y<0):
            return True
        if(self.head in self.snake[1:]):
            return True
        return False
    
if __name__=="__main__":
    game = SnakeGame()

    #Game loop
    #game_over=False
    while True:
        game_over,score=game.play_step()
        if(game_over == True):
            break
    print('Final Score',score)

    pg.quit()