import picamera
import pygame as pg
import os

from google.cloud import vision
from time import sleep
from adafruit_crickit import crickit
import time
import signal
import sys
import re

import random
from pydub import AudioSegment

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../Downloads/DET-2019-Wesley.json"
#client = vision.ImageAnnotatorClient()
image = 'image.jpg'

# Special beats
def blank(s):
    # Create special sound clips.
    return AudioSegment.silent(duration= s*1000)

# Global list for the final results.
selected_song = []

# Pre process.
Hen = blank(10) + AudioSegment.from_wav("Hen.wav")[:5000]
Clock = blank(2) + (AudioSegment.from_wav("Clock.wav")[2000:9000]-5)
Jazz = blank(1.5) + (AudioSegment.from_wav("Jazz.wav")[:5000]-6)
Toilet = blank(5) + AudioSegment.from_wav("Toilet.wav")[:10000]
Sheep = (AudioSegment.from_wav("Sheep.wav")[:5000] + 5)
Drip = AudioSegment.from_wav("Dripping.wav")[:10000] + 6
Baby = blank(6) + AudioSegment.from_wav("Baby.wav")[:4000]

def takephoto(camera):
    # Credit DETClass5.py
    camera.start_preview()
    sleep(1.5) # Need to be adjust.
    camera.capture('image.jpg')
    camera.stop_preview()

def get_string(image):
    # Get the string from image we took.
    response = client.label_detection(image = image)
    labels = response.label_annotations
    label_test = ""

    for label in labels:
        label_text += ''.join([label.description, " "])

    if label_text:
        print('image_labeling(): {}'.format(label_text))
        return label_text
    else:
        print('image_labeling(): No Label Descriptions')

def pick_sound_by_item(label_text):
    # Pick out the audio depending on the item key words.
    for item in item_sound_lib:
        if re.search(item, label_text, re.IGNORECASE):
            return item_sound_lib[item]

def pick_sound_by_attri(label_text):
    # Pick out the audio depending on the attribute key words.
    for attri in attri_sound_lib:
        if re.search(attri, label_text, re.IGNORECASE):
            return attri_sound_lib[attri]

def add_layer_directly(prev, curr):
    # adding new layer of sound.
    # Input: string prev, string curr;
    # Output: updated.wav for the song.
    base_layer = AudioSegment.from_wav(prev)
    adding_layer = AudioSegment.from_wav(curr)

    if (len(base_layer) < len(adding_layer)): # Avoid chunking.
        print('new audio too long')
        adding_layer = adding_layer[:len(base_layer)/3]

    updated_layer = base_layer.overlay(adding_layer)
    print('adding: {}'.format(curr))
    updated_layer.export("updated.wav", format = 'wav')


def add_beats(prev, curr, count):
    base_layer = AudioSegment.from_wav(prev)
    adding_layer = AudioSegment.from_wav(curr)

    updated_layer = base_layer.overlay(adding_layer, times = count)
    print('adding: {}'.format(curr))
    updated_layer.export("updated.wav", format = 'wav')

def generating_collage(sound_list):
    #Generating the final collage of sound using the global sound_list.

def play_sound(file):
    # Take in a file and play the music.
    pg.mixer.music.load(file)
    pg.mixer.music.play()

# Sound Library to choose from in real time.

base_sound_lib = []

item_sound_lib = {"coke":"coke.wav",
            "pen":"pen.wav",
            "clock":"clock.wav"}

attri_sound_lib = {'fresh':'fresh.wav',
                    'red':'dream.wav',
                    'messy':'game.wav'}

drum_sound_lib = {'drum1.wav','drum2.wav','drum3.wav'}

def main():

    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()

    base_sound = random.choice(base_sound_lib) # Can be more complicated.
    play_sound(base_sound) # A long one to wait for begin.
    pring('waiting for begin')

    # ctrl+c to stop.
    while True:

        takephoto(camera)
        """Run a label request on a single image"""

        with open('image.jpg', 'rb') as image_file:
            #read the image file
            content = image_file.read()
            image = vision.types.Image(content=content)

            execute(image)

            time.sleep(0.1) # Play around with this.

if __name__ == '__main__':
        main()
