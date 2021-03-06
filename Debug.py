import tweepy
import time

import SysCommands
"""

Debug.py DOCS


countdown(minutes, seconds):

   countdown() is pretty much a live time.sleep printout, which rewrites over its output, to look like it is counting down.
   
log(logging, fileCom)

   log() recieves logging, a string dictating what it's logging, and fileCom, the fileObject created by another function.
   It also outputs whatever it recieves, using SysCommands.output().

"""
def countdown(minutes, seconds):
    i=minutes
    j=seconds
    k=0
    while True:
        if(j==-1):
            j=59
            i -=1
        if(j > 9):  
            print(str(k)+str(i)+":"+str(j), end="\r")
        else:
            print(str(k)+str(i)+":"+str(k)+str(j), end="\r")
        time.sleep(1)
        j -= 1
        if(i==0 and j==-1):
            break
    if(i==0 and j==-1):
        print("Resuming...", end="\r")
        time.sleep(1)
    
#Log allows the print command and the write-to command to be called in the same statement. Quite helpful in a bunch of diffferent programs
def log(logging, fileCom):
    prefix = ""
    SysCommands.output(prefix + logging)
    fileCom.write(prefix + logging + "\n")
    