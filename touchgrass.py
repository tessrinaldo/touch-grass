import serial
import pygame
import time
import random 

# Initialize Pygame mixer
pygame.mixer.init()

# sounds = ["moan1.wav", "moan2.wav", "moan3.wav"]
sounds_dir = ["sounds"]
sound_files = ["jingle4.mp3"]

# Load the MP3 file

# Open the serial port
ser = serial.Serial('/dev/tty.usbmodem21401', 9600)  # Replace 'COM3' with your Arduino's serial port

def play_mp3():
    pygame.mixer.music.load(sounds_dir + sound_files[random.randint(0,2)])
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)

last_touched = False

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line == "Touched" and not last_touched:
          print("you touched me!!!")
          play_mp3()
          last_touched = True
        elif line != "Touched":
          # print("you didn't touch me..")
          last_touched = False
    
    # # Check if the mp3 file has stopped playing
    # if not pygame.mixer.music.get_busy() :
    #   last_touched = False

    time.sleep(0.1)
