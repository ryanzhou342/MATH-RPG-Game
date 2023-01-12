import pygame
import sys
import os
import random
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = ("0, 25")


def main():
    """
    Main Program
    """
    # Sets a clock
    fps = 30
    fpsClock = pygame.time.Clock()

    # Initializes screen depending on resolution of monitor
    info_object = pygame.display.Info()
    screen_width = info_object.current_w
    screen_height = info_object.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("MATH GAME")

    # Loads fonts
    title_font = pygame.font.Font("NewRocker-Regular.otf", 100)
    medium_font = pygame.font.Font("NewRocker-Regular.otf", 40)
    small_font = pygame.font.Font("NewRocker-Regular.otf", 30)
    info_font = pygame.font.Font("NewRocker-Regular.otf", 24)
    
    # Loads image
    title_background = pygame.image.load("img/dungeon.jpg").convert()
    main_background = pygame.image.load("img/dungeon1.jpg").convert()
    text_box = pygame.image.load("img/text_box.jpg").convert()
    playerImg = pygame.transform.rotate(pygame.image.load("img/shortsword.png"), 180)
    enemy1 = pygame.image.load("img/monster1.png")
    enemy2 = pygame.image.load("img/monster2.png")
    enemy3 = pygame.image.load("img/monster3.png")
    enemy4 = pygame.image.load("img/monster4.png")
    enemy5 = pygame.image.load("img/monster5.png")
    boss1 = pygame.image.load("img/boss1.png")
    
    # Initial variables
    location = "title"
    enemy_list = [enemy1, enemy2, enemy3, enemy4, enemy5]
    floor = 0
    max_floor = 10
    player = {"sprite": playerImg, "health": 0, "attack": 0, "x": screen.get_width() / 2 - 600 / 2, "y": screen.get_height() - 600, "width": 600, "height": 700}
    player["health"], player["attack"] = generate_player()
    enemy = {"sprite": None, "health": 0, "attack": 0, "x": screen.get_width() / 2 - 400 / 2, "y": screen.get_height() / 2 - 600 / 2}
    right_answers = 0
    wrong_answers = 0
    enemy_attack = False
    player_attack = False
    start_of_game = True
    start_of_boss = True
    boss_battle = False
    button_x_1 = screen.get_width() / 2 - 400
    button_x_2 = screen.get_width() / 2 - 400
    button_x_3 = screen.get_width() / 2 - 400
    
    # Main game loop
    while True:
        # Displays the title page
        if location == "title":
            location = title_page(screen, title_background, title_font, medium_font, small_font)
        # Displays the instructions
        elif location == "instructions":
            location = rules(screen, title_background, title_font, medium_font, small_font)
        # Allows user to change settings
        elif location == "settings":
            location, button_x_1, button_x_2, button_x_3, change, value = settings(screen, title_font, medium_font, small_font, button_x_1, button_x_2, button_x_3, small_font)
            max_floor, player["attack"], player["health"] = update_settings(change, value, player, max_floor)
        elif location == "menu":
            location = menu(screen, medium_font, small_font)
        # Plays the game
        elif location == "play":
            # Displays a message at the start of the game
            if start_of_game == True:
                start_of_game = False
                floor, message_type, message_counter, equation, answer, user_answer, enemy_counter, player_counter, player_attack = change_level(screen, floor, enemy_list, enemy, main_background, title_font)

            # Draws the background
            draw_image(screen, 0, 0, screen.get_width(), screen.get_height(), main_background)

            # Displays information about the game
            display_info(screen, medium_font, floor, right_answers, wrong_answers)

            # Displays information about the enemy
            display_enemy_info(screen, small_font, info_font, enemy["health"], enemy["attack"], text_box)

            # Draws the enemy
            draw_enemy(screen, enemy, 400, 600)
            
            # Displays the player
            display_player(screen, player)

            # Displays information about the player
            display_player_info(screen, small_font, info_font, player["health"], player["attack"], text_box)

            # Displays the equation
            display_equation(screen, medium_font, equation, user_answer, text_box)

            # Displays the user answer
            display_answer(screen, small_font, user_answer, text_box)

            # Displays a message if attack occurred
            message_type, message_counter = attack_message(screen, message_type, medium_font, message_counter, player, enemy)

            # Displays an animation if enemy attacks
            enemy_counter, enemy_attack = enemy_attack_animation(enemy, enemy_counter, enemy_attack)

            # Displays an animation if player attacks
            player_counter, player_attack = player_attack_animation(player, player_counter, player_attack)

            # Swaps message
            if player["health"] <= 0:
                end_message = "YOU LOSE."
            elif boss_battle == True and enemy["health"] <= 0:
                end_message = "YOU WIN."
            # Changes the round
            elif enemy["health"] <= 0:
                floor, message_type, message_counter, equation, answer, user_answer, enemy_counter, player_counter, player_attack = change_level(screen, floor, enemy_list, enemy, main_background, title_font)

            # Spawns the boss
            if floor >= max_floor and start_of_boss:
                generate_boss(screen, title_font, enemy, floor, boss1)
                start_of_boss = False
                boss_battle = True
                
            # Ends the game
            if player["health"] <= 0 or (boss_battle == True and enemy["health"] <= 0):
                enemy_attack = False
                player_attack = False
                start_of_game = True
                start_of_boss = True
                boss_battle = False
                player["health"], player["attack"] = generate_player()
                location = "end"
        # Ends the game
        elif location == "end":
            location, correct, incorrect, floor = end_game(screen, title_font, medium_font, small_font, info_font, end_message, right_answers, wrong_answers, floor)

        # Keeps screen open until X is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Adds character to end of string if digit
                if event.unicode.isdigit() or event.key == pygame.K_MINUS:
                    # Does not let user input go over 4 digits
                    if not len(user_answer) >= 4:
                        user_answer += event.unicode
                # Removes character from end of string
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                # Checks answer when enter is pressed
                elif event.key == pygame.K_RETURN:
                    # Updates the enemy
                    if user_answer == str(answer):
                        right_answers, equation, answer, message_type, player_attack = question_right(right_answers, enemy, player, floor)
                    # Updates the player
                    else:
                        wrong_answers, message_type, enemy_attack = question_wrong(wrong_answers, enemy, player)
                    user_answer = ""
                elif event.key == pygame.K_ESCAPE:
                    location = "menu"

        # Updates the display
        pygame.display.update()

        # Makes sure animation doesn't go over 30 FPS
        fpsClock.tick(fps)


def title_page(screen, background, title_font, medium_font, small_font):
    """
    Displays the title page
    """
    # Screen height and width
    height = screen.get_height()
    width = screen.get_width()
    
    # Displays the background
    draw_image(screen, 0, 0, width, height, background)

    # Displays the title
    white = (255, 255, 255)
    display_text(screen, ["MATH RPG"], title_font, white, width / 2, height / 6, 15)
    
    # Displays buttons
    black = (0, 0, 0)
    gray = (50, 50, 50)
    button_width = 300
    button_height = 100
    play = button(screen, "PLAY", medium_font, width / 2 - button_width / 2, height / 2, button_width, button_height, black, gray, white)
    instructions = button(screen, "INSTRUCTIONS", small_font, width / 2 - button_width / 2, height / 2 + button_height + 20, button_width, button_height, black, gray, white)
    settings = button(screen, "SETTINGS", small_font, width / 2 - button_width / 2, height / 2 + button_height * 2 + 20 * 2, button_width, button_height, black, gray, white)

    # Changes location if button clicked
    if play:
        return "play"
    elif instructions:
        return "instructions"
    elif settings:
        return "settings"
    else:
        return "title"

    
def rules(screen, background, title_font, medium_font, small_font):
    """
    Displays the instructions page
    """
    # Screen height and width
    height = screen.get_height()
    width = screen.get_width()

    # Displays the background
    draw_image(screen, 0, 0, width, height, background) 

    # Displays page title
    white = (255, 255, 255)
    display_text(screen, ["INSTRUCTIONS"], title_font, white, width / 2, height / 6, 15)

    # Displays instructions
    display_text(screen, ["To beat the game, you must:", "1. Answer math questions to deal damage", "2. Beat a set of enemies", "3. Survive through all the encounters"],  small_font, white, width / 2, height / 2, 15)

    # Displays the mechanics
    display_text(screen, ["Mechanics:", "When a question is displayed:", "1. Type in the answer", "2. Press enter on keyboard"], small_font, white, width / 2, height / 4 * 3, 15)

    # Displays buttons
    black = (0, 0, 0)
    gray = (50, 50, 50)
    button_width = 300
    button_height = 100
    play = button(screen, "PLAY", medium_font, width - (button_width / 2) * 2.5, height / 2, button_width, button_height, black, gray, white)
    settings = button(screen, "SETTINGS", small_font, width - (button_width / 2) * 2.5, height / 2 + button_height + 20, button_width, button_height, black, gray, white)
    
    # Changes location if button clicked
    if play:
        return "play"
    elif settings:
        return "settings"
    else:
        return "instructions"


def settings(screen, title_font, medium_font, small_font, button_x_1, button_x_2, button_x_3, slider_font):
    """
    Allows user to change settings
    """
    # Screen height and width
    width = screen.get_width()
    height = screen.get_height()
    
    # Displays settings background
    dark_brown = (97, 63, 25)
    light_brown = (156, 92, 20)
    pygame.draw.rect(screen, light_brown, [0, 0, width, height])
    pygame.draw.rect(screen, dark_brown, [0, 0, width, height], 60)

    # Displays title
    white = (255, 255, 255)
    title_text = title_font.render("SETTINGS", True, white)
    title_rect = title_text.get_rect(center=(width / 2, height / 8))
    screen.blit(title_text, title_rect)

    # Displays slider bars for settings
    x = screen.get_width() / 2 - 400
    button_x_1, button_click_1, slider_value_1 = slider(screen, x, 300, button_x_1, 10, 50, slider_font, "MAXIMUM FLOOR")
    button_x_2, button_click_2, slider_value_2 = slider(screen, x, 600, button_x_2, 10, 50, slider_font, "PLAYER ATTACK")
    button_x_3, button_click_3, slider_value_3 = slider(screen, x, 900, button_x_3, 100, 500, slider_font, "PLAYER HEALTH")

    # Displays buttons
    gray = (50, 50, 50)
    black = (0, 0, 0)
    button_width = 300
    button_height = 100
    play = button(screen, "PLAY", medium_font, width - button_width - 50, height - button_height * 2 - 150, button_width, button_height, white, gray, black)
    instructions = button(screen, "INSTRUCTIONS", small_font, width - button_width - 50, height - button_height - 100, button_width, button_height, white, gray, black)

    # Checks which slider was clicked
    value = 0
    change = ""
    if button_click_1:
        change = "floor"
        value = slider_value_1
    elif button_click_2:
        change = "player_attack"
        value = slider_value_2
    elif button_click_3:
        change = "player_health"
        value = slider_value_3

    # Checks button clicks
    if play:
        location = "play"
    elif instructions:
        location = "instructions"
    else:
        location = "settings"
    
    return location, button_x_1, button_x_2, button_x_3, change, value


def update_settings(change, value, player, floor):
    """
    Updates values for settings
    """
    # Health and attack values for player
    health = player["health"]
    attack = player["attack"]
    max_floor = floor
    
    # Changes settings
    if change == "floor":
        max_floor = value
    elif change == "player_attack":
        attack = value
    elif change == "player_health":
        health = value

    return max_floor, attack, health


def slider(screen, slider_x, slider_y, button_x, minimum, maximum, font, message):
    """
    Creates a slider bar
    """
    # X and Y values for mouse cursor
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    # Draws the slider label
    white = (255, 255, 255)
    slider_label = font.render(message, True, white)
    slider_label_rect = slider_label.get_rect(center=(screen.get_width() / 2, slider_y - 50))
    screen.blit(slider_label, slider_label_rect)
    
    # Draws the slider background
    dark_brown = (97, 63, 25)
    pygame.draw.rect(screen, dark_brown, [slider_x, slider_y, 800, 50])

    # Draws the slider button
    black = (0, 0, 0)
    light_brown = (156, 92, 20)
    pygame.draw.rect(screen, light_brown, [button_x, slider_y, 50, 50])
    pygame.draw.rect(screen, black, [button_x, slider_y, 50, 50], 5)

    # Checks if mouse is in slider button
    click = False
    lighter_brown = (214, 130, 19)
    if button_x + 50 > mouse_x > button_x - 50 and slider_y + 50 > mouse_y > slider_y:
        pygame.draw.rect(screen, lighter_brown, [button_x, slider_y, 50, 50])
        pygame.draw.rect(screen, black, [button_x, slider_y, 50, 50], 5)
        # Checks if mouse was clicked
        if pygame.mouse.get_pressed()[0] and slider_x + 800 > mouse_x > slider_x and slider_y + 50 > mouse_y > slider_y:
            button_x = mouse_x
            click = True

    # Displays the current value of the slider
    value = round((button_x - slider_x) / 800 * (maximum - minimum) + minimum)
    slider_value = font.render(str(value), True, white)
    slider_value_rect = slider_value.get_rect(center=(slider_x + 800 + 75, slider_y + 25))
    screen.blit(slider_value, slider_value_rect)
    
    return button_x, click, value     


def menu(screen, medium_font, small_font):
    """
    Displays a menu
    """
    # Screen height and width
    width = screen.get_width()
    height = screen.get_height()
    
    # Displays menu background
    background_width = 400
    background_height = 600
    black = (0, 0, 0)
    pygame.draw.rect(screen, black, [width / 2 - background_width / 2, height / 2 - background_height / 2, background_width, background_height])

    # Displays buttons
    button_width = 300
    button_height = 100
    white = (255, 255, 255)
    gray = (50, 50, 50)
    play = button(screen, "PLAY", medium_font, width / 2 - button_width / 2, height / 2 - button_height / 2 - 200, button_width, button_height, white, gray, black)
    instructions = button(screen, "INSTRUCTIONS", small_font, width / 2 - button_width / 2, height / 2 - button_height / 2 - 70, button_width, button_height, white, gray, black)
    settings = button(screen, "SETTINGS", small_font, width / 2 - button_width / 2, height / 2 - button_height / 2 + 70, button_width, button_height, white, gray, black)
    quit_game = button(screen, "QUIT", medium_font, width / 2 - button_width / 2, height / 2 - button_height / 2 + 200, button_width, button_height, white, gray, black)

    # Changes location if button clicked
    if play:
        return "play"
    elif settings:
        return "settings"
    elif instructions:
        return "instructions"
    elif quit_game:
        pygame.quit()
        sys.exit()
    else:
        return "menu"


def end_game(screen, title_font, medium_font, small_font, info_font, message, correct, incorrect, floor):
    """
    Shows the end game screen
    """
    # Width and height of screen
    width = screen.get_width()
    height = screen.get_height()
    
    # Displays the background
    black = (0, 0, 0)
    screen.fill(black)

    # Displays victory message
    white = (255, 255, 255)
    end_message = title_font.render(message, True, white)
    end_message_rect = end_message.get_rect(center=(width / 2, height / 6))
    screen.blit(end_message, end_message_rect)

    # Displays game information
    display_text(screen, ["CORRECT ANSWERS: " + str(correct), "INCORRECT ANSWERS: " + str(incorrect), "FLOOR REACHED: " + str(floor)], info_font, white, width / 2, height / 6 + 75, 25)

    # Displays buttons
    gray = (50, 50, 50)
    button_width = 300
    button_height = 100
    play = button(screen, "PLAY", medium_font, width / 2 - button_width / 2, height - button_height * 4 - 200, button_width, button_height, white, gray, black)
    instructions = button(screen, "INSTRUCTIONS", small_font, width / 2 - button_width / 2, height - button_height * 3 - 150, button_width, button_height, white, gray, black)
    settings = button(screen, "SETTINGS", small_font, width / 2 - button_width / 2, height - button_height * 2 - 100, button_width, button_height, white, gray, black)
    quit_game = button(screen, "QUIT", medium_font, width / 2 - button_width / 2, height - button_height - 50, button_width, button_height, white, gray, black)

    # Checks which button was clicked
    if play:
        location = "play"
    elif instructions:
        location = "instructions"
    elif settings:
        location = "settings"
    elif quit_game:
        pygame.quit()
        sys.exit()
    else:
        return "end", correct, incorrect, floor

    return location, 0, 0, 0

        
def change_level(screen, floor, sprites, enemy, background, title_font):
    """
    Changes the level
    """
    # Resets and changes variables
    floor += 1
    message_type = ""
    message_counter = 0
    user_answer = ""
    enemy_counter = 0
    player_counter = 0
    player_attack = False
                            
    # Generates a new enemy
    enemy["sprite"], enemy["health"], enemy["attack"] = generate_enemy(floor, sprites)

    # Generates a new equation
    equation, answer = generate_equation(floor)
    
    # Fades into black
    fade_surface(screen, background, 0, 0, screen.get_width(), screen.get_height(), 5)

    # Displays an in between round message
    display_floor_message(screen, "FLOOR " + str(floor), title_font)
    
    # Fades back into black
    white = (255, 255, 255)
    fade_text = title_font.render("FLOOR " + str(floor), True, white)
    text_width = fade_text.get_width()
    text_height = fade_text.get_height()
    fade_surface(screen, fade_text, screen.get_width() / 2 - text_width / 2, screen.get_height() / 2 - text_height / 2, text_width, text_height, 5)

    return floor, message_type, message_counter, equation, answer, user_answer, enemy_counter, player_counter, player_attack


def fade_surface(screen, surface, x, y, width, height, fade_delay):
    """
    Fades the screen into black
    """
    # Surface that will be put over to fade screen
    black = (0, 0, 0)
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill(black)

    # Fades the screen
    for alpha in range(0, 255):
        pygame.event.get()
        fade_surface.set_alpha(alpha)
        draw_image(screen, x, y, width, height, surface)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(fade_delay)


def display_floor_message(screen, message, title_font):
    """
    Displays a start of game message
    """
    # Colors for background and text
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Fills screen with black
    screen.fill(black)

    # Displays a message
    title_text = title_font.render(message, True, white)
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(title_text, title_rect)
    pygame.display.update()
    pygame.time.delay(3000)

    
def attack_message(screen, message_type, font, counter, player, enemy):
    """
    Displays message after attacking
    """
    # Gets text for message
    red = (161, 40, 48)
    if message_type == "attack":
        counter += 1
        message = "You dealt " + str(player["attack"]) + " damage!"
    elif message_type == "defend":
        counter += 1
        message = "You lost " + str(enemy["attack"]) + " health!"
    else:
        message = ""
        
    # Displays the message
    text = font.render(message, True, red)
    text_rect = text.get_rect(center=(screen.get_width() / 2, 200))
    screen.blit(text, text_rect)

    # Removes attack message after set amount of frames
    if counter > 80:
        return "", 0
    
    return message_type, counter


def display_info(screen, font, level, right_answers, wrong_answers):
    """
    Displays information about game
    """
    # Color for text
    white = (255, 255, 255)

    # Displays the level text
    level_text = font.render("Floor: " + str(level), True, white)
    screen.blit(level_text, (25, 25))

    # Display the right answers text
    correct_text = font.render("Correct: " + str(right_answers), True, white)
    screen.blit(correct_text, (25, 25 + level_text.get_height()))

    # Displays the wrong answers text
    incorrect_text = font.render("Incorrect: " + str(wrong_answers), True, white)
    screen.blit(incorrect_text, (25, 25 + level_text.get_height() + incorrect_text.get_height()))


def generate_enemy(level, sprites):
    """
    Generates an enemy
    """
    # Picks a sprite for the monster
    sprite = random.choice(sprites)
    
    # Generates random stats for the enemy
    health = random.randint(10 * level, 15 * level)
    attack = random.randint(5, 10)

    return sprite, health, attack


def generate_boss(screen, title_font, enemy, level, sprite):
    """
    Generates a boss
    """
    # Displays an introduction message
    display_floor_message(screen, "FINAL ROUND", title_font)
    fade_text = title_font.render("FINAL ROUND", True, (255, 255, 255))
    fade_surface(screen, fade_text, screen.get_width() / 2 - fade_text.get_width() / 2, screen.get_height() / 2 - fade_text.get_height() / 2, fade_text.get_width(), fade_text.get_height(), 5)

    # Changes stats for enemy
    enemy["health"] = random.randint(20 * level, 25 * level)
    enemy["attack"] = random.randint(20, 25)
    enemy["sprite"] = sprite


def draw_enemy(screen, enemy, enemy_width, enemy_height):
    """
    Draws the enemy
    """
    # Draws the enemy
    draw_image(screen, enemy["x"], enemy["y"], enemy_width, enemy_height, enemy["sprite"])


def display_enemy_info(screen, header_font, stats_font, health, attack, text_box):
    """
    Displays information about the enemy
    """
    # Width and height for text box
    width = 300
    height = 300
    
    # Displays a location for the text
    draw_image(screen, screen.get_width() - 100 - width, 100, width, height, text_box)

    # Displays the text
    white = (255, 255, 255)
    text = header_font.render("ENEMY STATS", True, white)
    text_rect = text.get_rect(center=(screen.get_width() - 100 - width / 2, 150))
    screen.blit(text, text_rect)
    display_text(screen, ["HEALTH: " + str(health), "ATTACK: " + str(attack)], stats_font, white, screen.get_width() - 100 - width / 2, 150 + text.get_height(), 15)


def enemy_attack_animation(enemy, counter, enemy_attack):
    """
    Displays an enemy attack animation
    """
    # Moves the enemy
    if enemy_attack == True:
        if counter < 30:
            enemy["y"] += 5
        elif counter < 60:
            enemy["y"] -= 5
        else:
            enemy_attack = False
            counter = 0
        counter += 1

    return counter, enemy_attack


def display_player(screen, player):
    """
    Draws the player
    """
    # Draws the player
    draw_image(screen, player["x"], player["y"], player["width"], player["height"], player["sprite"])


def display_player_info(screen, header_font, stats_font, health, attack, text_box):
    """
    Displays information about the player
    """
    # Width and height for text box
    width = 300
    height = 300

    # Displays a location for the text
    draw_image(screen, screen.get_width() - 100 - width, screen.get_height() - height - 100, width, height, text_box)

    # Displays the text
    white = (255, 255, 255)
    text = header_font.render("PLAYER STATS", True, white)
    text_rect = text.get_rect(center=(screen.get_width() - 100 - width / 2, screen.get_height() - height - 50))
    screen.blit(text, text_rect)
    display_text(screen, ["HEALTH: " + str(health), "ATTACK: " + str(attack)], stats_font, white, screen.get_width() - 100 - width / 2, screen.get_height() - height - 50 + text.get_height(), 15) 


def generate_player():
    """
    Generates the player
    """
    # Stats for player
    health = 100
    attack = 10

    return health, attack


def player_attack_animation(player, counter, player_attack):
    """
    Displays a player attack animation
    """
    # Moves the player
    if player_attack == True:
        if counter < 30:
            player["y"] -= 5
        elif counter < 60:
            player["y"] += 5
        else:
            player_attack = False
            counter = 0
        counter += 1

    return counter, player_attack


def generate_equation(level):
    """
    Generates an equat
    ion
    """
    # Picks an equation type
    equation_types = ["addition", "subtraction", "multiplication", "division"]
    equation_type = random.choice(equation_types)

    # Generates two random integers
    if equation_type == "addition" or equation_type == "subtraction":
        num1 = random.randint(0, 10 * level)
        num2 = random.randint(0, 10 * level)
    else:
        num1 = random.randint(1, 2 * level)
        num2 = random.randint(1, 2 * level)
        
    # Generates addition question
    if equation_type == "addition":
        answer = num1 + num2
        equation = str(num1) + " + " + str(num2)
    # Generates subtraction question
    elif equation_type == "subtraction":
        answer = num1 - num2
        equation = str(num1) + " - " + str(num2)
    # Generates multiplicaton question
    elif equation_type == "multiplication":
        answer = num1 * num2
        equation = str(num1) + " x " + str(num2)
    # Generates division question
    else:
        product = num1 * num2
        answer = int(product / num2)
        equation = str(product) + " / " + str(num2)

    return equation, answer


def display_equation(screen, font, equation, user_answer, text_box):
    """
    Displays the equation
    """
    # Width and height for the text box
    width = 200
    height = 100

    # Draws the text box
    draw_image(screen, screen.get_width() - 200 - width, screen.get_height() / 2 - height / 2, width, height, text_box)

    # Displays the equation
    white = (255, 255, 255)
    text = font.render(equation + " =", True, white)
    text_rect = text.get_rect(center=(screen.get_width() - 200 - width / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


def display_answer(screen, font, user_answer, text_box):
    """
    Displays an input box for answer
    """
    # Width and height for the text box
    width = 75
    height = 100
    
    # Draws the text box
    draw_image(screen, screen.get_width() - 100 - width, screen.get_height() / 2 - height / 2, width, height, text_box)

    # Displays the answer
    white = (255, 255, 255)
    text = font.render(user_answer, True, white)
    text_rect = text.get_rect(center=(screen.get_width() - 100 - width / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


def question_right(right_answers, enemy, player, level):
    """
    Changes variables if question right
    """
    right_answers += 1
    message_counter = 0
    equation, answer = generate_equation(level)
    message_type = "attack"
    enemy["health"] -= player["attack"]
    player_attack = True

    return right_answers, equation, answer, message_type, player_attack

    
def question_wrong(wrong_answers, enemy, player):
    """
    Changes variables if question wrong
    """
    wrong_answers += 1
    message_counter = 0
    message_type = "defend"
    player["health"] -= enemy["attack"]
    enemy_attack = True

    return wrong_answers, message_type, enemy_attack


def draw_image(screen, x, y, scaled_width, scaled_height, image):
    """
    Draws an image and scales it to an appropriate width/height
    """
    # Loads images
    smaller_image = pygame.transform.scale(image, (scaled_width, scaled_height))

    # Displays the image
    screen.blit(smaller_image, (x, y))

    
def display_text(screen, text, font, color, x, y, margin):
    """
    Allows text to be displayed multiline.
    Text must be passed in through a list.
    """
    rendered_text = []

    # Renders all the text and appends it into a list
    for line in text:
        rendered_text.append(font.render(line, True, color))

    # Blits the line onto the screen
    for line in range(len(rendered_text)):
        line_rect = rendered_text[line].get_rect(center=(x, y + line * rendered_text[line].get_height() + margin * line))
        screen.blit(rendered_text[line], line_rect)


def button(screen, message, font, x, y, width, height, color, hover_color, text_color):
    """
    Checks for button presses and hovers
    """
    # Gets position of mouse cursor
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    
    # Checks if button is clicked
    if x + width > mouse_x > x and y + height > mouse_y > y:
        # Draws a button with a different color when hovered
        pygame.draw.rect(screen, hover_color, [x, y, width, height])

        # Checks if mouse is clicked
        if pygame.mouse.get_pressed()[0]:
            return True
    else:
        # Draws a normal button
        pygame.draw.rect(screen, color, [x, y, width, height])

    # Displays text in button
    display_text(screen, [message], font, text_color, x + width / 2, y + height / 2, 15)

    return False


if __name__ == "__main__":
    main()
