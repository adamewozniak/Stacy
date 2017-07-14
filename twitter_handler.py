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
    printAcc(api)
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
    for f in friends:
        if f not in followers:
            i = i + 1
            if i != 250:
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
    printAcc(api)
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
    printAcc(api)
    myTweet = SysCommands.hear("What would you like to tweet?")
    
    yayNay = SysCommands.hear("Your tweet says " + myTweet + ", would you like to tweet it?")
    if yayNay != "no":
        api.update_status(str(myTweet))
    SysCommands.output("Tweet sent!")
def initial_function(api, handleUser):
    
    fileName = time.strftime(handleUser + "_%Y-%m-%d_%H_%M_%S")
    fileName = "svs/follow_log/FollowLog_" + fileName + ".txt"
    f = open(fileName, "w", 1)
    
    f.write("LOG : Following from " + handleUser)
    
    #scans for my ID, and ensures to NOT FOLLOW said ID
    me = api.me()
    myid = me.id
    
    
    SysCommands.output("Scanning users...")
    i = 1
    modulur = 0
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=handleUser).pages():
        ids.extend(page)

    for x in ids:
        modulur = i % 250
        if modulur == 0:
            log("Integer hit 250x. Stalling System.", f)
            countdown(15,0)
        user = api.get_user(x)
        if user.id != myid:
            if user.friends_count < 800:
                api.destroy_friendship(user.screen_name)
                try:
                    user.follow()
                    log("Followed : " + user.screen_name, f)
                    
                except Exception:
                    log("TweepError Raised. Stalling System.", f)
                    countdown(15,0)
                    continue
            else:
                log("Skipped - Over Limit : " + user.screen_name + "", f)
                
        else:
            log("I was skipped!", f)
        
        i = i + 1
    log("All users followed!", f)
    f.close()
    
def randFollow():
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
    printAcc(api)
    SysCommands.output("Downloading List Of Followers...")
    me = api.me()
    
    myName = me.screen_name
    #SysCommands.output("Entering Loop")
    #ERROR with snagg.io account : cannot scan list of followers
    followers = api.followers_ids(myName)
    
    friends = api.friends_ids(myName)
    amountFollowing = 0
    
    amountFollowersTemp = 0
    
    #Loop goes through followers and finds one with less than 500 people following to follow
    for f in followers:
        
        followersTemp = api.followers_ids(f)
        #print(f)
        for x in followersTemp:
            amountFollowersTemp += 1
        if amountFollowersTemp < 500:
            userEx = api.get_user(f)
            choice = SysCommands.hear("Follow " + str(amountFollowersTemp) + " users from " + userEx.screen_name + "?")
            if choice == "yes" or choice == "Yes" :
                initial_function(api, userEx.screen_name)
                break

def autoFollow():
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
    
    SysCommands.output("Downloading List Of Followers...")
    me = api.me()
    printAcc(api)
    myName = me.screen_name

    #SysCommands.output("Entering Loop")
    #ERROR with snagg.io account : cannot scan list of followers
    followers = api.followers_ids(myName)
    friends = api.friends_ids(myName)
    
    amountFollowing = 0
    
    amountFollowersTemp = 0
    
    #Loop goes through followers and finds one with less than 500 people following to follow
    for f in followers:
        followersTemp = api.followers_ids(f)
        #print(f)
        for x in followersTemp:
            amountFollowersTemp += 1
        if amountFollowersTemp < 500:
            userEx = api.get_user(f)
            SysCommands.output("Following users from account " + userEx.screen_name)
            initial_function(api, userEx.screen_name)
            SysCommands.output("Stalling in between scans")
            countdown(30,0)
            
            
#Functions called to help controllers
def printAcc(api):
    user = api.me()
    myName = user.screen_name
    SysCommands.output("Accessing user " + myName)
    
def checkTwit(consumer_key):
    if consumer_key == "undas":
        SysCommands.output("Please check the README to learn how to set up Twitter with Stacy.")
        return False
    return True
