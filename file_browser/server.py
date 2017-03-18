import socket
from os import listdir
from os.path import isfile, join,isdir
import os
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
c.send( "hello "+recv_chat+" I am here to help you with file browsing")
current_path = "/home/prabhat/Downloads"


def open_folder(recv_chat):
	global current_path
	if isdir(join(current_path,recv_chat)):
		current_path =  join(current_path, recv_chat)
	elif isfile(join(current_path,recv_chat)):
		os.system('xdg-open ' + join(current_path,recv_chat))
	print "The current path ", current_path
	return

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
		os.system('mkdir '+recv_chat)
		current_path  =  current_path
	else:
		c.send("Hey "+user_name+ " darling there is folder already by that name please choose a different name")
	print "The current path ", current_path
	return
def delete_folder(recv_chat):
	global current_path
	if isdir(join(current_path,recv_chat)):
		os.system('rm -rf '+recv_chat )
	else:
		c.send("Hey "+user_name+ " darling there is no folder by that name please")
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
	elif recv_chat == "bye alexa":
		c.close()
		break

