import pygame
import random
import math

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
done = False

circle_x = 30
circle_y = 30

image_width = 150
image_height = 150

speed = 1.5

image_circle = pygame.image.load("Uryi.png")
image_circle = pygame.transform.scale(image_circle, (150, 150))

image_coin = pygame.image.load("nurik.png")

coin_width = 120
coin_height = 120

image_coin = pygame.transform.scale(image_coin, (coin_width, coin_height))

coin_x = random.randint(0, 1280 - coin_width)
coin_y = random.randint(0, 720 - coin_height)

image_bomb = pygame.image.load("egor.png")


bomb_width = 120
bomb_height = 120

image_bomb = pygame.transform.scale(image_bomb, (bomb_width, bomb_height))

bomb_x = random.randint(0, 1280 - bomb_width)
bomb_y = random.randint(0, 720 - bomb_height)



background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (1280, 720))

score = 0

font = pygame.font.SysFont('Arial', 30)

sound_bomb = pygame.mixer.Sound("gameover.wav")
sound_coin = pygame.mixer.Sound("sound1.wav")

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def generate_safe_bomb_position():
    global bomb_x, bomb_y, circle_x, circle_y
    while True:
        bomb_x = random.randint(0, 1280 - bomb_width)
        bomb_y = random.randint(0, 720 - bomb_height)
        if distance(bomb_x, bomb_y, circle_x, circle_y) > 300:  
            break

def generate_safe_coin_position():
    global coin_x, coin_y, bomb_x, bomb_y
    while True:
        coin_x = random.randint(0, 1280 - coin_width)
        coin_y = random.randint(0, 720 - coin_height)
        if distance(bomb_x, bomb_y, coin_x, coin_y) > 300:
            break

def reset_game():
    global circle_x, circle_y, coin_x, coin_y, bomb_x, bomb_y, score
    circle_x = 30
    circle_y = 30
    coin_x = random.randint(0, 1280 - coin_width)
    coin_y = random.randint(0, 720 - coin_height)
    bomb_x = random.randint(0, 1280 - bomb_width)
    bomb_y = random.randint(0, 720 - bomb_height)
    score = 0


reset_game()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w] and circle_y > 0: circle_y -= speed

    if pressed[pygame.K_s] and  circle_y < 720 - image_height: circle_y += speed

    if pressed[pygame.K_a] and circle_x > 0: circle_x -= speed

    if pressed[pygame.K_d] and circle_x < 1280 - image_width: circle_x += speed

    if (circle_x < coin_x + coin_width and
        circle_x + image_width > coin_x and
        circle_y < coin_y + coin_height and
        circle_y + image_height > coin_y):

        coin_x = random.randint(0, 1280 - coin_width)
        coin_y = random.randint(0, 720 - coin_height)

        score += 1

        bomb_x = random.randint(0, 1280 - coin_width)
        bomb_y = random.randint(0, 720 - coin_height)

        generate_safe_bomb_position()
        generate_safe_coin_position()

        sound_coin.play()

    if (circle_x < bomb_x + bomb_width and
        circle_x + image_width > bomb_x and
        circle_y < bomb_y + bomb_height and
        circle_y + image_height > bomb_y):

        sound_bomb.play()

        reset_game()


    screen.blit(background, (0, 0))
    screen.blit(image_bomb, (bomb_x, bomb_y))
    screen.blit(image_coin, (coin_x, coin_y))
    screen.blit(image_circle, (circle_x, circle_y))

    score_text = font.render(F'Очки: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
