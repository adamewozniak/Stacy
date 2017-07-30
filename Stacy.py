#!/usr/bin/env python3

#STACY CORE : Contains the Stacy Object, necessary for all crazy stuff

#These imports are necessary for all required packages.
import os, shutil
from random import *
import time
import speech_recognition as sr
from gtts import gTTS
import pyglet
from pygame import mixer
import pygame 
import tweepy

#Stacian Modules
import SysCommands
import weather_handler
import twitter_handler


class stacy:
    
    def __init__(self):
       
        if SysCommands.readGlobals("TALK") == "True":
            while(True):
                self.voiceAssist()
        else:
            while(True):
                self.typeAssist()
            
    def voiceAssist(self):
        # Record Audio
        r = sr.Recognizer()
        print("Stacy is listening")
        while True:
            with sr.Microphone() as source:
                #output("Say something!")
                audio = r.listen(source)
                try:
                    command = r.recognize_google(audio)
                    #OUTPUT HELPS TO SHOW COMMAND RECIEVED:    
                    #output(command)
                    if 'stacy' in command.lower():
                        #listenToUser starts listening to the person
                        self.listenToUser()
                except sr.UnknownValueError:
                    print("")
                except sr.RequestError as e:
                    SysCommands.output("Could not access Stacy's database; {0}".format(e))     
                    
                    
    def listenToUser(self):
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
                wasFound = self.commandEx(lis)
                if not wasFound:
                    SysCommands.output("Command not available.")
            except sr.UnknownValueError:
                SysCommands.output("Stacy could not understand you. Please try again!")
            except sr.RequestError as e:
                SysCommands.output("Could not access Stacy's database; {0}".format(e))    
                
        
    def commandEx(self, command):
        #output("Command recieved : " + command)
        #output(command) 
        lili = []
        with open("svs/sysRead/coms.txt") as search:
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
                    comTemp = lines[i+1].split(",")
                    for x in comTemp:
                        #Actual execution if the line, if found.
                        exec(x)
                    return True
        return False
    
    def typeAssist(self):
        commandvar = SysCommands.hear("Enter Stacy's command\n")
        commandvar = commandvar.lower()
        wasFound = self.commandEx(commandvar)
        if not wasFound:
            SysCommands.output("Command not available")        
            
