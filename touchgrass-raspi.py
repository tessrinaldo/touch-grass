import time
import board
import busio
from adafruit_cap1188.i2c import CAP1188_I2C
import pygame
import random
import os
import numpy as np

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize CAP1188 sensor
cap = CAP1188_I2C(i2c)

# Initialize pygame mixer for audio playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# Define sound file directories
sounds_dir1 = "sounds/touchme"
sounds_dir2 = "sounds/donttouchme"

# Get list of sound files
touchme_files = [f for f in os.listdir(sounds_dir1) if f.endswith('.wav') or f.endswith('.mp3')]
donttouch_files = [f for f in os.listdir(sounds_dir2) if f.endswith('.wav') or f.endswith('.mp3')]

def load_stereo_sound(file_path):
    sound = pygame.mixer.Sound(file_path)
    array = pygame.sndarray.array(sound)
    
    # If the sound is mono, convert it to stereo
    if array.ndim == 1:
        stereo_array = np.column_stack((array, array))
    elif array.shape[1] == 1:
        stereo_array = np.column_stack((array, array))
    else:
        stereo_array = array
    
    return pygame.sndarray.make_sound(stereo_array)

# Create pygame.mixer.Sound objects for each list
touchme_sounds = [load_stereo_sound(os.path.join(sounds_dir1, f)) for f in touchme_files]
donttouch_sounds = [load_stereo_sound(os.path.join(sounds_dir2, f)) for f in donttouch_files]

# Set volume for all sounds (0.0 to 1.0)
volume = 5.0  # Maximum volume
for sound in touchme_sounds + donttouch_sounds:
    sound.set_volume(volume)

# Create channels for simultaneous playback
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

def is_music_playing():
    return pygame.mixer.music.get_busy()

# def play_mp3():
#   # Load the MP3 file (replace with your file path)
#   pygame.mixer.music.load(sounds_dir + sound_files[random.randint(0,2)])
#   pygame.mixer.music.play()

def play_random_sound(sounds, channel):
    sound = random.choice(sounds)
    channel.play(sound)

touchme_pin = 1
donttouch_pin = 2

# Main loop
while True:
    # touch_states = [cap[i].value for i in range(1, 9)]
    # print(f"touch states: {touch_states}")
   
    if cap[touchme_pin].value == True and not is_music_playing(): # Touched
        print(f"yesss touch me")
        play_random_sound(touchme_sounds, channel2)
        
        # Wait for the touch to be released
        while cap[touchme_pin].value == True:
            print(f"you're still touching me..")   
            time.sleep(0.1)

    if cap[donttouch_pin].value == True and not is_music_playing(): # Touched
        print(f"yesss touch me")
        play_random_sound(donttouch_sounds, channel2)
        
        # Wait for the touch to be released
        while cap[donttouch_pin].value == True:
            print(f"you're still touching me..")   
            time.sleep(0.1)
        
    if is_music_playing():
        print("audio still playing")
    
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage