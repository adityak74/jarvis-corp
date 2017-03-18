import os
for root, dirs, files in os.walk("/home/prabhat/Downloads/", topdown=True):
    # for name in files:
    #     print(os.path.join(root, name))
    # for name in dirs:
    #     print(os.path.join(root, name))
    for  diry in dirs:
    	print "\nThis is the file name:", diry
    	current_folder =  os.path.join(root,diry)
    	current_command  =  "nautilus "+ current_folder
    	print "Current",current_folder,current_command
    	os.system(current_command)