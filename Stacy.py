#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
# Also requires pygame, gtts, PyOWM

#STACY CORE : This is the core of who stacy is, and how exactly she reads in commands.
#Most of the commands are 

#These imports are necessary for all required packages.
import os, shutil
from random import *
import time

import speech_recognition as sr
from gtts import gTTS
import pyglet
from pygame import mixer
import pygame 

#THESE ARE THE INCLUDED PYTHON MODULES FOR STACY
from audio_handler import say
from audio_handler import playThis
from SysCommands import deleteFolder
from SysCommands import readGlobals
import weather_handler
from SysCommands import output

    
def fileSearcher(command):
    #output("Command recieved : " + command)
    #output(command) 
    lili = []
    with open("coms.txt") as search:
        lines = search.readlines()
        #strips entire array of rightspace
        for i in range(0, len(lines)):
            lines[i] = lines[i].rstrip()
        #searches through and attempts to see 
        for i in range(0, len(lines)):
            #creates a list of the commands, separated by commas
            lili = lines[i].split(",")
            #Enable to print proof of recieved list of commands
            #output(lili)
            
            if command in lili:
                exec(lines[i+1])
                return True
    return False
        
#Recieves input from the microphone, after initial call.
#Runs it through fileSearcher, which returns False if it isn't there
#If it is not in the program it tells the user that the command is not found
def startUp():
    r = sr.Recognizer()
    mixer.init()
    mixer.music.load('listening.mp3')
    mixer.music.play(0)    
    
    #output("What do you need?")
    
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            lis = r.recognize_google(audio)
            lis = lis.lower()
            wasFound = fileSearcher(lis)
            if not wasFound:
                output("Command not available.")
        except sr.UnknownValueError:
            output("Stacy could not understand you. Please try again!")
        except sr.RequestError as e:
            output("Could not access Stacy's database; {0}".format(e))
            
# Handles the primary call to stacy. Bypassed by typeTester for debugging.            
def main():
    # Record Audio
    r = sr.Recognizer()
    print("Stacy is listening")
    while True:
        with sr.Microphone() as source:
            #output("Say something!")
            audio = r.listen(source)
            
            try:
                
                command = r.recognize_google(audio)
                #output(command)
                if 'stacy' in command.lower():
                    startUp()
            except sr.UnknownValueError:
                print("")
            except sr.RequestError as e:
                output("Could not access Stacy's database; {0}".format(e))
                
# Bypasses any vocal input from the user, as this is all handled the same.
def typeTester():
    while True:
        commandvar = input("Enter Stacy's command\n")
        commandvar = commandvar.lower()
        wasFound = fileSearcher(commandvar)
        if not wasFound:
            output("Command not available")

main()
