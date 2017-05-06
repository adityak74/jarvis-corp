import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

###################################################################################################################################### 
pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'sub-c-56f8fe2a-0dcd-11e7-83b6-0619f8945a4f'
pnconfig.publish_key = 'pub-c-b432bbef-d96b-4a40-91d4-7ae1c6d96ee6'
 
pubnub = PubNub(pnconfig)

client_message =  ''

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        print "Published"
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            # pubnub.publish().channel("redChannel").message("hello!!").async(my_publish_callback)
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        global client_message
        client_message = ''
		# print "This is what I received from client side", message.message
        client_message = message.message  
        print "this is what I received from client: ",client_message      
		# pass  # Handle new message stored in message.message

  
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('blueChannel').execute()



##################################################################################################################################
PASSCODE = 0

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def file_browser():
    welcome_msg = "Welcome Please say your passcode ?"
    print "---------------------------",welcome_msg,"---------------------------"
    return question(welcome_msg)

@ask.intent("PassCodeIntent", convert = {'Passcode':int})
def passcode(Passcode):
    global PASSCODE
    print Passcode
    PASSCODE = Passcode
    # Call digital ocean and get the respective pascodes cannels. If not found return response incorrect passcode
    # Set the passcode and channel names in session, with pascode as key and channels as values or any other logic but that needs to be there in the session
    # We also have to include one more flow if the user forgets his passcode.
    msg = "You are verified. What can I do for you"
    return question(msg)

@ask.intent("UploadDrive", convert={'FolderName' : str})
def upload_drive(FolderName):
    global client_message
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "drive",
            "value"  : str(FolderName)
    }
    pubnub.publish().channel('redChannel').message(data).async(my_publish_callback)
    while not client_message:
        continue
    ret_mesg = client_message
    client_message = ""
    return question(ret_mesg)


@ask.intent("OpenFolder", convert={'FolderName' : str})
def open_folder(FolderName):
    global client_message
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "open",
            "value"  : str(FolderName)
    }
    pubnub.publish().channel('redChannel').message(data).async(my_publish_callback)
    while not client_message:
        continue
    ret_mesg = client_message
    client_message = ""
    return question(ret_mesg)


@ask.intent("GoBack")
def go_back():
    global client_message
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "goback",
            "value"  : None
    }
    pubnub.publish().channel('redChannel').message(data).async(my_publish_callback) 
    while not client_message:
        continue
    ret_mesg = client_message
    client_message = ""
    return question(ret_mesg)



@ask.intent("CreateFolder" , convert={'FolderName' : str})
def create_folder(FolderName):
    global client_message
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "create",
            "value"  : str(FolderName)
    }
    pubnub.publish().channel('redChannel').message(data).async(my_publish_callback)
    while not client_message:
        continue
    ret_mesg = client_message
    client_message = ""
    return question(ret_mesg)

# @ask.intent("DeleteFolder")    

@ask.intent("RenameFolder" , convert={'ofoldername' : str, 'nfoldername':str} )
def rename_folder(ofoldername, nfoldername):
    global client_message
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "rename",
            "value"  : {'oldfoldername':str(oldfoldername),'newfoldername':str(nfoldername)}
    }
    pubnub.publish().channel('redChannel').message(data).async(my_publish_callback)
    while not client_message:
        continue
    ret_mesg = client_message
    client_message = ""
    return question(ret_mesg)

if __name__ == '__main__':
    app.run(debug=True)