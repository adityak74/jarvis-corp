import socket
import platform
from os import listdir
from os.path import isfile, join,isdir
import os
import getpass
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
print 'Got connections from', addr
recv_chat= c.recv(8192)
user_name =  recv_chat
c.send( "Hello "+recv_chat+" I am here to help you with file browsing")

# Add case for windows, platform.system() for Windows returns 'Windows' as string

if platform.system() == "Linux":
	current_path = "/home/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Darwin":
	current_path = "/Users/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Windows":
	pass
	#add folder path structure here for windows


def open_folder(recv_chat):
	global current_path
	if isdir(join(current_path,recv_chat)):
		current_path =  join(current_path, recv_chat)
	elif isfile(join(current_path,recv_chat)):
		if platform.system() == "Linux":
			os.system('xdg-open ' + join(current_path,recv_chat))
		elif platform.system() == "Darwin":
			os.system('open ' + join(current_path,recv_chat))
		elif platform.system() == "Windows":
			pass
			#add folder open code for current_path for Windows
	print "The current path ", current_path
	return

def upload_drive(recv_chat):
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
	file.SetContentFile(join(current_path,recv_chat))
	file.Upload()

def go_back():
	global current_path
	if not current_path.rindex('/'):
		current_path = '/'
	else:	
		current_path =  current_path[:current_path.rindex('/')]
	print "The current path ", current_path
	return

def create_folder(recv_chat):
	global current_path
	if not isdir(join(current_path,recv_chat)):
		os.system('mkdir '+join(current_path,recv_chat))
		current_path  =  current_path
	else:
		c.send("Hey "+user_name+ " darling there is folder already by that name please choose a different name")
	print "The current path ", current_path
	return
def delete_folder(recv_chat):
	global current_path
	if isdir(join(current_path,recv_chat)):
		os.system('rm -rf '+join(current_path,recv_chat))
	else:
		c.send("Hey "+user_name+ " darling there is no folder by that name please")
	return

def rename_folder(recv_chat):
	global current_path
	names =  recv_chat.split(' ')
	old_name = join(current_path,names[0])
	new_name =  join(current_path,names[1])
	print old_name,new_name 
	os.system('mv '+old_name+' '+new_name)
	return

while True:
	send_chat=''
	if not listdir(current_path):
		c.send("Hey "+ user_name + " darling this is an empty directory")
		recv_chat = c.recv(8192)
		if "create" in recv_chat:
			recv_chat = recv_chat[14:]
			create_folder(recv_chat)
		else:
			go_back()
	for f in listdir(current_path):
		send_chat+=f+'$'
	c.send(send_chat)
	recv_chat = c.recv(8192)
	print "Client wants to do this action:", recv_chat
	if "open" in recv_chat:
		recv_chat = recv_chat[5:]
		open_folder(recv_chat)
	if recv_chat == "go back":
		go_back()
	if 'create folder' in recv_chat:
		recv_chat = recv_chat[14:]
		create_folder(recv_chat)		
	if "delete folder" in recv_chat:
		recv_chat = recv_chat[14:]
		delete_folder(recv_chat)
	if "rename folder" in recv_chat:
		recv_chat = recv_chat[14:]
		rename_folder(recv_chat)
	if "google drive" in recv_chat:
		recv_chat = recv_chat[13:]
		upload_drive(recv_chat)
	elif recv_chat == "bye Alexa":
		c.close()
		break

