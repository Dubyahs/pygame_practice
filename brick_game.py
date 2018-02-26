import pygame
import math
import sys

#Constants
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 728
FPS = 60

WHITE = (255 ,255 ,255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

GAME_LIVES = 2
PAD_WIDTH = 128
PAD_HEIGHT = 32
PAD_SPEED = 10
BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_SPEED = 5
BRICK_WIDTH = 70
BRICK_HEIGHT = 30


#window
pygame.init()
game_window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Brick Game")
clock = pygame.time.Clock()

#graphics
pad_x = (DISPLAY_WIDTH * 0.5) - (PAD_WIDTH * 0.5)
pad_y = (DISPLAY_HEIGHT * 0.9) - (PAD_HEIGHT * 0.5)
pad_rect = pygame.Rect(pad_x, pad_y, PAD_WIDTH, PAD_HEIGHT)
ball_x = (DISPLAY_WIDTH * 0.5) - (BALL_WIDTH * 0.5)
ball_y = (DISPLAY_HEIGHT * 0.8) - (BALL_HEIGHT * 0.5)
ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)

class Pad:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PAD_WIDTH
        self.h = PAD_HEIGHT
        self.left = False
        self.right = False
        self.surface = pygame.Surface((PAD_WIDTH, PAD_HEIGHT))
    def reset(self):
        self.x = (DISPLAY_WIDTH * 0.5) - (PAD_WIDTH * 0.5)
        self.y = (DISPLAY_HEIGHT * 0.9) - (PAD_HEIGHT * 0.5)
    def draw(self):
        pygame.draw.rect(game_window, BLUE, pygame.Rect(self.x, self.y, self.w, self.h))

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BALL_WIDTH
        self.h = BALL_HEIGHT
        self.speed = BALL_SPEED
        self.direction = 90
    def reset(self):
        self.x = (DISPLAY_WIDTH / 2 - BALL_WIDTH)
        self.y = (DISPLAY_HEIGHT * 0.8)
        self.direction = 90
    def bounce(self, diff):
        self.direction = (360 - self.direction) % 360
        self.direction -= diff
    def draw(self):
        pygame.draw.rect(game_window, GREEN, pygame.Rect(self.x, self.y, self.w, self.h))

class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BRICK_WIDTH
        self.h = BRICK_HEIGHT
        self.visible = True
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(game_window, BLACK, self.rect, 5)
        pygame.Surface.fill(game_window, RED, self.rect)

class Game:
    def __init__(self):
        self.reset_game()
        self.lives = GAME_LIVES
        
    def reset_game(self):
        self.pad = Pad((DISPLAY_WIDTH * 0.5) - (PAD_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.9) - (PAD_HEIGHT * 0.5))
        self.ball = Ball((DISPLAY_WIDTH * 0.5 - BALL_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.85 - BALL_HEIGHT * 0.5))
        brick_x = 0
        brick_y = 0
        self.bricks = []
        for i in range(0,61):
            self.bricks.append(Brick(brick_x, brick_y))
            brick_x += BRICK_WIDTH
            if i % 15 == 0 and i != 0:
                brick_y += BRICK_HEIGHT
                brick_x = 0
    def check_collision(self, a, b):
        x_collision = True
        y_collision = True
        if (a.x > (b.x + b.w)) or ((a.x + a.w) < b.x):
            x_collision = False
        if (a.y > (b.y + b.h)) or ((a.y + a.h) < b.y):
            y_collision = False
        return (x_collision and y_collision)
        
#game
game = Game()
game.reset_game()

        
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.pad.left = True
            if event.key == pygame.K_RIGHT:
                game.pad.right = True

        if event.type == pygame.KEYUP:
            if game.pad.left and event.key == pygame.K_LEFT:
                game.pad.left = False
            if game.pad.right and event.key == pygame.K_RIGHT:
                game.pad.right = False


def redraw():
    game_window.fill(WHITE)
    for i in range(0, len(game.bricks)):
        if game.bricks[i].visible == True:
            game.bricks[i].draw()
    if game.pad.left == True and game.pad.x >= 0:
        game.pad.x += -PAD_SPEED
    elif game.pad.right == True and game.pad.x <= DISPLAY_WIDTH - PAD_WIDTH:
        game.pad.x += PAD_SPEED
    game.pad.draw()

    #ball physics
    game.ball.draw()
    game.direction_radians = math.radians(game.ball.direction)
    game.ball.x += game.ball.speed * math.cos(game.direction_radians)
    game.ball.y += game.ball.speed * math.sin(game.direction_radians)

    if game.ball.y <= 0:
        game.ball.direction = (360 - game.ball.direction) % 360
    elif game.ball.y > DISPLAY_HEIGHT - game.ball.h:
        #game.ball.direction = (360 - game.ball.direction) % 360
        if game.lives == 0:
            game.reset_game()
        else:
            game.ball.reset()
            game.pad.reset()
            game.lives -= 1
    elif game.ball.x <= 0:
        game.ball.direction = (180 - game.ball.direction) % 360  
    elif game.ball.x > DISPLAY_WIDTH - game.ball.w:
        game.ball.direction = (180 - game.ball.direction) % 360
    elif game.check_collision(game.pad, game.ball):
        game.ball.direction = (360 - game.ball.direction) % 360
    else:
        for i in range(0, len(game.bricks)):
            if game.check_collision(game.bricks[i], game.ball) and game.bricks[i].visible == True:
                game.ball.diff = ((game.bricks[i].x + game.bricks[i].w) / 2) - ((game.ball.x + game.ball.w) / 2)
                game.ball.bounce(game.ball.diff)
                    
                game.bricks[i].visible = False
    
    pygame.display.update()
    

#game loop
exited = False
while not exited:
    clock.tick(FPS)
    redraw()
    handle_events()

    
