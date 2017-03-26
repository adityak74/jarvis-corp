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


# if platform.system() == "Linux":
#     current_path = "/home/"+ getpass.getuser() +"/Downloads/"
# elif platform.system() == "Darwin":
#     current_path = "/Users/"+ getpass.getuser() +"/Downloads/"
# elif platform.system() == "Windows":
#     pass
    #add folder path structure here for windows



@ask.launch
def file_browser():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("UploadDrive")
def upload_drive():
    msg = render_template('upload')
    return question(msg)
    # global current_path
    # gauth = GoogleAuth()
    # gauth.LoadCredentialsFile("credentials.txt")
    # if gauth.credentials is None:
    #     # Authenticate if they're not there
    #     gauth.LocalWebserverAuth()
    # elif gauth.access_token_expired:
    #     # Refresh them if expired
    #     gauth.Refresh()
    # else:
    #     # Initialize the saved creds
    #     gauth.Authorize()
    # # Save the current credentials to a file
    # gauth.SaveCredentialsFile("credentials.txt")

    # drive = GoogleDrive(gauth)
    # file = drive.CreateFile()
    # file.SetContentFile(join(current_path,recv_chat))
    # file.Upload()


@ask.intent("OpenFolder")
def open_folder():
    msg = render_template('open')
    return question(msg)
    # global current_path
    # if isdir(join(current_path,recv_chat)):
    #     current_path =  join(current_path, recv_chat)
    # elif isfile(join(current_path,recv_chat)):
    #     if platform.system() == "Linux":
    #         os.system('xdg-open ' + join(current_path,recv_chat))
    #     elif platform.system() == "Darwin":
    #         os.system('open ' + join(current_path,recv_chat))
    #     elif platform.system() == "Windows":
    #         pass
    #         #add folder open code for current_path for Windows
    # print "The current path ", current_path
    # return

@ask.intent("GoBack")
def go_back():
    msg = render_template('goback') 
    return question(msg)   
    # global current_path
    # if not current_path.rindex('/'):
    #     current_path = '/'
    # else:   
    #     current_path =  current_path[:current_path.rindex('/')]
    # print "The current path ", current_path
    # return

@ask.intent("CreateFolder")
def create_folder():
    msg = render_template('create')
    return question(msg)
    # global current_path
    # if not isdir(join(current_path,recv_chat)):
    #     os.system('mkdir '+join(current_path,recv_chat))
    #     current_path  =  current_path
    # else:
    #     c.send("Hey "+user_name+ " darling there is folder already by that name please choose a different name")
    # print "The current path ", current_path
    # return

@ask.intent("DeleteFolder")    
def delete_folder():
    msg = render_template('delete')
    return question(msg)
    # global current_path
    # if isdir(join(current_path,recv_chat)):
    #     os.system('rm -rf '+join(current_path,recv_chat))
    # else:
    #     c.send("Hey "+user_name+ " darling there is no folder by that name please")
    # return

@ask.intent("RenameFolder")
def rename_folder():
    msg = render_template('rename')
    return question(msg)
    # global current_path
    # names =  recv_chat.split(' ')
    # old_name = join(current_path,names[0])
    # new_name =  join(current_path,names[1])
    # print old_name,new_name 
    # os.system('mv '+old_name+' '+new_name)
    # return



# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
# def answer(first, second, third):
#     # print convert['first'], convert['second'], convert['thrid']
#     winning_numbers = session.attributes['numbers']
#     print winning_numbers
#     if [first, second, third] == winning_numbers:
#         msg = render_template('win')
#     else:
#         msg = render_template('lose')
#     return question(msg)

if __name__ == '__main__':
    app.run(debug=True)