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
import audio_handler
from audio_handler import say


#SysCommands.py DOCS

#SysCommands handles the commands to interface with the Stacy object, and generic other operations.

#deleteFolder(folder):

   #deleteFolder() is used to delete temporary files in Stacy. It should be used to clear out the system on boot.
   
#readGlobals(globalreq):

   #readGlobals() returns the string value of any variable in the svs/sysRead/globs.txt file.
   #It allows for the program to be saved and changed while live, as all variables are read during operations.
   
#output(var):

   #output() gets a string, and dictates whether to say it using text, or Stacy's voice. This is dictated by readGlobals().
   
#hear(outty):
   
   #hear() uses readGlobals(), listenin(), and notListenin() in order to either ask a user what they want to say from the speakers,
   #or out through text.
   


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
    with open("svs/sysRead/globs.txt") as search:
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
        
def listenin():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            lis = r.recognize_google(audio)
        except sr.UnknownValueError:
            output("Stacy could not understand you. Please try again!")
        except sr.RequestError as e:
            output("Could not access Stacy's database; {0}".format(e))    
    return lis

def notListenin():
    x = input()
    return x
"""
HEAR IS CALLED WHENEVER A FUNCTION NEEDS SEPARATE INPUT
IT READS IN GLOBALS FROM GLOBS.TXT TO SEE IF IT WILL USE VOICE
RECOGNITION, OR TEXT INPUT
"""

def hear(outty):
    
    output(outty)
    if readGlobals("TALK") == "True":
        audio_handler.playThis("listening.mp3")
        ret = listenin()
    else:
        print(">> ")
        ret = notListenin()
    
    return ret