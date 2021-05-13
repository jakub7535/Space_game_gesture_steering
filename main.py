import sys
import time
import pygame
import cv2
from steering import HandDetector, Steering
from time import sleep
from space_objects import Player
from screen import Screen
from game import Game
from level_images_load import read_level_images

def play_game():
    vid = cv2.VideoCapture(0)
    vid_h = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vid_w = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    steering_img_ratio = vid_w / vid_h

    game_screen_height = 1300
    game_screen_width = 1200
    steering_screen_height = int(game_screen_height * 0.5)
    steering_screen_width = int(steering_screen_height * steering_img_ratio)
    detector = HandDetector(steering_screen_height, steering_screen_width, draw_hands=False)

    pygame.init()
    screen = Screen(width=game_screen_width, height=game_screen_height,
                    steering_img_ratio=steering_img_ratio)
    player = Player(x=screen.width / 2, y=screen.height , size=120)
    game = Game()
    game.level_images = read_level_images('star_wars', game.n_levels, screen.height,
                                     steering_img_ratio)
    steering = Steering(steering_screen_height,
                                     steering_screen_width)

    # how many pixel passed
    pixels = 0
    index_calculated = False
    while True:
        start_time = time.time()
        _, img = vid.read()
        img = cv2.resize(img, (steering_screen_width, steering_screen_height))
        img = cv2.flip(img, 1)
        detector.get_hands_params(img)

        turn = None
        shot = False

        steering.calculate_wheel(img, detector.left_hand, detector.right_hand)
        if steering.wheel_radius is not None:
            turn, shot = steering.get_commands(detector)


        if game.life > 0:
            game.collision_check(player)
            game.laser_hit_check()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

            if turn is not None:
                player.x = min(max(player.x - 0.002 * steering.wheel_angle * player.size, 0),
                               screen.width - player.size)
            if shot:
                game.create_laser(player.x, player.y, player.size)

            # when to create new resources and obstacles
            if game.speed > pixels % screen.height >= 0:
                game.create_resources_obstacles(screen.width, screen.height)
                game.ammunition = min(game.ammunition + 20, 100)
            pixels += game.speed

            game.update_resources_obstacles_positions(screen.height)
            game.update_lasers_positions(pixels)
            game.set_level_speed()
            screen.update_screen(game, player, img, steering, start_time)
            pygame.display.update()
        else:
            pygame.display.update()
            # Where player would be in top scores
            if not index_calculated:
                index = next((i for i, record_score in enumerate(game.record_scores)
                              if game.score > record_score), None)
                index_calculated = True
            game_state = game.end_game(screen, game, index, img)
            if game_state == 'over':

                pygame.display.quit()
                pygame.quit()
                vid.release()
                sys.exit()
                break
            elif game_state == 'new game':
                vid.release()
                play_game()

if __name__ == "__main__":
    play_game()