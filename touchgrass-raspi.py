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


def is_music_playing():
    return pygame.mixer.music.get_busy()

# Create channels for simultaneous playback
pygame.mixer.set_num_channels(3)  # Ensure we have enough channels
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2) 


def play_sound_once(sound, channel):
    if not channel.get_busy():
        channel.play(sound)

def play_loop_sound(loop_sound, channel):
    channel.play(loop_sound, loops=-1)
    
def stop_loop_sound(channel):
    channel.stop()

def play_mp3(sounds_dir, sound_files):
  # Load the MP3 file (replace with your file path)
  pygame.mixer.music.load(sounds_dir + random.choice(sound_files))
  pygame.mixer.music.play()

def play_random_sound(sounds, channel):
    sound = random.choice(sounds)
    channel.play(sound)


pin_touched = {pin: False for pin in range(4)}

# Main loop
while True:
    if cap[1].value:
        if not pin_touched[1]:
            print("yesss touch me")
            play_loop_sound(random.choice(touchme_sounds), channel1)
            pin_touched[1] = True
    else:
        if pin_touched[1]:
            stop_loop_sound(channel1)
            pin_touched[1] = False

    if cap[2].value:
        if not pin_touched[2]:
            print("ew go away")
            play_loop_sound(random.choice(donttouch_sounds), channel2)
            pin_touched[2] = True
    else:
        if pin_touched[2]:
            stop_loop_sound(channel2)
            pin_touched[2] = False
    
    if cap[3].value:
        if not pin_touched[3]:
            print("boots & cats")
            play_loop_sound(pygame.mixer.Sound("sounds/other/amen-break.wav"), channel3)      
            pin_touched[3] = True
    else: 
        if pin_touched[3]:
            print("stopping drums")
            stop_loop_sound(channel3)
            pin_touched[3] = False
        
    if is_music_playing():
        print("audio still playing")
    
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage