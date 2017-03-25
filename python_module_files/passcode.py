from uuid import getnode as get_mac
f =  open('/dev/random','r')
f =  f.read(10)
passcode = '' # Take starting 6 or 8 characters convert it to integer depending on the need 
for x in f:
	passcode+=str(ord(x))
mac =  str(hex(get_mac()))
print mac[2:-1] # this will print the hex format of the mac address removing the 0x and L characters in string format
print int(passcode[0:8]) # this is int 