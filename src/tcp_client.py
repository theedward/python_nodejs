#!/usr/bin/env python
import sys
import socket
import time
import socket

'''
1) Create socket
  - Set the buffer size as required
2) Open file
3) Send file
'''

#File handling
filename = sys.argv[1]
sendfile = open(filename,'rb')
data = sendfile.read()

print ">> "+str(filename)+", size to transfer: "+ str(sys.getsizeof(data))

#SOCKET handling
TCP_IP = sys.argv[2]
TCP_PORT = int(sys.argv[3])
BUFFER_SIZE = 256
MESSAGE = data

#Send data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

s.close()
print "TCP connection closed"