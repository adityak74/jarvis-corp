from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


import platform
from os import listdir
from os.path import isfile, join,isdir
import os
import getpass
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

if platform.system() == "Linux":
	current_path = "/home/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Darwin":
	current_path = "/Users/"+ getpass.getuser() +"/Downloads/"
elif platform.system() == "Windows":
	pass


###################################################################################################################################### 
pnconfig = PNConfiguration()
# These two keys has to be read from some configuration file and put here
# For the time being its hard coded but this part of the code needs change
pnconfig.subscribe_key = 'sub-c-56f8fe2a-0dcd-11e7-83b6-0619f8945a4f'
pnconfig.publish_key = 'pub-c-b432bbef-d96b-4a40-91d4-7ae1c6d96ee6'
 
pubnub = PubNub(pnconfig)

server_message = ''

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
		global server_message
		print "This is what I received from the server side", message.message
		if message.message['intent'].encode('ascii','ignore') == 'open':
			server_message = open_folder(message.message['value'].encode('ascii','ignore'))
		elif message.message['intent'].encode('ascii','ignore') == 'drive':
			server_message = upload_drive(message.message['value'].encode('ascii','ignore'))
		elif message.message['intent'].encode('ascii','ignore') == 'goback':
			server_message = go_back()
		elif message.message['intent'].encode('ascii','ignore') == 'create':
			server_message = create_folder(message.message['value'].encode('ascii','ignore'))
		elif message.message['intent'].encode('ascii','ignore') == 'rename':
			server_message = rename_folder(message.message['value'].encode('ascii','ignore'))

		# For the time being this channel names are hard coded they need to be made dyamic based on server management logic
		print "This is before publishing to server : ", server_message
		pubnub.publish().channel('blueChannel').message(server_message).async(my_publish_callback)
		pass  # Handle new message stored in message.message

  
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('redChannel').execute()



##################################################################################################################################
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
	return msg
##################################################################################################################################

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
		return msg
		
	print "The current path ", current_path
	# msg  = "The folder " +str(FolderName)+ " is opened for you"
	msg = str(current_path)
	return msg
##################################################################################################################################
def go_back():
	global current_path
	if not current_path.rindex('/'):
		current_path = '/'
	else:   
		current_path =  current_path[:current_path.rindex('/')]
	print "The current path ", current_path
	msg = str(current_path)
	# msg  = "I have created a folder by the name"
	return msg
##################################################################################################################################

def create_folder(FolderName):
	global current_path
	if not isdir(join(current_path,str(FolderName))):
		os.system('mkdir '+join(current_path,str(FolderName)))
		current_path  =  current_path
	else:
		msg  = "I am sorry there is folder already by that name. Please choose a different name"
		return msg
	print "The current path ", current_path
	msg = str(current_path)
	# msg  = "I have created a folder by the name"
	return msg
##################################################################################################################################
# def delete_folder():
	# global current_path
	# if isdir(join(current_path,recv_chat)):
	#	 os.system('rm -rf '+join(current_path,recv_chat))
	# else:
	#	 c.send("Hey "+user_name+ " darling there is no folder by that name please")
	# return
##################################################################################################################################
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
	return msg
##################################################################################################################################
	
