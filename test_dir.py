#!/usr/bin/python

import os.path
dirs = [d for d in os.listdir('/home/aditya/Desktop') if os.path.isdir(os.path.join('/home/aditya/Desktop', d))]
print dirs