#!/usr/bin/python

import OpenSSL
import socket
import struct
import ssl
import pprint
import sys

address =sys.argv[1]
port = int(sys.argv[2])


# Prefer TLS
context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s, ca_certs="/etc/ssl/certs/ca-certificates.crt", cert_reqs=ssl.CERT_REQUIRED)
match_hostname(sslsock.getpeercert(), hostname)
ssl_sock.connect((address, port))
s.settimeout(5)

#print repr(ssl_sock.getpeername())
#print ssl_sock.cipher()
#print pprint.pformat(ssl_sock.getpeercert())

# Set a simple HTTP request
ssl_sock.write("GET / HTTP/1.1 \r\n\r\n")

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
print ssl_sock.read()

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()
