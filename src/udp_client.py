#!/usr/bin/env python
import sys
import socket
import time
import datetime as dt
import socket

#File handling
filename = sys.argv[1]
sendfile = open(filename,'rb')
data = sendfile.read()

print ">> "+str(filename)+", size to transfer: "+ str(sys.getsizeof(data))

IP = sys.argv[2]
PORT = int(sys.argv[3])
BUFFER_SIZE = 256
MESSAGE = data

i=1
packet=""

for byte in MESSAGE:
	packet = packet+byte
	#create chunks with 256bytes to send
	if (sys.getsizeof(packet)%BUFFER_SIZE==0):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(packet , (IP, PORT))
		packet=""

print "UDP stream done"