"""
    Contain Utility functionality like:
        - Play sound
        - Handle images
        ...
"""
import pygame
import time
import sys
import os

# Determine the base path
if getattr(sys, 'frozen', False):
    # When bundled by PyInstaller, use the temporary directory
    base_path = sys._MEIPASS
else:
    # When running from source, use the script's directory
    base_path = os.path.dirname(__file__)

# Construct paths to resource folders
sounds_dir = os.path.join(base_path, 'sounds')
images_dir = os.path.join(base_path, 'images')

# Initialize Pygame mixer
pygame.mixer.init()

# Load sounds with dynamic paths
sounds = {
    1: pygame.mixer.Sound(os.path.join(sounds_dir, 'eat.mp3')),
    2: pygame.mixer.Sound(os.path.join(sounds_dir, 'game-over.mp3')),
    3: pygame.mixer.Sound(os.path.join(sounds_dir, 'HighScore.mp3')),
}

# Dictionary to track current playing channels
current_channels = {
    1: None,
    2: None,
    3: None,
}

def play_sound(track):
    """
    Ensures the sound only plays again after the current instance finishes.
    """
    if current_channels[track] is None or not current_channels[track].get_busy():
        channel = sounds[track].play()
        current_channels[track] = channel

def fetch_win():
    """
    Fetch and return the trophy image, then play the win sound.
    """
    try:
        trophy_path = os.path.join(images_dir, 'Trophy.png')
        trophy_image = pygame.image.load(trophy_path).convert_alpha()
        trophy_image = pygame.transform.scale(trophy_image, (300, 300))
    except Exception as e:
        print("Error loading trophy.png:", e)
        trophy_image = None

    play_sound(3)
    return trophy_image

if __name__ == "__main__":
    # Simulate displaying the trophy and playing the sound
    trophy = fetch_win()
    if trophy:
        print("Displaying trophy...")
        time.sleep(3)
        play_sound(3)