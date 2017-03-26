import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import socket
import platform
from os import listdir
from os.path import isfile, join,isdir
import os
import getpass
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


if platform.system() == "Linux":
    current_path = "/home/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Darwin":
    current_path = "/Users/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Windows":
    pass
    # add folder path structure here for windows



@ask.launch
def file_browser():
    # welcome_msg = render_template('welcome')
    welcome_msg = "Welcome,"+ getpass.getuser() + "! what can I do for you ?"
    print "---------------------------",welcome_msg,"---------------------------"
    return question(welcome_msg)

@ask.intent("UploadDrive", convert={'FolderName' : str})
def upload_drive(FolderName):
    global current_path
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.txt")

    drive = GoogleDrive(gauth)
    file = drive.CreateFile()
    file.SetContentFile(join(current_path,str(FolderName)))
    file.Upload()
    return question(msg)
    

@ask.intent("OpenFolder", convert={'FolderName' : str})
def open_folder(FolderName):
    global current_path
    if isdir(join(current_path,str(FolderName))):
        current_path =  join(current_path, str(FolderName))
    elif isfile(join(current_path,str(FolderName))):
        if platform.system() == "Linux":
            os.system('xdg-open ' + join(current_path,str(FolderName)))
        elif platform.system() == "Darwin":
            os.system('open ' + join(current_path,str(FolderName)))
        elif platform.system() == "Windows":
            pass
            #add folder open code for current_path for Windows
    else: 
        msg  = "I am sorry, there is no such folder by that name"
        return question(msg)
        
    print "The current path ", current_path
    msg  = "The folder" +str(FolderName)+ "is opened for you"
    return question(msg)
    


@ask.intent("GoBack")
def go_back():
    global current_path
    if not current_path.rindex('/'):
        current_path = '/'
    else:   
        current_path =  current_path[:current_path.rindex('/')]
    print "The current path ", current_path
    msg = "This is the previous folder"
    return question(msg)

@ask.intent("CreateFolder" , convert={'FolderName' : str})
def create_folder(FolderName):
    global current_path
    if not isdir(join(current_path,recv_chat)):
        os.system('mkdir '+join(current_path,recv_chat))
        current_path  =  current_path
    else:
        msg  = "I am sorry" + + "there is folder already by that name. Please choose a different name"
        return question(msg)
    print "The current path ", current_path
    msg  = "I have created a folder by the name"
    return question(msg)
    

# @ask.intent("DeleteFolder")    
# def delete_folder():
    
#     return question(msg)
    # global current_path
    # if isdir(join(current_path,recv_chat)):
    #     os.system('rm -rf '+join(current_path,recv_chat))
    # else:
    #     c.send("Hey "+user_name+ " darling there is no folder by that name please")
    # return

@ask.intent("RenameFolder")
def rename_folder():
    
    return question(msg)
    # global current_path
    # names =  recv_chat.split(' ')
    # old_name = join(current_path,names[0])
    # new_name =  join(current_path,names[1])
    # print old_name,new_name 
    # os.system('mv '+old_name+' '+new_name)
    # return



if __name__ == '__main__':
    app.run(debug=True)