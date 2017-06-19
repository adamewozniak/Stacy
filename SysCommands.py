#SysCommands
#This file will handle commands that help with maintainance of Stacy

import os, shutil
from random import *
import time
import speech_recognition as sr
from gtts import gTTS
import pyglet
from pygame import mixer
import pygame 

from audio_handler import say

def deleteFolder(folder):
    #folder = '/path/to/folder'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)    
    output("Temporary files deleted.")

def readGlobals(globalreq):
    with open("globs.txt") as search:
        lines = search.readlines()
        #strips entire array of rightspace
        for i in range(0, len(lines)):
            lines[i] = lines[i].rstrip()    
            if globalreq in lines:
                varr = lines[i+1]
                varstring = str(varr)
                varstring = varstring.rstrip()
                return varstring
    return 0

def output(var):
    if readGlobals("WILL_SPEAK") == "True":
        # print("I AM SUPPOSED TO BE SAYING THIS!")
        say(var)
    else:
        print(var)