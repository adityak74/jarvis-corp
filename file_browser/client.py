import socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))

send_chat= "Prabhat"
s.send(send_chat)
print s.recv(8192)

while True:
	recv_chat = s.recv(8192)
	if '$' not in recv_chat:
		print recv_chat
		if 'empty' in recv_chat:
			# send_chat = ''
			while 1:
				send_chat =  raw_input("Create a new folder or go back:")
				print "This is what you entered", send_chat
				if send_chat == "go back" or  "create" in send_chat:
					print "You entered correct command"
					s.send(send_chat)
					break
				else:	
					print "It came here"
					continue	
		continue
	all_files= recv_chat.split('$')
	for fily in all_files:
		print fily
	send_chat =  raw_input("Type the folder/file name you want:")
	if send_chat == "bye Alexa":
		s.send(send_chat)
		s.close() 
		break 
	s.send(send_chat)