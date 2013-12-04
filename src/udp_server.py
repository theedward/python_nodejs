#!/usr/bin/env python
import sys
import socket
import time
import datetime as dt
import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = int(sys.argv[1])
BUFFER_SIZE = 256

print "UDP server listening at "+str(IP)+":"+str(PORT)+"\n"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((IP, PORT))
sock.settimeout(3)

throughputs = []
init_time = dt.datetime.now()


try:
	while True:
		total_size = 0
   		nr_chunks=0
   		avg_time_diff = 0
   		data, addr = sock.recvfrom(BUFFER_SIZE)
   	
   		time_before = dt.datetime.now()

   		if data != "":
   			nr_chunks=nr_chunks+1
   			time_after = time.localtime()
   			chunk_size = sys.getsizeof(data)
   			time_diff = (dt.datetime.now()-time_before).microseconds		
   			throughputs.append((chunk_size/time_diff))

except socket.timeout:
	sum_all=0
	for t in throughputs:
		sum_all=sum_all+t
		print t
	
	print "avg throughput: "+str(sum_all/len(throughputs)) +"MB/s"