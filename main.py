import pygame
import random

pygame.init()
pygame.font.init()

WIDTH = 630
HEIGHT = 640
FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# may need to compress assets
BG = pygame.transform.scale(pygame.image.load("Assets/bg.png"),
                            (WIDTH, HEIGHT))

pipes = []
score = 0
highScore = 0

class Player:

  def __init__(self):
    self.x = 50
    self.y = 20
    self.original_image = pygame.image.load("Assets/bird.png")
    self.img = self.original_image
    self.mask = pygame.mask.from_surface(self.img)
    self.velocity = 0.0
    self.gravity = 0.5
    self.angle = 0
    self.minAngle = -45
    self.maxAngle = 30

  def draw(self):
    WINDOW.blit(self.img, (self.x, self.y))

  def move(self):
    self.y += self.velocity
    self.velocity += self.gravity
    if self.angle > self.minAngle and self.velocity > 0.0:
      self.angle -= 1
      self.img = pygame.transform.rotate(self.original_image, self.angle)
      self.mask = pygame.mask.from_surface(self.img)
    elif self.angle < self.maxAngle and self.velocity < 0.0:
      self.angle += 1 * -self.velocity
      self.img = pygame.transform.rotate(self.original_image, self.angle)
      self.mask = pygame.mask.from_surface(self.img)


class Pipes:
  gap = 125

  class Pipe:
    def __init__(self, y, img):
      self.x = WIDTH
      self.y = y
      self.img = img
      self.mask = pygame.mask.from_surface(self.img)

  def __init__(self):
    self.bottom = self.Pipe(
        random.randint(100, 600),
        pygame.transform.scale(pygame.image.load("Assets/pipe.png"), 
                               (100, 600)))
    self.top = self.Pipe(self.bottom.y - self.gap - self.bottom.img.get_height(),
          pygame.transform.rotate(
          pygame.transform.scale(pygame.image.load("Assets/pipe.png"), (100, 600)), 180))
    self.scored = False

  def draw(self):
    WINDOW.blit(self.bottom.img, (self.bottom.x, self.bottom.y))
    WINDOW.blit(self.top.img, (self.top.x, self.top.y))

  def move(self):
    self.bottom.x -= 2
    self.top.x -= 2
    if self.bottom.x < -100:
      pipes.remove(self)
    if self.bottom.x <= 50 and not self.scored:
      global score
      score += 1
      self.scored = True


def run_game():
  run = True
  clock = pygame.time.Clock()

  player = Player()
  pipe_timer = 0

  gameOver = False
  global score
  score = 0

  score_font = pygame.font.SysFont("impact", 200)
  gameOver_font = pygame.font.SysFont("impact", 150)
  
  gameOver_label = gameOver_font.render("Game Over", 1, (255, 0, 0))

  def redraw_window():
    WINDOW.blit(BG, (0, 0))
    for pipe in pipes:
      pipe.draw()
    player.draw()

    score_label = score_font.render(str(score), 1, (255, 255, 0))
    WINDOW.blit(score_label, (WIDTH/2 - score_label.get_width()/2, 50))

    if gameOver:
      WINDOW.blit(gameOver_label, (WIDTH/2 - gameOver_label.get_width()/2, HEIGHT/2 - 
                                   gameOver_label.get_height()/2))
    
    pygame.display.update()

  def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

  while run:
    global highScore
    clock.tick(FPS)
    redraw_window()

    keys = pygame.key.get_pressed()

    if gameOver is True:
      '''
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
        pipes.clear()
        run_game()
      elif keys[pygame.K_q]:
        main_menu()
      '''
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            pipes.clear()
            run_game()
          elif event.key == pygame.K_q:
            pipes.clear()
            return
      if player.y < HEIGHT - player.img.get_height():
        player.move()
      continue

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      elif event.type == pygame.KEYDOWN and player.y > 0:
        player.velocity = -6

    if player.y > HEIGHT - player.img.get_height():
      if score > highScore:
        highScore = score
        save_data.write(str(highScore))
        save_data.truncate()
      gameOver = True

    if pipe_timer == 0:
      pipes.append(Pipes())
      pipe_timer = 2.5 * FPS
    else:
      pipe_timer -= 1
    
    player.move()
    for pipe in pipes:
      if collide(pipe.bottom, player) or collide(pipe.top, player):
        if score > highScore:
          highScore = score
          save_data.write(str(highScore))
          save_data.truncate()
        gameOver = True
      pipe.move()

  pygame.quit()

def main_menu():
  timer = 0
  clock = pygame.time.Clock()
  running = True
  global highScore
  while running:
    if timer < 300:
      timer += 1
      continue
    clock.tick(FPS)
    WINDOW.blit(BG, (0, 0))
    
    title_font = pygame.font.SysFont("impact", 120)
    title_label = title_font.render("Flappy Bird", 1, (255, 255, 0))
    title_rect = title_label.get_rect(center=(WIDTH/2, 
                                              HEIGHT/2 - title_label.get_height()/2 - 120))
    WINDOW.blit(title_label, title_rect)
    highScore_label = title_font.render(str(highScore), 1, (255, 255, 0))
    highScore_rect = highScore_label.get_rect(center=(WIDTH/2, 
                                              HEIGHT/2 - title_label.get_height()/2 + 200))
    WINDOW.blit(highScore_label, highScore_rect)
    ctrl_font = pygame.font.SysFont("impact", 70)
    ctrl_label = ctrl_font.render("[space] to start", 1, (255, 0, 255))
    ctrl_rect = ctrl_label.get_rect(center = (WIDTH/2, HEIGHT/2 - ctrl_label.get_height()/2 + 20))
    WINDOW.blit(ctrl_label, ctrl_rect)

    keys =  pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
      return
    '''
    elif keys[pygame.K_q]:
      running = False
    '''

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    pygame.display.update()
  
  pygame.quit()

while True:
  save_data = open("save_data.txt", "r+")
  hs = save_data.read()

  if hs == '':
    highScore = 0
    save_data.write('0')
  else:
    highScore = int(hs)

  save_data.seek(0)
  
  main_menu()
  run_game()
