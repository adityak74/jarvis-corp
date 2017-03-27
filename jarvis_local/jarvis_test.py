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
    # The followinf 3 cases can occur it has to be a file only. You can't uploa folders in google drive. So it can happen that starting letter is caps
     # or all letters are in caps or all are smallcase
    if isfile(join(current_path,str(FolderName.title()))):
        file.SetContentFile(join(current_path,str(FolderName).title()))
    elif isfile(join(current_path,str(FolderName.upper()))):
        file.SetContentFile(join(current_path,str(FolderName).upper()))
    elif isfile(join(current_path,str(FolderName.lower()))):
        file.SetContentFile(join(current_path,str(FolderName).lower()))

    file.Upload()
    msg = "Your file is uploaded on your drive"
    return question(msg)
    

@ask.intent("OpenFolder", convert={'FolderName' : str})
def open_folder(FolderName):
    global current_path
    # The followinf 6 cases can occur it can be folder or a file that user wants to open with starting letter as caps or all letters in caps or all smallcase

    if isdir(join(current_path,str(FolderName.title()))):
        current_path =  join(current_path, str(FolderName.title()))
    elif isdir(join(current_path,str(FolderName.upper()))):
        current_path =  join(current_path, str(FolderName.upper()))
    elif isdir(join(current_path,str(FolderName.lower()))):
        current_path =  join(current_path, str(FolderName.lower()))

    elif isfile(join(current_path,str(FolderName.title()))):
        if platform.system() == "Linux":
            os.system('xdg-open ' + join(current_path,str(FolderName.title())))
        elif platform.system() == "Darwin":
            os.system('open ' + join(current_path,str(FolderName.title())))
        elif platform.system() == "Windows":
            pass
            #add folder open code for current_path for Windows
    elif isfile(join(current_path,str(FolderName.upper()))):
        if platform.system() == "Linux":
            os.system('xdg-open ' + join(current_path,str(FolderName.upper())))
        elif platform.system() == "Darwin":
            os.system('open ' + join(current_path,str(FolderName.upper())))
        elif platform.system() == "Windows":
            pass
            #add folder open code for current_path for Windows
    elif isfile(join(current_path,str(FolderName.lower()))):
        if platform.system() == "Linux":
            os.system('xdg-open ' + join(current_path,str(FolderName.lower())))
        elif platform.system() == "Darwin":
            os.system('open ' + join(current_path,str(FolderName.lower())))
        elif platform.system() == "Windows":
            pass
            #add folder open code for current_path for Windows
    else: 
        msg  = "I am sorry, there is no such folder by that name"
        return question(msg)
        
    print "The current path ", current_path
    msg  = "The folder " +str(FolderName)+ "is opened for you"
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
    if not isdir(join(current_path,str(FolderName))):
        os.system('mkdir '+join(current_path,str(FolderName)))
        current_path  =  current_path
    else:
        msg  = "I am sorry there is folder already by that name. Please choose a different name"
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

@ask.intent("RenameFolder" , convert={'ofoldername' : str, 'nfoldername':str} )
def rename_folder(ofoldername, nfoldername):
    global current_path
    # The following 6 cases can occur for the older folder. It can be folder or a file with starting letter as caps or all letters in caps or all smallcase
    if isfile(join(current_path,str(ofoldername.title()))):
        old_name = join(current_path,str(ofoldername.title()))
    elif isfile(join(current_path,str(ofoldername.upper()))):
        old_name = join(current_path,str(ofoldername.upper()))
    elif isfile(join(current_path,str(ofoldername.lower()))):
        old_name = join(current_path,str(ofoldername.lower()))

    elif isdir(join(current_path,str(ofoldername.title()))):
        old_name = join(current_path,str(ofoldername.title()))
    elif isdir(join(current_path,str(ofoldername.upper()))):
        old_name = join(current_path,str(ofoldername.upper()))
    elif isdir(join(current_path,str(ofoldername.lower()))):
        old_name = join(current_path,str(ofoldername.lower()))
    
    # new_name =  join(current_path,names[1])
    print "Oldfoldername:", old_name, "newfoldername:", nfoldername 
    os.system('mv '+old_name+' '+new_name)
    msg = "I have renamed your file." 
    return question(msg)



if __name__ == '__main__':
    app.run(debug=True)