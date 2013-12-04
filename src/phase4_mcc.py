from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urllib2
import sys
import time
import cgi

host_name = '127.0.0.1';
port_number = 66006;
workload_limits = [30,60,90]

current_workers = []
current_requests = 0
instance_name_count = 1

#Credentials
USER_NAME = 'mccgroup09'
PASSWORD = 'W92HoMR37c'
PROJECT_NAME = 'mobile_cloud_computing_2'
URL = 'http://echo.niksula.hut.fi:5000/v2.0/'
#Public key
PUB_KEY_PATH = '~/.ssh/mobClCompRSAKey.pub'
PUB_KEY = 'key_pair'

class Worker:
    pend_req = 0
    instance= ""

    def __init__ (self, instance):
        self.pend_req = 0
        self.instance = instance
        # get IP
        ip_address = re.findall( r'[0-9]+(?:\.[0-9]+){3}', str(self.instance.networks))[0];
        # Start node
        port = 9999;
        conn_url = 'ssh -i group09.pem ubuntu@'+str(ip_address)+' node pw_breaker.js '+str(port)
        p = Popen(conn_url, shell=True, stdout=PIPE)
    
    def get_pend_req(self):
        return self.pend_req
    
    def get_instance(self):
        return instance;

    def incr_pend_req(self): 
        self.pend_req = self.pend_req + 1;
    
    def decr_pend_req(self):
        self.pend_req = self.pend_req - 1;
    
def get_happiest_worker(list_workers):
    hap = list_workers[0]
    for worker in list_workers:
        if (worker.get_pend_req() < hap.get_pend_req()):
            hap = worker
    return hap;

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        val = self.raw_requestline.split('/')[1];
        val = val.split(' ')[0];
        hap = get_happiest_worker(current_workers);
        addr = hap.addr;
        print "----->>>> Request forwarded to {}\n".format(addr);
        req = addr + '/' + val;
		current_requests += 1;
        hap.incr_pend_req();
        recv = urllib2.urlopen(req).read();
        hap.decr_pend_req();
        current_requests -= 1;
        print "  <<<<----- Response from {} = {}\n".format(addr, recv);
        print "------------>>>> Returning to {}\n".format(self.client_address);
        self.wfile.write(recv);
        return;
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def get_nova_client():
	NOVA_CLIENT = nvclient.Client(USER_NAME, PASSWORD, PROJECT_NAME, URL)
	return NOVA_CLIENT 

def hireWorker():
	instance_name = 'test_'+str(instance_name_count)
	instance_name_count = instance_name_count + 1

    nova_client = get_nova_client();
    if not nova_client.keypairs.findall(name=PUB_KEY):
    		with open(os.path.expanduser(PUB_KEY_PATH)) as fpubkey:
        		nova_client.keypairs.create(name=PUB_KEY, public_key=fpubkey.read())
	snapshot = nova_client.images.find(name="mcc2013")
	flavor = nova_client.flavors.find(name="m1.tiny")
	instance = nova_client.servers.create(name=instance_name, image=snapshot, flavor=flavor, key_name=PUB_KEY)
	status = instance.status
	while status == 'BUILD':
    		time.sleep(5)
    		# Retrieve the instance again so the status field updates
    		instance = nova_client.servers.get(instance.id)
	    	status = instance.status
	print "status: %s" % status
	current_workers.append(Worker(instance));
    

def fireWorker():
    nova_client = get_nova_client();
    # Check if any worker is currently not proccessing any request
    free = None;
    for worker in current_workers:
        if worker.get_pend_req == 0:
            server = nova_client.servers.find(name=worker.get_instance());
            server.delete();
            

def monitor ():
    while 1:
        if current_req <= workload_limits[0]:   
            #There should be 1 instance running
            while len(current_workers) > 1: # Delete instances
                fireWorker();
        elif (current_requests > workload_limits[0] and current_requests <= workload_limits[1]):
            #There should be 2 instances running
            if len(current_workers) < 2:   # Boot 1 instance
                hireWorker();
            elif len(current_workers > 2:   # Delete 1 instance
                fireWorker();
        else:  
            #There should be 3 instances running
            while len(current_workers) < 3: # Boot instances
                hireWorker();


if __name__ == '__main__':
    server = ThreadedHTTPServer((host_name, port_number), Handler);
    
	#Binding load balancer with the floating IP machine
    nova_client = get_nova_client()
	instance = nova_client.servers.find(name="group09")
    current_balancer = instance
	
	#hire the first worker
    hireWorker()
	
    print 'Starting server, use <Ctrl-C> to stop'
    
    #Create monitor
    monitor_th = threading.Thread(target= monitor, args = (,)); 
    t.daemon = True;
    t.start();
    
    server.serve_forever()
