# run miscelanious functionalities
"""
eg:
    - run music/sound
    - run the video
    - display text from a file (instruction docs)
    - 

"""

import pygame


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
    
    

#def fetch_docs():
    # the code to fetch the documentaion when needed

