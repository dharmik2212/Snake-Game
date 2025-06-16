import pygame
import random
import warnings
import os


pygame.init()
pygame.mixer.init()


# creating window


gameWindow = pygame.display.set_mode((800, 500))
pygame.display.set_caption("My Game")
pygame.display.update()
bgimag = pygame.image.load("snake.jpg")
bgimag = pygame.transform.scale(bgimag, (800, 500)).convert_alpha()
gameWindow.blit(bgimag, (0, 0))
pygame.display.update()

gameOverimag = pygame.image.load("gameover.png")
gameOverimag = pygame.transform.scale(gameOverimag, (800, 500)).convert_alpha()
gameWindow.blit(gameOverimag, (0, 0))
pygame.display.update()

frontImag = pygame.image.load("playsnake.png")
frontImag = pygame.transform.scale(frontImag, (800, 500)).convert_alpha()
gameWindow.blit(frontImag, (0, 0))
pygame.display.update()



clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30, False, True)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")


def screen_text(text, color, x, y):
    text_screen = font.render(text, True, color)
    gameWindow.blit(text_screen, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome_screen():
    exit_game = False
    game_over = False
    while not exit_game:

        gameWindow.fill(white)
        gameWindow.blit(frontImag, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                  exit_game = True


def game_loop():
    # game specific variables

    snake_x = 45
    snake_y = 45
    snake_size = 10
    snake_speed = 1
    food_x = random.randint(20, 400)
    food_y = random.randint(20, 250)
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_len = 1
    snake_list = []
    exit_game = False
    game_over = False
    high_score = 0   
    
        
    try:
        with open("highscore.txt", "r") as f:
                high_score = int(f.read())
    except (FileNotFoundError, ValueError):
        # If file doesn't exist or is empty/corrupt, start with 0
        high_score = 0
        with open("highscore.txt", "w") as f:
                f.write("0")
        

    while not exit_game:

        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            gameWindow.fill(white)
            gameWindow.blit(gameOverimag, (0, 0))

            # screen_text("game over!",red,250,200)
            # screen_text("press enter to play again",red,250,250q)
            # screen_text("press q to quit",red,250,300)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit_game = True
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        # welcome_screen()
                        game_loop()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = 10
                        velocity_y = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:

                        velocity_x = -10
                        velocity_y = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y = -10
                        velocity_x = 0

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y = 10
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 1
                
                food_x = random.randint(20, 400)
                food_y = random.randint(20, 250)
                snake_len += 1

            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as f:
                    f.write(str(high_score))
                
            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_len:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("destroysound.mp3")
                pygame.mixer.music.play()
               

            if snake_x < 0 or snake_x > 800 or snake_y < 0 or snake_y > 500:
                game_over = True
                pygame.mixer.music.load("destroysound.mp3")
                pygame.mixer.music.play()
                

            gameWindow.fill((124, 252, 0))
            if bgimag:
                gameWindow.blit(bgimag, (0, 0))
            screen_text("Score: " + str(score * 10), red, 5, 5)
            screen_text("High Score: " + str(high_score * 10), red, 5, 25)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            plot_snake(gameWindow, black, snake_list, snake_size)
            pygame.display.update()
            clock.tick(15)

    pygame.quit()
    quit()


welcome_screen()
game_loop()
