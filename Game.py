import math
import random
import os
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1280, 800))

background = pygame.image.load('Cityresizeimage.jpg')

mixer.music.load("background_song.wav")

mixer.music.play(-1)

pygame.display.set_caption("Corona Invader")

icon = pygame.image.load('coronavirus.png')
pygame.display.set_icon(icon)

player_image = pygame.image.load('VaccineResized.png')
playerX = 600
playerY = 600
playerX_change = 0

enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 7

for i in range(enemies_num):
    enemy_image.append(pygame.image.load('CoronavirusResized.png'))
    enemyX.append(random.randint(0, 1225))
    enemyY.append(random.randint(45, 140))
    enemyX_change.append(4)
    enemyY_change.append(40)


bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 585
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 35)

textX = 10
textY = 10

end_font = pygame.font.Font('Organic Brand.ttf', 64)


def show_points(x, y):
    score = font.render("Points : " + str(score_value), True, (254, 0, 246))
    screen.blit(score, (x, y))

def game_over_message():
    over_text = end_font.render("£ corona won £", True, (254, 0, 246))
    screen.blit(over_text, (400, 300))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def shoot_bullet(x, y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bullet_image, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 26:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    shoot_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1225:
        playerX = 1225


    for i in range(enemies_num):

        if enemyY[i] > 560:
            for j in range(enemies_num):
                enemyY[j] = 2000
            game_over_message()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1225:
            enemyX_change[i] =-2
            enemyY[i] += enemyY_change[i]


        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 590
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1225)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 585
        bullet_state = "ready"

    if bullet_state is "fire":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_points(textX, textY)
    pygame.display.update()