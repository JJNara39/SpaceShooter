import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Dimensions of the screen
WIDTH, HEIGHT = 900, 500

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
RED = (255, 0, 0)
YELLOW = (255,255,0)

# Speed of our game, ships movements, bullet speed, max of them
FPS = 60
VEL = 5
PROJ_VEL = 7
MAX_PROJ = 3

# Various Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Borders
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound('Boom.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Laser_Shoot.wav')

# Spaceship new dimensions
SHIP_WIDTH, SHIP_HEIGHT = 55, 40

# Characters, Background
YELLOW_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)
RED_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270) # we can wrap these rotates and scales together
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

def draw_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))
        
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def move_ships(red, yellow):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: 
        yellow.y += VEL
    if keys[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15:
        red.y += VEL
    if keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += PROJ_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= PROJ_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main(): 
    red = pygame.Rect(675,250, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(225,250, SHIP_WIDTH, SHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_PROJ:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_PROJ:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        move_ships(red, yellow)

        draw_win(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        

    main()

if __name__ == "__main__":
    main() # assures this cannot be called by another module


