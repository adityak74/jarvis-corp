import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import jarvis_pubnub


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
    # print type(Passcode)
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
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    

@ask.intent("OpenFolder", convert={'FolderName' : str})
def open_folder(FolderName):
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "open",
            "value"  : str(FolderName)
    }
    jarvis_pubnub.pubnub.publish().channel('awesomeChannel').message(data).async(jarvis_pubnub.my_publish_callback)
    msg = "Opened folder " + str(FolderName)
    return question(msg)
    


@ask.intent("GoBack")
def go_back():
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "goback",
            "value"  : None
    } 
    msg = "Go back done."
    return question(msg)   


@ask.intent("CreateFolder" , convert={'FolderName' : str})
def create_folder(FolderName):
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "create",
            "value"  : str(FolderName)
    }

# @ask.intent("DeleteFolder")    

@ask.intent("RenameFolder" , convert={'ofoldername' : str, 'nfoldername':str} )
def rename_folder(ofoldername, nfoldername):
    # Check if passcode is set in the session or not. Else return with proper messsage.  This Logic needs more work
    if not PASSCODE:
        msg = "You haven't verified your password. Please say you passcode. Thank You"
        return question(msg)
    data = {
            "intent" : "rename",
            "value"  : {'oldfoldername':str(oldfoldername),'newfoldername':str(nfoldername)}
    }

if __name__ == '__main__':
    app.run(debug=True)