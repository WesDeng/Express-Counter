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
from adafruit_seesaw.neopixel import NeoPixel

num_pixels = 9
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="det-cloud.json"
client = vision.ImageAnnotatorClient()

image = 'image.jpg'

from operator import add

directory = [
            "Apple",
            "Cheese",
            "Coke",
            "Cucumber",
            "Chocolate",
            "Water",
            "Pasta",
            "Tissue",
            "Garlic",
            "Pen",
            "Milk",
            "Egg",
            None
            ]

directory_set = {
            "Apple",
            "Cheese",
            "Coke",
            "Cucumber",
            "Chocolate",
            "Water",
            "Pasta",
            "Tissue",
            "Garlic",
            "Pen",
            "Milk",
            "Egg"
            }

sounds = [
        "apple1.wav",
        "cheese.wav",
        "coke.wav",
        "cucumber.wav",
        "chocolate.wav",
        "runningwater.wav",
        "pasta.wav",
        "runningwater.wav",
        "garlic.wav",
        "typing.wav",
        "milk.wav",
        "hen.wav"
        ]

ambient = ["summer.wav",
           "drumy.wav",
           "love.wav"
           ]

# "Textile": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
directory_dict = {
            "Circle": [0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
            "White": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "Paper": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "Tissue paper": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "Linens": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "Paper product": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "Metal": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "Water": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "Aluminum can": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "Coca-cola": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "Cola": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "Carbonated soft drinks": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "Apple": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Fruit": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Snack": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            "Pink": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Food": [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            "Material property": [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            "Plastic wrap": [0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
            "Cuisine": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "Dish": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "Comfort food": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "Farfalle": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "Junk food": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            "Label": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            "Wool": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            "Net": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            "Green": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            "Cucumber": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            "Vegetable": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            "Pen": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "Office supplies": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "Ball pen": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            "Water bottle": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "Bottle": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "Plastic": [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            "Glass": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "Transparent Material": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "Fluid": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            }

keys = list(directory_dict.keys())

def get_string(image):
    # Get the string from image we took.
    response = client.label_detection(image = image)
    labels = response.label_annotations
    predictor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    #print(len(labels))
    for label in labels:
        #print(label.description)
        if label.description in keys:
            #print(label.description)
            predictor = list(map(add, predictor, directory_dict[label.description]))

    #print(predictor)

    if len(find_index(predictor)) == 1:
        return find_index(predictor)[0]

def ocr(image):

    egg_words = ["FRESH", "OPEN", "NATURE", "BROWN", "FREE", "RANGE" "LARGE", "EGGS"]
    milk_words = ["TRADER", "JOE'S", "LACTOSE", "FREE", "WHOLE", "MILK"]
    snickers_words = ["BAR"]

    egg_score = 0
    milk_score = 0

    response = client.text_detection(image=image)
    text = response.full_text_annotation

    word_text = ""

    for page in text.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_label = ''.join([
                        symbol.text for symbol in word.symbols
                        ])

                    if word_label.strip() in egg_words:
                        egg_score += 1
                    if word_label.strip() in milk_words:
                        milk_score += 1
                    if word_label.strip() in snickers_words:
                        return 4

                    word_text += " "
                    word_text += ''.join([
                        symbol.text for symbol in word.symbols
                        ])

    if egg_score > 2 or milk_score > 2:
        if egg_score > milk_score:
            return 11
        else:
            return 10
    else:
        return None


def find_index(lst):
    m = max(lst)
    return [i for i, j in enumerate(lst) if j == m]


def takephoto(camera):
    camera.start_preview()
    sleep(.5)
    camera.capture('image.jpg')
    camera.stop_preview()

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():

    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()
    pg.mixer.set_num_channels(10)

    channel1 = pg.mixer.Channel(0)
    channel2 = pg.mixer.Channel(1)
    channel3 = pg.mixer.Channel(2)
    channel4 = pg.mixer.Channel(3)


    channels = [channel2, channel3, channel4, None]

    #channel5, channel6, channel7, channel8, channel9, channel10, None]

    ambientsound = "music16/ambient/" + ambient[random.randint(0, 2)]
    channel1.play(pg.mixer.Sound(ambientsound), loops = -1)
    channel_index = 0
    name_ind = 0
    while True:

        takephoto(camera)

        with open('image.jpg', 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)

            index = ocr(image)

            if index is None:
                index = get_string(image)

            if index is not None:
                pixels.fill(GREEN)
                pixels.show()
                time.sleep(0.5)
                label = directory[index]

                print("PREDICTION ", label)
                if sounds[index] is not None and label in directory_set:
                    directory_set.remove(label)
                    sound = "music16/effect/" + sounds[index]

                    if channels[channel_index] is not None:
                        channels[channel_index].play(pg.mixer.Sound(sound), loops = 16)
                        channel_index += 1
                        print("CHANNELS FULL - ", channel_index)
                    else:
                        channel_index = 0
                        channels[channel_index].play(pg.mixer.Sound(sound), loops = 16)
                        channel_index += 1


                pixels.fill(BLACK)
                pixels.show()
                time.sleep(1.5)

            else:
                color_chase(WHITE, 0.05)
                color_chase(BLACK, 0.05)


if __name__ == '__main__':
        main()
