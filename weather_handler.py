#WeatherHandler
#All Things Weather!

from pyowm import OWM

from audio_handler import say
from audio_handler import playThis
from SysCommands import deleteFolder
from SysCommands import readGlobals
from SysCommands import output

API_KEY = '48830b62de4a712567c45941557407d8'

def weatherAll():
    
    
    """
    Print out Detailed status : w.get_detailed_status(), returns string
    Print out Temperature : 
    """
    statOut()
    tempOut()
    humidOut()

def weatherObject():
    owm = OWM(API_KEY)
    obs = owm.weather_at_place(readGlobals("LOC_HERE"))
    w = obs.get_weather()
    return w

def statOut():
    w = weatherObject()
    weOut = "This location has " + w.get_detailed_status()
    output(weOut)
    
def tempOut():
    w = weatherObject()
    dic = w.get_temperature('fahrenheit')
    curTemp = "The current temperature is " + str(dic['temp']) +" degrees fahrenheit, with a high of " + str(dic['temp_max']) + ", and a low of " + str(dic['temp_min'])
    output(curTemp)
    
def windOut():
    w = weatherObject()
    dic = w.get_wind()
    curSpeed = "The wind is blowing at " + str(dic['speed']) + " miles per hour, at " + str(dic['deg']) + " degrees."
    output(curSpeed)
def humidOut():
    w = weatherObject()
    curHumid = "Humidity is at " + str(w.get_humidity()) + " percent."
    output(curHumid)
