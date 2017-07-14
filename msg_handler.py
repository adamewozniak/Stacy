#NEEDS TWILIO

from twilio.rest import Client
from SysCommands import output
import SysCommands

def texter():
    reciever = SysCommands.hear("What number do you want to text?")
    message = SysCommands.hear("What would you like the message to say?")

    
    account_sid = "AC9fcbc5555c41af3be98d0f650ef1a8c9"#str(SysCommands.readGlobals("MSG_SID"))
    auth_token = "5c886cda9e7e32631ae5288caf16f78b"#str(SysCommands.readGlobals("MSG_TOKEN"))
    number = "+17028197227"#str(SysCommands.readGlobals("MSG_NUM"))
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to = str(reciever),
        from_ = number,
        body = "yoyoy")
    
texter()