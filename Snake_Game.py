import pygame
import random
import os

pygame.mixer.init()

clock = pygame.time.Clock()
fps = 60

pygame.init()

# screen size
s_width = 900
s_height = 600

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Sounds
gameover_aud = pygame.mixer.Sound('gameover.mp3')
foodeat = pygame.mixer.Sound('foodeat.mp3')

# creating game channels
pygame.mixer.set_num_channels(1)
go = pygame.mixer.Channel(0)

gameWindow = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Snakes")

# background image
bkgpic = pygame.image.load('bkgpic.jpg')
bkgpic = pygame.transform.scale(bkgpic, (s_width, s_height)).convert_alpha()

# menu image
menupic = pygame.image.load('menupic1.jpg')
menupic = pygame.transform.scale(menupic, (s_width, s_height)).convert_alpha()

# printing score on game window
highscore_x = 700
highscore_y = 10
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 50)


def printtext(text, color, x, y, type):
    if type == 0:
        score_text = font.render(text, True, color)
        gameWindow.blit(score_text, [x, y])
    else:
        message = font2.render(text, True, color)
        gameWindow.blit(message, [x, y])


def drawSnake(gameWindow, green, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, green, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    global clock, fps, go
    while not exit_game:
        gameWindow.blit(menupic, (0, 0))
        printtext('Snakes', green, 370, 215, 1)
        printtext('Press space', green, 50, 550, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if go.get_busy():
                        go.stop()
                    pygame.mixer.music.load("bkg.mp3")
                    pygame.mixer.music.play()
                    gameLoop()
                if event.key == pygame.K_ESCAPE:
                    quit()
        pygame.display.update()
        clock.tick(fps)


def gameLoop():
    global clock, fps, foodeat, gameover_aud, go

    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write(str(0))
    with open('highscore.txt', 'r') as f:
        highscore = f.read()

    score = 0
    score_x = 10
    score_y = 10
    exit_game = False
    game_over = False
    speed = 4
    snake_x = 50
    snake_y = 50
    snake_size = 15
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, s_width - 60)
    food_y = random.randint(0, s_height - 60)
    food_size = 15
    snk_len = 1
    snk_list = []
    while not exit_game:
        if game_over:
            with open('highscore.txt', 'w') as f:
                f.write(str(highscore))
            printtext('Game Over! press enter to continue', red, 160, 260, 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                    if event.key == pygame.K_ESCAPE:
                        quit()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                # event and actions
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = speed
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -speed
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -speed
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = speed
                        velocity_x = 0
                    elif event.key == pygame.K_TAB:
                        score += 5  # cheat code
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(foodeat)
                pygame.mixer.music.unpause()
                score += 10
                if score > int(highscore):
                    highscore = score
                snk_len += 5
                food_x = random.randint(0, s_width - 60)
                food_y = random.randint(0, s_height - 60)
                pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            gameWindow.blit(bkgpic, (0, 0))
            printtext("Score:" + str(score), green, score_x, score_y, 0)
            printtext("Top Score: " + str(highscore), green, highscore_x, highscore_y, 0)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_len:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.stop()
                go.play(gameover_aud)
                game_over = True

            if snake_x < 0 or snake_x > s_width or snake_y < 0 or snake_y > s_height:
                pygame.mixer.music.stop()
                go.play(gameover_aud)
                game_over = True

            drawSnake(gameWindow, green, snk_list, snake_size)

        # Update display screen with most recent changes
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()
