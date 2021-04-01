import pygame
import random
import math
# importing music
from pygame import mixer

# Initialise the pygame otherwise the code won't work
pygame.init()

# creating the screen
# pygame: to access the methods inside the pygame module
# display.set_mode() is a method
# inside the bracket is the size of the window width = 800 and height = 600
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# background music
mixer.music.load("bensound-birthofahero.wav")
# the background music will play on a loop
mixer.music.play(-1)

# Displaying Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# loading the picture of the player
playerImg = pygame.image.load("space-invaders.png")
# these values represent the coordinates of the picture. It will be half-way closer to the bottom of the screen
# coordinate 600 is at the bottom of the screen
playerX = 370
playerY = 480
playerX_change = 0

# creating lists to hold info for multiple enemies

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # loading the picture of the enemy
    enemyImg.append(pygame.image.load("alien.png"))
    # making the coordinates of the enemy random to that it will spawn in a different location each time
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    # initialise the enemyX_change to 2 so that initially it will start moving to the right
    # if enemyX_change = 0 then the enemy won't move
    enemyX_change.append(1)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("line.png")
bulletX = 0
# the bullet will always be shot from the position of the spaceship
bulletY = 480
bulletX_change = 0
bulletY_change = 6
# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# score
score_value = 0

# creating a font
font = pygame.font.Font("Heroes Legend Hollow.ttf", 24)

textX = 10
textY = 10

# game over font
over_font = pygame.font.Font("Heroes Legend Hollow.ttf", 32)


def show_score(x, y):
    # we are rendering the text
    # at the end we are choosing a colour of the font
    score = font.render("score: " + str(score_value), True, (255, 240, 0))
    # we are drawing the text onto the screen
    screen.blit(score, (x, y))


def game_over_text():
    # displaying game over text
    over_score = over_font.render("GAME OVER", True, (255, 0, 0))
    # (200,250) is the coordinate
    screen.blit(over_score, (220, 250))


def player(x, y):
    # blit means to draw
    # we are drawing an image of our player to the screen
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    # to access a variable from outside a function you need to put global in front of it
    global bullet_state
    bullet_state = "fire"
    # The coordinats makes sure that the bullet appears in the middle and above the spaceship
    screen.blit(bulletImg, (x + 15, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # finding the distance between two points
    # the square root of (x1-x2)^2 + (y1-y2)^2
    distance = (math.sqrt(math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # if the distance between two points is < 27 then the bullet has defeated the alien
    # the number 27 has been picked by trial and error, as well just judgement
    if distance < 27:
        return True
    else:
        return False


# Game Loop
# all the events that are happening, get into pygame.event.get()
# This loop will make the window run infintely until I click the exit button
running = True
while running:
    # changing the colour of the window
    # RGB = Red, Green, Blue
    # each colour can go up to a maximum of 255
    screen.fill((9, 49, 131))
    # Background image
    # because the loop has to load the picture every iteration, the loop is running a little slower
    screen.blit(background, (0, 0))

    # anytime a player presses a button in a game, it is an event
    # every event is stored inside the pygame.event.get():
    for event in pygame.event.get():
        # when we press the x button, we are no longer running the game, therefore the window will close
        if event.type == pygame.QUIT:
            running = False
        # if a button has been pressed on the keyboard
        if event.type == pygame.KEYDOWN:
            # if it's the left arrow I will decrease the x-coordinate by 3
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            # if it's the right arrow I will increase the x-coordinate by 3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            # if you have pressed the spacebar
            if event.key == pygame.K_SPACE:
                # This if loop makes sure that the bullet can only be fired when it's state is "ready"
                if bullet_state is "ready":
                    # playing the sound when the bullet is fired
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # bulletX = playerX makes sure that the bullet doesn't follow the player the around.
                    # The x-coordinate will be where it was fired
                    # it gets the current x-coordinate of the spaceship and stores it in the variable bulletX
                    bulletX = playerX
                    # when the spacebar is pressed the fire_bullet function is called and the state of the bullet is changed
                    # to fire inside the function
                    # however the default state of the bullet is "ready
                    fire_bullet(bulletX, bulletY)
        # if the button has been released
        if event.type == pygame.KEYUP:
            # if it's either arrow
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # make sure to call player function after screen.fill method otherwise player won't appear on the screen
    # this is because the screen is drawn first and then on top the player is drawn
    # we put player into while loop so that the player doesn't disappear

    # the variable playerX (x-coordinate) will adjust according to the button I have pressed
    playerX += playerX_change

    # if the spaceship goes out of the window on the left side, it will be forced to stay in it
    # (x-coordinate cannot be <0)
    if playerX <= 0:
        playerX = 0
    # the width of the spaceship is 64x64 pixels
    # so if the spaceship goes out of the window on the right side (x-coordinate>736), the x-coordinate has to = 736
    # the spaceship cannot go beyond the window.
    elif playerX >= 736:
        playerX = 736

    # resets the bullet so that once it reaches the top of the screen it goes back to waiting with the spaceship
    # allows user to shoot multiple bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement
    # x-coordinate = same as spaceship when fired, and doesn't change as spaceship moves
    # but the y- coordinate will be 480 (bulletY) - bullletY_change (3) every iteration (it goes up)
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(num_of_enemies):
        # game over
        # when an enemy reaches the level of the spaceship on the y-axis, all the enemies will disappear from the screen.
        # the y-coordinate = 2000
        # and the screen will display game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # in each iteration of the while loop, we will either add or takeaway 0.3 to the x-coordinate (enemyX), depending on
        # which side the enemy touches
        # so it will look like the enemy is moving
        enemyX[i] += enemyX_change[i]
        # checking boundary for enemy so it doesn't go out of the window
        # instead the enemy will start moving in the opposite direction
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            # when enemy will hit the boundary it will go down by 40 pixels (enemyY_change = 40)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        # if collision == True return the bullet to the spaceship and increase the score by 1 and the enemy will respawn
        # in a different location
        # making sure the if loop occurs for all enemies
        if collision:
            # playing sound when bullet hits monster
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # running the functions that draw our characters to the window
    player(playerX, playerY)

    show_score(textX, textY)

    # if we add anything to our display window it will be updated in this while loop
    pygame.display.update()
