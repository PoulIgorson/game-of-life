import pygame

import figures

def toColor(color):
  rcolor = []
  for c in color:
    if c[-1] == ',':
      c = c[:-1]
    rcolor.append(c)
  color = int(rcolor[0]), int(rcolor[1]), int(rcolor[2])
  return color


def parser(lines: list) -> dict:
  kwargs: dict = {}
  for line in lines:
    arg = line.split()
    if len(arg) < 2:
      continue
    if arg[0][0:2] == '//':
      continue
    arg[0] = arg[0][:-1]

    if arg[0] == 'createList'\
    or arg[0] =='liveList':
      arg[1] = [int(x) for x in arg[1]]
    elif arg[0] == 'bg_color'\
    or arg[0] == 'cell_color':
      arg[1] = toColor(arg[1:])
    else:
      arg[1] = int(arg[1])

    kwargs[arg[0]] = arg[1]

  return kwargs

def draw(sc, world, size, barrier=0):
  for i in range(HEIGHT):
    for j in range(WIDTH):
      if world[i][j]:
        color = (255, 255, 255)
      else:
        color = (0, 0, 0)
      pygame.draw.rect(sc, color, (barrier + j * size, barrier + i * size, size, size))

def draw_barrier(sc, color, width):
  pygame.draw.rect(
    sc, color, (
      0, 0, WIDTH * SIZE_CELL + width, width
    )
  )
  pygame.draw.rect(
    sc, color, (
      0, 0, width, HEIGHT * SIZE_CELL + width
    )
  )
  pygame.draw.rect(
    sc, color, (
      0, HEIGHT * SIZE_CELL + width,
      WIDTH * SIZE_CELL + width * 2,
      width
    )
  )
  pygame.draw.rect(
    sc, color, (
      WIDTH * SIZE_CELL + width, 0, 
      width,
      HEIGHT * SIZE_CELL + width * 2
    )
  )


SIZE_CELL = 5
wSIZE = wWIDTH, wHEIGHT = 520, 570

pygame.init()
screen = pygame.display.set_mode(wSIZE)
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Calibri', 35)


first_run = 1
pause = False
pause_draw = font.render('PAUSE', 1, (255, 255, 255))


'''
0 - void
1 - cell
'''
while True:
  if not pause:
    with open('dinamic_values.txt', 'r') as f:
      lines = f.readlines()
      
      args = parser(lines)

      WIDTH = args['WIDTH']
      HEIGHT = args['HEIGHT']
      SIZE = WIDTH, HEIGHT

      FPS = args['FPS']

      createList = args['createList']
      liveList = args['liveList']

      SIZE_CELL = args['SIZE_CELL']

      bg_color = args['bg_color']

      proc_random = args['random_field_proc']
  
    if first_run:
      world: list = []
      for i in range(HEIGHT):
        world.append([0]*WIDTH)
      #world = figures.randomfield(world, 10)
      first_run = 0
  
    for i in range(HEIGHT, len(world)):
      world[i] = [0] * WIDTH
  
    for i in range(HEIGHT):
      for j in range(WIDTH, len(world[0])):
        world[i][j] = 0
  
    hidden: list = []
    for i in range(HEIGHT):
      hidden.append([0]*WIDTH)
    for i in range(HEIGHT):
      for j in range(WIDTH):
        opp = 0
        opp += (world[i - 1][j - 1] == 1)
        opp += (world[i - 1][j - 0] == 1)
        opp += (world[i - 1][(j + 1) % WIDTH] == 1)

        opp += (world[i - 0][j - 1] == 1)
        opp += (world[i + 0][(j + 1) % WIDTH] == 1)

        opp += (world[(i + 1) % HEIGHT][j - 1] == 1)
        opp += (world[(i + 1) % HEIGHT][j + 0] == 1)
        opp += (world[(i + 1) % HEIGHT][(j + 1) % WIDTH] == 1)

        if world[i][j] == 0 and opp in createList or\
            world[i][j] == 1 and opp in liveList:
          hidden[i][j] = 1
        else:
          hidden[i][j] = 0

    for i in range(HEIGHT):
      for j in range(WIDTH):
        world[i][j] = hidden[i][j]
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
     
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_p:
        pause = not pause

      if event.key == pygame.K_r:
        figures.randomfield(world, proc_random)
      
      if event.key == pygame.K_c:
        figures.randomfield(world, 0)

    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      x = pos[0] // SIZE_CELL
      y = pos[1] // SIZE_CELL

      if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        world[y][x] = int(not(world[y][x]))

  screen.fill((0, 0, 0))
  draw_barrier(screen, (200, 179, 207), 5)
  draw(screen, world, SIZE_CELL, 5)
  
  if pause:
    screen.blit(pause_draw, (30, wHEIGHT - 50))

  pygame.display.flip()
  clock.tick(FPS)
  