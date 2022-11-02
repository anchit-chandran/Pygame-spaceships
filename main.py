import pygame
import os

from random import randint

pygame.init()

# INITIALISE WINDOW
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceships')

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# FONT
my_font = pygame.font.SysFont('Times New Roman',25)

# GAME VARIABLES
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SPACESHIP_START_X, SPACESHIP_START_Y = 300, 300
PLAYER_SPEED = 5
ENEMY_SPEED = 6
ENEMY_WIDTH, ENEMY_HEIGHT = SPACESHIP_WIDTH - 20, SPACESHIP_HEIGHT - 12
ENEMY_START_X, ENEMY_START_Y = 300, 0
NUM_ENEMIES = 10
LIVES = 3
LIFE_HEART_SIZE = 30, 30

# MAKE PLAYER SPACESHIP
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

# MAKE ENEMY SPACESHIP
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)), 0)

# MAKE HEART
HEART_IMAGE = pygame.image.load(os.path.join('Assets','heart.png'))
HEART = pygame.transform.rotate(pygame.transform.scale(HEART_IMAGE, (LIFE_HEART_SIZE)), 0)

# RENDER SCREEN
def draw_screen(spaceship, enemies, lives, score):
    WIN.fill(BLACK)

    # SHOW PLAYER
    WIN.blit(RED_SPACESHIP, (spaceship.x, spaceship.y))

    # GENERATE ENEMY SPACESHIPs
    for enemy in enemies:
        WIN.blit(YELLOW_SPACESHIP, (enemy.x, enemy.y))

    # GENERATE SCORE
    WIN.blit(debug_text(text=f'Score: {score}'), (10, 10))

    # GENERATE LIVES
    for life in lives:
        WIN.blit(HEART, (life.x, life.y))

    pygame.display.update()

# HANDLE DEBUG TEXT
def debug_text(font = 'Times New Roman', font_size = 25, text='Debug', text_color =(255, 0, 0), background_color = (0,255,0) ):
    return pygame.font.SysFont(font,font_size).render(text, True, text_color, background_color)

# HANDLE SPACESHIP MOVEMENT
def handle_movement(keys_pressed, spaceship):
    # UP
    if keys_pressed[pygame.K_w] and spaceship.y > 0:
        spaceship.y -= PLAYER_SPEED

    # DOWN
    if keys_pressed[pygame.K_s] and spaceship.y < HEIGHT - SPACESHIP_HEIGHT:
        spaceship.y += PLAYER_SPEED

    # LEFT
    if keys_pressed[pygame.K_a] and spaceship.x > 0:
        spaceship.x -= PLAYER_SPEED

    # RIGHT
    if keys_pressed[pygame.K_d] and spaceship.x < WIDTH - SPACESHIP_WIDTH:
        spaceship.x += PLAYER_SPEED

# HANDLE ENEMY MOVEMENT
def move_enemy(enemies, spaceship, lives, score):

    for enemy in enemies:
        # check if on screen
        if enemy.y <= HEIGHT:
            enemy.y += ENEMY_SPEED
        
        # RESET POSITION IF OFF SCREEN
        if enemy.y > HEIGHT:
            # RESET TO TOP
            enemy.y = 0 - ENEMY_WIDTH

            #RANDOMISE X COORD
            enemy.x = randint(0,WIDTH-ENEMY_WIDTH)

            # ADD TO SCORE
            score += 1
            # print(score)
    
        if pygame.Rect.colliderect(enemy, spaceship):
            tolerance = 10
            difference = enemy.bottom - spaceship.top
            if difference < tolerance:
                print(f'hit ({difference})\n\n')
                if lives:
                    lives.pop()
                else:
                    print('dead')
                

# MAKE DEATH SCREEN
def dead_screen():
    text_rect = debug_text(text='DEAD!', font_size=50).get_rect()
    WIN.blit(debug_text(text='DEAD!', font_size=50), ((WIDTH/2) - text_rect.width/2, (HEIGHT/2) - text_rect.height/2))   
    pygame.display.update()      



# MAIN LOOP
def main():

    # MAKE SPACESHIP RECT
    spaceship = pygame.Rect(
        SPACESHIP_START_X, SPACESHIP_START_Y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # MAKE ENEMY RECTS
    enemies = []
    for i in range(NUM_ENEMIES):
        enemies.append(pygame.Rect(
            randint(0, WIDTH), 
        
            ENEMY_START_Y - randint(10,500),
            ENEMY_WIDTH, 
            ENEMY_HEIGHT))

    # MAKE HEALTH BAR
    lives = []
    for i in range(LIVES):
        lives.append(
            pygame.Rect(50+i*50, 50, LIFE_HEART_SIZE[0], LIFE_HEART_SIZE[1])
        )

    # make SCORE
    score = 0
    
    # SET MAIN LOOP
    clock = pygame.time.Clock()
    run = True

    # handle events
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if lives:
            # GET OBJECT CONTAINING WHICH KEY IS PRESSED
            keys_pressed = pygame.key.get_pressed()

            # HANDLE MOVEMENT
            handle_movement(keys_pressed=keys_pressed, spaceship=spaceship)

            # MOVE ENEMY
            move_enemy(enemies=enemies, spaceship=spaceship, lives=lives, score=score)

            # RENDER SCREEN
            draw_screen(spaceship=spaceship, enemies=enemies, lives = lives, score=score)


        else:
            dead_screen()

    pygame.quit()


if __name__ == '__main__':
    main()
