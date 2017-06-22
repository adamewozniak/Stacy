import tweepy
import time
from Debug import countdown
from Debug import log

import SysCommands


#Automatically unfollows people that are not following back
def unfollow_all():
    
    consumer_key = SysCommands.readGlobals("TWT_KEY")
    consumer_secret = SysCommands.readGlobals("TWT_SEC")
    access_token = SysCommands.readGlobals("TWT_ACCTOKEN")
    access_secret = SysCommands.readGlobals("TWT_ACCSEC")
    
    if checkTwit(consumer_key) == False:
        return    
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)    
    
    handleUser = api.me()
    fileName = time.strftime("%Y-%m-%d_%H_%M_%S")
    fileName = "svs/unfollow_log/Unfollow_Log_" + fileName + ".txt"
    un = open(fileName, "w", 1)
    un.write("UNFOLLOW LOG\n")
    SysCommands.output("Downloading List Of Followers...")
    me = api.me()
    myName = me.screen_name
    followers = api.followers_ids(myName)
    friends = api.friends_ids(myName)
    
    i = 0
    minu = 5
    for f in friends:
        if f not in followers:
            i = i + 1
            if i != 50:
                try:
                    api.destroy_friendship(f)
                    log("Unfollowing " + api.get_user(f).screen_name, un)
                    time.sleep(3)
                except Exception:
                    log("TweepError Raised. Stalling System.", un)
                    countdown(15,0)
                    continue                
            else:
                i = 0
                log("Stalling system for a few minutes", un)
                countdown(15,0)
    log("All users unfollowed!", un)
    un.close()

#initial_function actually handles the loop for following users


#Handles operations of the initial_function
def follow_followers():
    
    consumer_key = SysCommands.readGlobals("TWT_KEY")
    consumer_secret = SysCommands.readGlobals("TWT_SEC")
    access_token = SysCommands.readGlobals("TWT_ACCTOKEN")
    access_secret = SysCommands.readGlobals("TWT_ACCSEC")
    
    if checkTwit(consumer_key) == False:
        return    
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)    
    
    handleUser = input('>> What username do you want to scan?')
    initial_function(api, handleUser)
    
def tweetThis():
    
    #Initializations 
    consumer_key = SysCommands.readGlobals("TWT_KEY")
    consumer_secret = SysCommands.readGlobals("TWT_SEC")
    access_token = SysCommands.readGlobals("TWT_ACCTOKEN")
    access_secret = SysCommands.readGlobals("TWT_ACCSEC")
    
    if checkTwit(consumer_key) == False:
        return
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    myTweet = SysCommands.hear("What would you like to tweet?")
    
    yayNay = SysCommands.hear("Your tweet says " + myTweet + ", would you like to tweet it?")
    if yayNay != "no":
        api.update_status(str(myTweet))
    SysCommands.output("Tweet sent!")

def checkTwit(consumer_key):
    if consumer_key == "und":
        SysCommands.output("Please check the README to learn how to set up Twitter with Stacy.")
        return False
    return True