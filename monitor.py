#!/usr/bin/env python

from pygtail import Pygtail
from os import path
from time import time
import socket

#for line in Pygtail("some.log"):
#    sys.stdout.write(line)

cycle_rate = 30

# these are all the log files we want to monitor
log_files = ["/var/log/syslog",
			"/var/log/auth.log",
			"/var/log/dmesg",
			"/var/log/kern.log",
			"/var/log/mail.log",
			"/var/log/mail.err",
			"/var/log/ufw.log",
			"/home/kippo/kippo-0.8/log/kippo.log"]

#log_files = ["/var/log/messages",
#                        "/var/log/dmesg",
#                        "/var/log/kern.log",
#                        "/var/log/exim_mainlog",
#                        "/var/log/exim_rejectlog",
#                        "/var/log/secure"]


dst_host = 'dstoll.no-ip.biz'
dst_port = 9999
buffer_size = 1024000

DEBUG=False

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((dst_host, dst_port))
except Exception as e:
	print e
	exit(-1)


while(True):
	start_time = time()
	if DEBUG:
		print 'starting log sweep'

	for file in log_files:
		if DEBUG:
			print 'checking ', file
		if path.exists(file):
			for line in Pygtail(file):
				msg = file.split('/')[-1] + ' - ' + line.rstrip() + '\n'
				try:
					s.send(msg)
				except:
					if DEBUG:
						print 'error, retrying connection.'
					try:
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((dst_host, dst_port))
						s.send(msg)
					except Exception as e:
						print e
						exit(-1)

	while time() - start_time < cycle_rate:
		pass

s.close()
