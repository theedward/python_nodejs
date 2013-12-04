#!/usr/bin/env python
import sys
import socket
import time
import datetime as dt
import socket

'''
1) Create socket
	- Set the buffer size as required
2) Listen 
3) Receive
	- While receiving, register time
	- Each chunck of 256KiB, register time and save it
4) Calculate throughput (data size vs time)
'''

TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 256

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

print "TCP server listening at "+sys.argv[1]+"\n"

try:
	throughputs = []
	total_size = 0
	nr_chunks=0
	avg_time_diff = 0
	conn, addr = sock.accept()
	print 'Connection address:', addr

	while True:
		data = conn.recv(BUFFER_SIZE)
		
		time_before = dt.datetime.now()
		if data != "":
			nr_chunks=nr_chunks+1
			time_after = time.localtime()
			chunk_size = sys.getsizeof(data)

		time_diff = (dt.datetime.now()-time_before).microseconds		
		throughputs.append((chunk_size/time_diff))

		#detects end of connection	
		if not data: 
			print "chunks of data: "+str(nr_chunks)
			break

	sum_all=0
	for t in throughputs:
		sum_all=sum_all+t
		print t

	print "avg throughput: "+str(sum_all/len(throughputs)) + "MB/s"

	print "Closing TCP connection"
	conn.close()
except socket.herror:
	print "TCP error"