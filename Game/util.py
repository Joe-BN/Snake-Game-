# run miscelanious functionalities
"""
eg:
    - run music/sound
    - run the video
    - display text from a file (instruction docs)
    - 

"""

import pygame
import time

def play_sound(track):
    pygame.mixer.init()

    sounds = {
        1:"sounds/eat.mp3",
        2:"sounds/game-over.mp3",
        3:"sounds/HighScore.mp3",
    }

    # get the sound and play it
    sound = pygame.mixer.Sound(sounds[track])
    sound.play()
    
    

def fetch_win():
    # the code to fetch the documentaion when needed
    try:
        trophy_image = pygame.image.load("images/Trophy.png").convert_alpha()
        trophy_image = pygame.transform.scale(trophy_image, (300, 300))

    except Exception as e:
        print("Error loading trophy.png:", e)
        trophy_image = None

    return trophy_image
    time.sleep(3)

    play_sound(3)

    