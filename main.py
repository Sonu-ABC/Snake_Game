import pygame
import time
import random
from pygame.locals import *


SIZE=40
BACKGROUND_COLOR = (110, 110, 5)  # Define a background color for the game

class Apple:
  def __init__(self, parent_screen):
    self.parent_screen = parent_screen
    self.image = pygame.image.load("resources/apple.jpg").convert()
    self.x = SIZE * 3
    self.y = SIZE * 3
    
  def draw(self):
    self.parent_screen.blit(self.image, (self.x, self.y))  # Draw the apple on the screen
    pygame.display.flip()  # Update the display
    
  def move(self):
    self.x = random.randint(1,24)*SIZE  # Reset apple position
    self.y = random.randint(1,14)*SIZE  # Reset apple position
    # Redraw the apple at the new position


class Snake:
  def __init__(self, parent_screen):
    self.length=1
    self.parent_screen = parent_screen
    self.image=pygame.image.load("resources/block.jpg").convert()
    self.x=[SIZE]
    self.y=[SIZE]
    self.direction = 'down'  # Initial direction of the snake
  
  def move_left(self):
    self.direction = 'left'  # Update direction

  def move_right(self):
    self.direction = 'right'  # Update direction

  def move_up(self):
   self.direction = 'up'  # Update direction

  def move_down(self):
    self.direction = 'down'  # Update direction

  def increase_length(self):
    self.length += 1  # Increase the length of the snake
    self.x.append(-1)  # Add a new block at the end
    self.y.append(-1)  # Add a new block at the end





  def draw(self):
    # Clear the surface

    for i in range(self.length):
       self.parent_screen.blit(self.image, (self.x[i], self.y[i]))  # Draw each block of the snake
    pygame.display.flip()  # Update the display

  def walk(self):

    for i in range(self.length-1, 0, -1):
        self.x[i] = self.x[i-1]
        self.y[i] = self.y[i-1] # Move each block to the position of the previous block

    if self.direction == 'left':
        self.x[0] -= SIZE
    elif self.direction == 'right':
        self.x[0] += SIZE
    elif self.direction == 'up':
        self.y[0] -= SIZE
    elif self.direction == 'down':
        self.y[0] += SIZE

    self.draw()  # Redraw the snake after moving


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        #self.surface.fill((110, 110, 5))
        self.snake=Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
       

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg").convert()
        self.surface.blit(bg, (0, 0))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()  # Display the score on the screen
        pygame.display.flip()  # Update the display

        # Check for collision between snake and apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()# Add a new block to the snake
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision occurred"  # Raise an exception if the snake collides with itself
                

            
          
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.snake.length - 1}', True, (255, 255, 255))
        self.surface.blit(score, (10, 10))


    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)  # Clear the surface with the background color
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game Over! Your score is {self.snake.length - 1}', True, (255, 255, 255))
        self.surface.blit(line1, (200, 250))
        line2 = font.render('Press Enter to play again or Escape to exit', True, (255, 255, 255))
        self.surface.blit(line2, (200, 300))
        pygame.display.flip()
       
        pygame.mixer.music.pause()



    def run(self):
        running = True
        pause=False
        while running:
            for event in pygame.event.get():
             if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                    running = False
               if event.key == K_RETURN:
                    pygame.mixer.music.unpause()
                    pause = False

               if not pause:
                if event.key == K_LEFT:
                    self.snake.move_left()

                if event.key == K_RIGHT:
                    self.snake.move_right()

                if event.key == K_UP:
                   self.snake.move_up()

                if event.key == K_DOWN:
                   self.snake.move_down()

             elif event.type == QUIT:
                    running = False

            try:
              if not pause:
                self.play()
            except Exception as e:
              self.show_game_over()
              pause = True
              self.reset()
            time.sleep(0.1)

if __name__== "__main__":

    game = Game()
    game.run()
   
