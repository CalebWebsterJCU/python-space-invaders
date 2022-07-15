import pygame
from pygame import mixer

""" Settings """

# Player Settings
PLAYER_SPEED = 0.5
BULLET_SPEED_NORMAL = 1.5
BULLET_SPEED_OVERCHARGE = 5
OVERCHARGE_FILL_RATE = 5000  # (lower is faster)
OVERCHARGE_DRAIN_RATE = 1000

# Enemy Settings
NUMBER_OF_ENEMIES = 56
ENEMY_STARTING_LIVES = 2
ENEMY_Y_SPEED = 0.01  # Default: 0.01
ENEMY_X_SPEED = 0.1
ENEMY_X_TRAVEL = 50

# Music / Sound
MUSIC_ON = True
SOUNDS_ON = True
""" Setup """

# Initialize Pygame
pygame.init()

# Set number of sound channels
pygame.mixer.set_num_channels(3)

# Fonts
FONT = pygame.font.Font('darkpoestry.ttf', 25)
TITLE_FONT = pygame.font.Font('darkpoestry.ttf', 85)
BUTTON_FONT = pygame.font.Font('darkpoestry.ttf', 50)
SMALL_FONT = pygame.font.Font('darkpoestry.ttf', 15)

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Title and Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Icons/logo.png')
pygame.display.set_icon(icon)


def display_score_value(x, y, value):
    score = FONT.render('Score: ' + str(value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def display_overcharge(x, y, state):
    state_message = FONT.render('Overcharge:   ' + state, True, (255, 255, 255))
    screen.blit(state_message, (x, y))


def display_overcharge_bar(x, y, amount):
    charge_bar = "*" * amount
    charge_message = FONT.render(charge_bar, True, (255, 255, 255))
    screen.blit(charge_message, (x, y))


def player(player_image, x, y):  # draws the player character
    screen.blit(player_image, (int(x), int(y)))


def enemy(x, y, image):  # draws the enemy character
    screen.blit(image, (int(x), int(y)))


def fire_bullet(bullet_image, x, y):
    screen.blit(bullet_image, (int(x) + 16, int(y) + 10))
    if SOUNDS_ON:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sounds/laser.wav'))


def is_collision(b_x, b_y, e_x, e_y):
    if (e_x - 16) <= (b_x + 12) <= (e_x + 32):
        if e_y <= b_y <= (e_y + 32):
            return True


def view_scores(scores):
    scores.sort()
    scores.reverse()
    click = False
    view_scores_active = True

    button_2 = pygame.Rect(450, 300, 250, 150)

    scores_title_text = TITLE_FONT.render("SCORES", True, (255, 255, 255))
    button2_text = BUTTON_FONT.render("MENU", True, (0, 0, 0))

    while view_scores_active:
        score_y = 150
        score_x = 35
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (255, 255, 255), button_2)

        screen.blit(scores_title_text, (25, 25))
        screen.blit(button2_text, (500, 350))

        for score in scores:
            score_text = FONT.render(str(score), True, (255, 255, 255))
            screen.blit(score_text, (score_x, score_y))
            score_y += 35
            if (scores.index(score) + 1) % 12 == 0 and scores.index(score) != 0:
                score_x += len(str(score)) + 75
                score_y = 150

        if button_2.collidepoint(mx, my):
            if click:
                view_scores_active = False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                view_scores_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    view_scores_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def game_over(score):
    click = False
    game_over_active = True

    button_1 = pygame.Rect(100 + 170, 300, 250, 150)

    game_over_text = TITLE_FONT.render("Game Over", True, (255, 0, 0))
    button1_text = BUTTON_FONT.render("MENU", True, (0, 0, 0))
    score = FONT.render(f"Score: {score}", True, (255, 255, 255))

    while game_over_active:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (255, 255, 255), button_1)

        screen.blit(game_over_text, (185, 85))
        screen.blit(score, (353, 220))
        screen.blit(button1_text, (330, 350))

        if button_1.collidepoint(mx, my):
            if click:
                game_over_active = False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def main_menu():
    scores = [0]
    click = False
    menu_is_active = True

    button_1 = pygame.Rect(100, 300, 250, 150)
    button_2 = pygame.Rect(450, 300, 250, 150)

    title = TITLE_FONT.render("Space Invaders", True, (255, 255, 255))
    button1_text = BUTTON_FONT.render("PLAY", True, (0, 0, 0))
    button2_text = BUTTON_FONT.render("SCORES", True, (0, 0, 0))
    creator_text = SMALL_FONT.render("A game by Caleb Webster", True, (255, 255, 255))
    date_text = SMALL_FONT.render("Completed on 09/06/2020", True, (255, 255, 255))

    while menu_is_active:
        high_score = FONT.render(f"High Score: {max(scores)}", True, (255, 255, 255))

        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(title, (85, 85))

        mx, my = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (255, 255, 255), button_1)
        pygame.draw.rect(screen, (255, 255, 255), button_2)

        screen.blit(high_score, (327, 220))
        screen.blit(button1_text, (160, 350))
        screen.blit(button2_text, (500, 350))
        screen.blit(creator_text, (5, 580))
        screen.blit(date_text, (598, 580))

        if button_1.collidepoint(mx, my):
            if click:
                score = game()
                scores.append(score)
        if button_2.collidepoint(mx, my):
            if click:
                view_scores(scores)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_is_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_is_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def game():

    score = 0

    # Background Music
    if MUSIC_ON:
        mixer.music.load('Sounds/background.wav')
        mixer.music.play(-1)

    # Player
    player_image = pygame.image.load('Icons/player_2.png')
    player_x = 368
    player_y = 480
    player_movement = 0

    # Enemies
    enemy_images = []
    enemy_x = []
    enemy_y = []
    enemy_lives = []
    x_value = 28
    y_value = -50

    for i in range(NUMBER_OF_ENEMIES):

        enemy_images.append(pygame.image.load('Icons/enemy_2.png'))
        enemy_x.append(x_value)
        enemy_y.append(y_value)
        enemy_lives.append(ENEMY_STARTING_LIVES)
        x_value += 95
        if (i + 1) % 8 == 0:
            x_value = 28
            y_value -= 100

    enemy_x_change = ENEMY_X_SPEED

    # Bullet
    bullet_image = pygame.image.load('Icons/bullet_1.png')
    bullet_x = player_x + 4
    bullet_y = player_y

    # Game Loop
    is_running = True
    moving_left = False
    moving_right = False
    is_firing = False
    overcharge = False
    bullet_is_travelling = False
    bullet_has_collided = False
    times_moved_x = 0
    number_of_times_run = 1
    overcharge_amount = 0

    while is_running:

        screen.fill((255, 255, 255))  # fill  the screen with RGB colour

        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():  # check all events that are happening
            if event.type == pygame.QUIT:  # check for quit event (pressing "x" button)
                is_running = False
                break

            """ Key Detection """

            if event.type == pygame.KEYDOWN:  # check for any key pressed
                if event.key == pygame.K_LEFT:  # left
                    player_movement = -PLAYER_SPEED
                    moving_left = True
                if event.key == pygame.K_RIGHT:  # right
                    player_movement = PLAYER_SPEED
                    moving_right = True
                if event.key == pygame.K_SPACE:  # space
                    if not is_firing:
                        is_firing = True
                        if not bullet_is_travelling:
                            bullet_x = player_x + 4
                        bullet_is_travelling = True
                if event.key == pygame.K_z:  # Z
                    if not overcharge and overcharge_amount > 0:
                        overcharge = True
                    else:
                        overcharge = False
                if event.key == pygame.K_ESCAPE:  # ESC
                    is_running = False

            if event.type == pygame.KEYUP:  # check for any key released
                if event.key == pygame.K_LEFT:
                    moving_left = False
                    if moving_right:
                        player_movement = PLAYER_SPEED
                    else:
                        player_movement = 0
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                    if moving_left:
                        player_movement = -PLAYER_SPEED
                    else:
                        player_movement = 0
                if event.key == pygame.K_SPACE:
                    is_firing = False

        """ Game Mechanics """

        # Player Movement
        player(player_image, player_x, player_y)
        player_x += player_movement

        if player_x <= 0 and player_movement < 0:
            player_movement = 0
        elif player_x >= 736 and player_movement > 0:
            player_movement = 0

        # Enemy Mechanics

        # Enemy Boundaries
        times_moved_x += 1
        if times_moved_x == ENEMY_X_TRAVEL / ENEMY_X_SPEED:
            enemy_x_change = -enemy_x_change
            times_moved_x = 0

        for i in range(NUMBER_OF_ENEMIES):
            enemy(enemy_x[i], enemy_y[i], enemy_images[i])
            enemy_x[i] += enemy_x_change
            enemy_y[i] += ENEMY_Y_SPEED

            # Collision Detection
            if bullet_is_travelling and not bullet_has_collided:
                if is_collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i]):
                    bullet_has_collided = True
                    enemy_lives[i] -= 1
                    if enemy_lives[i] == 0:
                        if SOUNDS_ON:
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/explosion.wav'))
                        score += 1
                        enemy_y[i] = enemy_y[i] - 700
                        enemy_lives[i] = 2

            # Game Over
            if enemy_y[i] > 480:
                is_running = False

        # Bullet Mechanics
        if bullet_is_travelling:
            if overcharge:
                bullet_speed = BULLET_SPEED_OVERCHARGE
            else:
                bullet_speed = BULLET_SPEED_NORMAL
            if not bullet_has_collided:
                fire_bullet(bullet_image, bullet_x, bullet_y)
            bullet_y -= bullet_speed
            if bullet_y < -24:
                bullet_y = 480
                bullet_x = player_x + 4
                bullet_is_travelling = False
                bullet_has_collided = False
                if is_firing:
                    bullet_is_travelling = True

        # Display score overcharge state and charge bar.
        if overcharge:
            overcharge_state = "ON"
        else:
            overcharge_state = "OFF"
        display_score_value(10, 10, score)
        display_overcharge(578, 10, overcharge_state)
        display_overcharge_bar(578, 50, overcharge_amount)

        # Drain or fill overcharge bar.
        if overcharge and overcharge_amount > 0 and is_firing:
            if number_of_times_run % OVERCHARGE_DRAIN_RATE == 0:
                overcharge_amount -= 1
        if not overcharge and overcharge_amount < 20:
            if number_of_times_run % OVERCHARGE_FILL_RATE == 0:
                overcharge_amount += 1

        # Turn overcharge off when amount reaches 0.
        if overcharge_amount == 0:
            overcharge = False

        number_of_times_run += 1

        pygame.display.update()
    mixer.music.stop()
    game_over(score)
    return score


main_menu()
print("Game Closed")
