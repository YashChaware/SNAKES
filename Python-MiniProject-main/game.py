import pygame
import random
import button
from pygame import mixer
from database_manager import dm;


def run_game(username):
    snake_size = 20
    img_size = (snake_size+5, snake_size+5)

    #music
    mixer.init()
    mixer.music.load('music/bag2.mp3')
    mixer.music.load('music/bag3.mp3')
    pygame.init()

    # Colors
    white = (255, 255, 255)
    red = (255, 0, 0)
    black = (153, 76, 0)
    snakegreen = (130, 76, 0)
    grass = (102, 255, 102)
    scc =(0, 90, 90)

    fps = 60
    global direction;
    direction = "right"
    global highscore;
    highscore = dm.get_user_highscore(username);
    
    # Creating window
    screen_width = 900
    screen_height = 600
    gameWindow = pygame.display.set_mode((screen_width, screen_height))

    #images
    bg = pygame.image.load("img/bg.jpg")
    bg = pygame.transform.scale(bg, (screen_width, screen_height)).convert_alpha()

    bg1 = pygame.image.load("img/bg2.png")
    bg1 = pygame.transform.scale(bg1, (screen_width, screen_height)).convert_alpha()

    bg2 = pygame.image.load("img/bg3.jpg")
    bg2 = pygame.transform.scale(bg2, (screen_width, screen_height)).convert_alpha()

    outro = pygame.image.load("img/outro.png")
    outro = pygame.transform.scale(outro, (screen_width, screen_height)).convert_alpha()

    intro = pygame.image.load("img/intro.jpg")
    intro = pygame.transform.scale(intro, (screen_width, screen_height)).convert_alpha()

    pau = pygame.image.load("img/pause-button.png")
    pau = pygame.transform.scale(pau, (screen_width, screen_height)).convert_alpha()

    def get_random_food_image():
        foood = ['img/apple.png', 'img/df.png', 'img/grapes.png', 'img/grapes (1).png', 'img/kiwi.png', 'img/orange.png']
        fod1 = pygame.image.load(random.choice(foood))
        return pygame.transform.scale(fod1, (snake_size + 5, snake_size + 5)).convert_alpha()

    snhed = pygame.image.load('img/snkhd1.png')
    snhed = pygame.transform.rotate(snhed, 180)
    snhed = pygame.transform.scale(snhed, (snake_size+7, snake_size-2)).convert_alpha()

    start_img = pygame.image.load('img/start_btn.png').convert_alpha()

    #create button instances
    start_button = button.Button(350, 350, start_img, 0.8)
    # Game Title
    pygame.display.set_caption("yash games")
    icon = pygame.image.load('img/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.update()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)
    def pause_game():
        paused = True
        gameWindow.blit(pau, (0, 0))
        while paused:
            mixer.music.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    dm.update_user_highscore(username, highscore);
                    dm.close_database();
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dm.update_user_highscore(username, highscore);
                        dm.close_database();
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_SPACE:
                        paused = False
                        mixer.music.unpause()
            pygame.display.update()
            clock.tick(fps)

    def display_score(text, color, x, y):
        screen_text = font.render(text, True, color)
        gameWindow.blit(screen_text, [x, y])


    def draw_snake( gameWindow, color, snk_list, snake_size):

        if direction == "right":
            hed = snhed
        if direction == "left":
            hed = pygame.transform.rotate(snhed, 180)
        if direction == "up":
            hed = pygame.transform.rotate(snhed, 90)
        if direction == "down":
            hed = pygame.transform.rotate(snhed, 270)

        for x, y in snk_list:
            pygame.draw.ellipse(gameWindow, color, [x, y, snake_size, snake_size])
            gameWindow.blit(hed, (snk_list[-1]))

    #show_welcome_screen gameWindow
    def show_welcome_screen():
        exit_game = False
        while not exit_game:
            gameWindow.blit(intro, (0, 0))
            if start_button.draw(gameWindow):
                mixer.music.load('music/bag.mp3')
                mixer.music.play(-1)
                gameloop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            exit_game = True
                            dm.update_user_highscore(username, highscore);
                            dm.close_database();
                    if event.key == pygame.K_RETURN:
                        mixer.music.load('music/bag.mp3')
                        mixer.music.play(-1)
                        gameloop()

            pygame.display.update()
            clock.tick(60)

    # Game Loop
    def gameloop():
        global direction;
        global highscore;
        # Game specific variables
        exit_game = False
        game_over = False
        snake_x = 45
        snake_y = 55
        velocity_x = 0
        velocity_y = 0
        snk_list = []
        snk_length = 1
    # Check if highscore file exist
        # if(not os.path.exists("highscore.txt")):
        #     with open("highscore.txt", "w") as f:
        #         f.write("0")

        # with open("highscore.txt", "r") as f:
        #     highscore = f.read()

        food_x = random.randint(20, screen_width / 2)
        food_y = random.randint(20, screen_height / 2)
        score = 0
        init_velocity = 4
        epoch = -1
        while not exit_game:
            epoch = epoch + 1
            if game_over:
                direction = "right"
                if score > highscore:
                    highscore = score
                # with open("highscore.txt", "w") as f:
                #     f.write(str(highscore))
                gameWindow.blit(outro, (0, 0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dm.update_user_highscore(username, highscore);
                        dm.close_database();
                        exit_game = True
                display_score("Score: " + str(score), scc, 380, 385)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                        dm.update_user_highscore(username, highscore);
                        dm.close_database();

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            dm.update_user_highscore(username, highscore);
                            show_welcome_screen()
            else:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            if direction == "left": break;
                            direction = "right"
                            velocity_x = init_velocity
                            velocity_y = 0

                        if event.key == pygame.K_LEFT:
                            if direction == "right": break;
                            direction = "left"
                            velocity_x = - init_velocity
                            velocity_y = 0

                        if event.key == pygame.K_UP:
                            if direction == "down": break;
                            direction = "up"
                            velocity_y = - init_velocity
                            velocity_x = 0

                        if event.key == pygame.K_DOWN:
                            if direction == "up": break;
                            direction = "down"
                            velocity_y = init_velocity
                            velocity_x = 0
                        if event.key == pygame.K_q:
                            score += 10
                        if event.key == pygame.K_r:
                            highscore = 0
                        if event.key == pygame.K_KP1:
                            if init_velocity == 1:
                                init_velocity = init_velocity
                            else:
                                init_velocity = init_velocity-1
                        if event.key == pygame.K_KP2:
                            init_velocity = init_velocity+1
                        if event.key == pygame.K_1:
                            mixer.music.load('music/bag1.mp3')
                            mixer.music.play(-1)
                        if event.key == pygame.K_2:
                            mixer.music.load('music/bag2.mp3')
                            mixer.music.play(-1)
                        if event.key == pygame.K_3:
                            mixer.music.load('music/bag3.mp3')
                            mixer.music.play(-1)
                        if event.key == pygame.K_4:
                            mixer.music.load('music/bag.mp3')
                            mixer.music.play(-1)
                        if event.key == pygame.K_5:
                            mixer.music.load('music/bag4.mp3')
                            mixer.music.play(-1)
                        if event.key == pygame.K_ESCAPE:
                            exit_game = True
                        if event.key == pygame.K_KP0:
                            mixer.music.pause()
                        if event.key == pygame.K_KP_PERIOD:
                            mixer.music.unpause()
                        if event.key == pygame.K_SPACE:
                            pause_game()

                snake_x = snake_x + velocity_x
                snake_y = snake_y + velocity_y
                snake_rect = pygame.Rect(snake_x, snake_y, snake_size, snake_size)
                food_rect = pygame.Rect(food_x, food_y, snake_size + 5, snake_size + 5)
                if epoch ==0:
                    fod1 = get_random_food_image()
                if snake_rect.colliderect(food_rect):
                    eat = mixer.Sound('music/eat.mp3')
                    eat.play()
                    score += 10
                    # get_random_food_image()
                    fod1 = get_random_food_image()
                    food_x = random.randint(20, screen_width / 2)
                    food_y = random.randint(20, screen_height / 2)
                    snk_length += 5
                    if score == highscore:
                        h = mixer.Sound('music/hc.mp3')
                        h.play()
                        
                if score > 190:
                    gameWindow.blit(bg1, (0, 0))
                    display_score(f"Score:{score}   highscore:{highscore}", red, 5, 5)
                    gameWindow.blit(fod1, (food_x, food_y))
                if score > 290:
                    gameWindow.blit(bg, (0, 0))
                    display_score(f"Score:{score}   highscore:{highscore}", red, 5, 5)
                    gameWindow.blit(fod1, (food_x, food_y))
                if score > 390:
                    gameWindow.blit(bg2, (0, 0))
                    display_score(f"Score:{score}   highscore:{highscore}", red, 5, 5)
                    gameWindow.blit(fod1, (food_x, food_y))
                else:
                    gameWindow.blit(bg, (0, 0))
                    display_score(f"Score:{score}   highscore:{highscore}", red, 5, 5)
                    gameWindow.blit(fod1, (food_x, food_y))

                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)

                if len(snk_list) > snk_length:
                    del snk_list[0]

                if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load('music/gm.mp3')
                    pygame.mixer.music.play()

                if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                    game_over = True
                    pygame.mixer.music.load('music/gm.mp3')
                    pygame.mixer.music.play()

                if score > 190:
                    draw_snake(gameWindow, snakegreen, snk_list, snake_size)
                else:
                    draw_snake(gameWindow, black, snk_list, snake_size)
            pygame.display.update()
            clock.tick(fps)
        pygame.quit()
        quit()
    show_welcome_screen()
