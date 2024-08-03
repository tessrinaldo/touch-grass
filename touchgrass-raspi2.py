import time
import board
import busio
from adafruit_cap1188.i2c import CAP1188_I2C
import pygame
import random
import os

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize CAP1188 sensor
cap = CAP1188_I2C(i2c)

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Define sound file directories
sounds_dir1 = "sounds/touchme"
sounds_dir2 = "sounds/donttouchme"

# Get list of sound files
sound_files1 = [f for f in os.listdir(sounds_dir1) if f.endswith('.wav') or f.endswith('.mp3')]
sound_files2 = [f for f in os.listdir(sounds_dir2) if f.endswith('.wav') or f.endswith('.mp3')]

# Create pygame.mixer.Sound objects for each list
sounds1 = [pygame.mixer.Sound(os.path.join(sounds_dir1, f)) for f in sound_files1]
sounds2 = [pygame.mixer.Sound(os.path.join(sounds_dir2, f)) for f in sound_files2]

# Create channels for simultaneous playback
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

def play_random_sound(sounds, channel):
    sound = random.choice(sounds)
    channel.play(sound)

# Main loop
while True:
    c1_touched = cap[0].value  # C1 is the first pin (index 0)
    c2_touched = cap[1].value  # C2 is the second pin (index 1)
    
    if c1_touched and not channel1.get_busy():
        print("C1 touched! Playing sound from list 1...")
        play_random_sound(sounds1, channel1)
    
    if c2_touched and not channel2.get_busy():
        print("C2 touched! Playing sound from list 2...")
        play_random_sound(sounds2, channel2)
    
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage