"""
    Contail Utility functionality like:
        - Play sound
        - Handle images
        ...
"""
import pygame
import time


pygame.mixer.init()
sounds = {
    1: pygame.mixer.Sound("sounds/eat.mp3"),
    2: pygame.mixer.Sound("sounds/game-over.mp3"),
    3: pygame.mixer.Sound("sounds/HighScore.mp3"),
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
    # Check if the sound's channel is None or not busy
    if current_channels[track] is None or not current_channels[track].get_busy():
        # Play the sound and store its channel
        channel = sounds[track].play()
        current_channels[track] = channel

def fetch_win():
    """
    Fetch and return the trophy image, then play the win sound after a delay.
    """
    try:
        trophy_image = pygame.image.load("images/Trophy.png").convert_alpha()
        trophy_image = pygame.transform.scale(trophy_image, (300, 300))
    except Exception as e:
        print("Error loading trophy.png:", e)
        trophy_image = None

    play_sound(3)
    return trophy_image




if __name__ == "__main__":
    # Simulate displaying the trophy and playing the sound by default
    trophy = fetch_win()
    if trophy:
        # Here you would display the trophy image in your game loop
        print("Displaying trophy...")
        time.sleep(3)  # Wait 3 seconds
        play_sound(3)  # Play "HighScore.mp3"