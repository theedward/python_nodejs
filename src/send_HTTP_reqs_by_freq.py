#!/usr/bin/python

import httplib
import sys
import hashlib
import time
import random
from datetime import datetime 
from threading import Thread

def request(parameter, round):
	try:
		c = httplib.HTTPConnection("130.233.42.118", 9999, timeout=120)
		c.request("GET", "/" + str(parameter))
		start_t = datetime.now()
#		print start_t
		response = c.getresponse()
		data = response.read()
#		print data
		delta_t = datetime.now() - start_t
#		print delta_t
		c.close()
		print(str(round) + "\t" + str(delta_t.total_seconds()))
	except:
		print(str(round) + "\t" + "failed")

def hash():
        line = ""
	for i in xrange(0,3):
		line += chr(random.randint(30,128))
        linecrypt = hashlib.sha1(line).hexdigest()
        #print ("Hash --> "+ linecrypt )
        return linecrypt   

def main():
	if len(sys.argv) < 3:
        	print "Wrong command line, program will be terminated."
	        sys.exit()

	if len(sys.argv) > 3:
	        print "Wrong command line, program will be terminated."
		sys.exit()

	else:

       #frequency and period
	        global freq
    		freq = int(sys.argv[1])
        	p = 60/freq
		rep_num = -1
        #time period of the test
		if len(sys.argv) == 3:
	       		 rep_num = int(sys.argv[2])
		#print("Requests are being sent." + str(freq) + "/rep_num" + " " + str(p))
	
		sent = 0
		threads = []
		global finish
#		print "Entering while"
		while(rep_num == -1 or sent < rep_num) and not finish:
#			print "Broke here:1"
			time.sleep(60.0 / freq)
#			print "Broke here:2" 
			sent+=1
#			print "Thread will start"
			thread = Thread(target = request, args = (hash(), sent))
			thread.start()
			threads.append(thread)
#		print "End of while"
		for thread in threads:
			thread.join()

freq = 15
finish = False
main()
