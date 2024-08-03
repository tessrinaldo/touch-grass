import pygame
import numpy as np
import time
import random
import board
import busio
from adafruit_cap1188.i2c import CAP1188_I2C

# Initialize I2C bus and CAP1188 sensor
i2c = busio.I2C(board.SCL, board.SDA)
cap = CAP1188_I2C(i2c)

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# Define two scales (C major and A minor)
scale1 = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
scale2 = [220.00, 261.63, 293.66, 329.63, 349.23, 440.00, 523.25]

def generate_tone(freq, duration=0.1):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate a sine wave
    tone = np.sin(2 * np.pi * freq * t)
    
    # Add some "glitter" with high-frequency noise
    glitter = np.random.rand(len(t)) * np.exp(-t * 10) * 0.05
    
    # Combine and normalize
    waveform = (tone + glitter) * 0.5
    
    # Apply a simple envelope
    envelope = np.exp(-t * 10)  # Faster decay for arpeggiator effect
    waveform = waveform * envelope
    
    # Convert to 16-bit PCM and make it stereo
    waveform = (waveform * 32767).astype(np.int16)
    stereo_waveform = np.column_stack((waveform, waveform))
    
    return pygame.sndarray.make_sound(stereo_waveform)

# Generate tones for each scale
tones1 = [generate_tone(freq) for freq in scale1]
tones2 = [generate_tone(freq) for freq in scale2]

def play_random_note(tones):
    tone = random.choice(tones)
    tone.play()

def generate_drum_sound(freq, duration=0.1, decay=50):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    drum = np.sin(2 * np.pi * freq * t) * np.exp(-t * decay)
    drum += np.random.rand(len(t)) * np.exp(-t * decay) * 0.2  # Add some noise
    
    drum = (drum / np.max(np.abs(drum)) * 32767).astype(np.int16)
    stereo_drum = np.column_stack((drum, drum))
    
    return pygame.sndarray.make_sound(stereo_drum)

# Generate different drum sounds
kick = generate_drum_sound(50, duration=0.15, decay=20)
snare = generate_drum_sound(180, duration=0.1, decay=40)
hihat = generate_drum_sound(800, duration=0.05, decay=100)

# Amen break-inspired pattern (1 = kick, 2 = snare, 3 = hihat)
drum_pattern = [
    1, 3, 0, 3, 2, 3, 0, 3,
    0, 3, 0, 3, 2, 3, 2, 3,
    1, 3, 0, 3, 2, 3, 0, 3,
    0, 3, 2, 0, 2, 3, 2, 3
]
drum_index = 0

def play_drum():
    global drum_index
    if drum_pattern[drum_index] == 1:
        kick.play()
    elif drum_pattern[drum_index] == 2:
        snare.play()
    elif drum_pattern[drum_index] == 3:
        hihat.play()
    drum_index = (drum_index + 1) % len(drum_pattern)

# Main loop
while True:
    pin2_touched = cap[2].value
    pin4_touched = cap[4].value
    pin5_touched = cap[5].value
    
    if pin2_touched or pin4_touched or pin5_touched:
        print("Plant touched! Playing sounds...")
        
        while pin2_touched or pin4_touched or pin5_touched:
            if pin2_touched:
                play_random_note(tones1)
            if pin4_touched:
                play_random_note(tones2)
            if pin5_touched:
                play_drum()
            
            time.sleep(0.05)  # Shorter delay for faster drum pattern
            
            # Update touch status
            pin2_touched = cap[2].value
            pin4_touched = cap[4].value
            pin5_touched = cap[5].value
        
        print("Touch released. Stopping sounds.")
    
    time.sleep(0.01)  # Small delay to prevent excessive CPU usage