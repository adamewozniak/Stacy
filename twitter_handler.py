import tweepy
import time
from Debug import countdown
from Debug import log

import SysCommands


#twitter_handler.py DOCS


#All functions in this handler begin by initializing the api for each user, checking whether or not that user is actually
#set up, and then printing out the function.

#Most functions use the "output("string")" function, from the SysCommands.py file.

#The Twitter handler engine is composed of these functions :

#unfollow_all() : 

    #unfollow_all() is a function which scans through all the people a twitter user is following, and unfollows those which
    #are not following a user back. This is done by filing a list of these users before processing them.
    
    #Log : Log file found under svs\unfollow_log
    
    #Error catching : Tweeperrors are the biggest problem with this script. It both has a listener for the TweepError, and also
    #a counter, which stops you after processing 250 users in a row. Stalling is for 15 minutes, and is optimal.
    
#follow_followers():
   
   #follow_followers() operates as more of a shell. It is an input mechanism for the user to directly follow any one user through 
   #strictly text input. initial_function() handles the actual process of creating lists and following, for reusability.
   
   #Log : See initial_functio()
   
   #Error catching : See initial_function()

#tweet_this():

   #tweet_this() uses the SysCommands.hear() command to ask the user what they would like to tweet.
   
   #Log : Nonexistent 
   
   #Error catching : No errors, except for initalization. See beginning of docs.
   
#intial_function(api, handleUser):

   #intial_function() is the engine of the twitter_handler follow scripts. It takes the arguments (api, handleUser). api is an object 
   #created first by another function, using the user's credentials. handleUser is a string, containing the handle of whomever
   #the user is trying to follow. It follows people based on a limit of how many people it is following, which is currently 800. 
   #(This is found by user.friend_count()) If it is below this integer, and the person which the user is trying to follow is not 
   #themselves, it attempts to unfollow them, and then follows them. This is in order to evade the tweeperror which is raised
   #when you try to follow someone which you are already following.
   
   #Log : Log file found under svs\follow_log
   
   #Error catching : Integer of 250, TweepError listener. Stalls for 15 minutes.
   
#randFollow():

   #randFollow(), so far, isn't so random. It generates a list of the people which the user is following, and then starts with the
   #first person, and begins to follow the people following those users. It requires user input, and is not fully auto. 
   #It uses the initial_function(api, handleUser) engine.

   #Log : See intitial_function
   
   #Error catching : See initial_function
   
#autoFollow():

   #autoFollow() is a version of randFollow(), which is fully autonomous, allowing a user to walk away, without management.
   #This can be dangerous, causing TweepErrors and account cancellations.
   #It uses the initial_function(api, handleUser) engine.
   
   #Log : See initial_function
   
   #Error catching : See initial_function
   
#printAcc(api):

   #printAcc() simply prints out the user account which it is accessing. It is used in initialization of most functions.
   
   #Log : Nonexistant 
   
   #Error catching : Nonexistant
   
#checkTwit(consumer_key):

   #checkTwit() checks to see if the consumer_key is still default. Used in initialization.
   
   #Log : Nonexistant
   
   #Error catching : Technically, it's supposed to catch errors, so all of it


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
    #Generating lists of followers and people following
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
