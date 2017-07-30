#Program handles audio for Stacy

import os, shutil
from random import *
import time
import speech_recognition as sr
from gtts import gTTS
import pyglet
from pygame import mixer
import pygame 

#Will play a song of any given string, and then stop until song ends -- not fully dev'd
def playThis(mp3Name):
    mixer.init()
    mixer.music.load(mp3Name)
    mixer.music.play(0)
    while mixer.music.get_busy():
        time.sleep(0.0002)

#Say is not that efficient. It creates a completely random number in front of a temp name, and then saves it.
#Awkward. Just glad that there's a method for taking this junk out.
def say(stacysay):
    tts = gTTS(text=stacysay, lang='en')
    #For now, let's just create random-ass filenames. Dope.
    tempName = "temp.mp3"
    tempName = str(randint(1,1000)) + str(randint(1,1000)) + str(randint(1,1000)) + tempName
    tempName = "temp/" + tempName
    tts.save(tempName)
    playThis(tempName)
    
