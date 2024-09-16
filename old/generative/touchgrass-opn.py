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
c_maj = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
a_min = [220.00, 261.63, 293.66, 329.63, 349.23, 440.00, 523.25]

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
tones1 = [generate_tone(freq) for freq in c_maj]
tones2 = [generate_tone(freq) for freq in a_min]

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


def generate_bass_drone(duration=2.0, base_freq=55):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate a low sine wave with slight frequency modulation
    mod = np.sin(2 * np.pi * 0.1 * t)  # Slow modulation
    bass = np.sin(2 * np.pi * base_freq * t + mod * 5)
    
    # Add harmonics
    bass += 0.5 * np.sin(2 * np.pi * base_freq * 2 * t)
    bass += 0.25 * np.sin(2 * np.pi * base_freq * 3 * t)
    
    # Apply a slow envelope
    envelope = 1 - np.exp(-t * 0.5)
    bass = bass * envelope
    
    # Normalize and convert to 16-bit PCM
    bass = (bass / np.max(np.abs(bass)) * 32767 * 0.7).astype(np.int16)
    stereo_bass = np.column_stack((bass, bass))
    
    return pygame.sndarray.make_sound(stereo_bass)


def generate_glitch_texture(duration=0.5):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate a complex waveform with frequency modulation
    carrier = np.sin(2 * np.pi * 440 * t)
    modulator = np.sin(2 * np.pi * 110 * t)
    glitch = carrier * modulator
    
    # Add some noise and distortion
    noise = np.random.rand(len(t)) * 0.2
    glitch = np.clip(glitch + noise, -1, 1)
    
    # Apply an envelope
    envelope = np.exp(-t * 5)
    glitch = glitch * envelope
    
    # Normalize and convert to 16-bit PCM
    glitch = (glitch / np.max(np.abs(glitch)) * 32767).astype(np.int16)
    stereo_glitch = np.column_stack((glitch, glitch))
    
    return pygame.sndarray.make_sound(stereo_glitch)


def generate_ambient_pad(duration=3.0, base_freq=220):
    sample_rate = 44100
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate multiple sine waves with slight detuning
    pad = np.sin(2 * np.pi * base_freq * t)
    pad += np.sin(2 * np.pi * (base_freq * 1.01) * t) * 0.5
    pad += np.sin(2 * np.pi * (base_freq * 0.99) * t) * 0.5
    
    # Add a slow LFO for subtle modulation
    lfo = np.sin(2 * np.pi * 0.2 * t)
    pad = pad * (1 + lfo * 0.1)
    
    # Apply a slow attack and release envelope
    envelope = (1 - np.exp(-t)) * np.exp(-(t - duration) * 2)
    pad = pad * envelope
    
    # Normalize and convert to 16-bit PCM
    pad = (pad / np.max(np.abs(pad)) * 32767 * 0.7).astype(np.int16)
    stereo_pad = np.column_stack((pad, pad))
    
    return pygame.sndarray.make_sound(stereo_pad)


# Generate sounds
bass_drone = generate_bass_drone()
glitch_texture = generate_glitch_texture()
ambient_pad = generate_ambient_pad()

# Create separate channels for each sound
bass_channel = pygame.mixer.Channel(0)
glitch_channel = pygame.mixer.Channel(1)
ambient_channel = pygame.mixer.Channel(2)

# Variables for glitch timing
last_glitch_time = 0
glitch_interval = 0


# # Main loop
# while True:
#     pin2_touched = cap[2].value
#     pin4_touched = cap[4].value
#     pin5_touched = cap[5].value
    
#     if pin2_touched or pin4_touched or pin5_touched:
#         print("Plant touched! Playing sounds...")
        
#         while pin2_touched or pin4_touched or pin5_touched:
#             if pin2_touched:
#                 play_random_note(tones1)
#             if pin4_touched:
#                 play_random_note(tones2)
#             if pin5_touched:
#                 play_drum()
            
#             time.sleep(0.05)  # Shorter delay for faster drum pattern
            
#             # Update touch status
#             pin2_touched = cap[2].value
#             pin4_touched = cap[4].value
#             pin5_touched = cap[5].value
        
#         print("Touch released. Stopping sounds.")
    
#     time.sleep(0.01)  # Small delay to prevent excessive CPU usage

# Main loop
while True:
    pin2_touched = cap[2].value
    pin4_touched = cap[4].value
    pin5_touched = cap[5].value
    
    if any([pin2_touched, pin4_touched, pin5_touched]):
        print("you touched me!")
        
        while any([pin2_touched, pin4_touched, pin5_touched]):
            current_time = time.time()
            if pin2_touched and not bass_channel.get_busy():
                bass_channel.play(bass_drone, loops=-1)
            elif not pin2_touched:
                bass_channel.stop()
            
            if pin4_touched:
                if current_time - last_glitch_time > glitch_interval:
                    glitch_sound = generate_glitch_texture(duration=random.uniform(0.05, 0.2))
                    glitch_channel.play(glitch_sound)
                    last_glitch_time = current_time
                    glitch_interval = random.uniform(0.1, 0.5)  # Random interval between glitches
            elif not pin4_touched:
                glitch_channel.stop()
            
            if pin5_touched and not ambient_channel.get_busy():
                ambient_channel.play(ambient_pad, loops=-1)
            elif not pin5_touched:
                ambient_channel.stop()
            
            time.sleep(0.05)
            
            # Update touch status
            pin2_touched = cap[2].value
            pin4_touched = cap[4].value
            pin5_touched = cap[5].value
        
        # Stop all sounds when touch is released
        bass_channel.stop()
        glitch_channel.stop()
        ambient_channel.stop()
        print("Touch released. Stopping sounds.")
    
    time.sleep(0.01)  # Small delay to prevent excessive CPU usage
