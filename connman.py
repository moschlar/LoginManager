#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re
from urlparse import urlsplit, urlunsplit
from httplib import HTTPSConnection
from urllib import urlencode

scheme = "https"
host = 'login.wohnheim.uni-mainz.de'
path = {'loginref': '/login.html', 'login': '/cgi-bin/login-cgi', 'logoutref': '/logout.html', 'logout': '/cgi-bin/logout.cgi'}

def login(username, password):
	params  = urlencode({'user': username, 'pass': password, 'submit': '   Login   ', 'forward': '', 's': ''})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Referer": urlunsplit((scheme, host, path['loginref'], "", ""))}
	conn = HTTPSConnection(host)
	conn.request("POST", path['login'], params, headers)
	response = conn.getresponse()
	if 300 <= response.status < 400:
		conn.close()
		b = urlsplit(response.getheader('location'))
		#print b.path
		conn.request("GET", b.path)
		response = conn.getresponse()
	#print dir(response)
	#print response.status, response.reason
	#print response.msg
	#print response.getheaders()
	site = response.read()
	#print site
	#pattern = re.compile(r'You have consumed (\d*)/(\d*) % of your monthly')
	pattern = re.compile(r'consumed (.*?)/(.*?) % of your', re.MULTILINE)
	match = pattern.search(site)
	return match.groups()

def logout():
	params  = urlencode({'submit': '   Logout   ', 'command': 'logout'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Referer": urlunsplit((scheme, host, path['logoutref'], "", ""))}
	conn = HTTPSConnection(host)
	conn.request("POST", path['logout'], params, headers)
	response = conn.getresponse()
	if 300 <= response.status < 400:
		conn.close()
		b = urlsplit(response.getheader('location'))
		#print b.path
		conn.request("GET", b.path)
		response = conn.getresponse()
	#print dir(response)
	#print response.status, response.reason
	#print response.msg
	#print response.getheaders()
	#print response.read()
	return

def isLoggedIn():
	conn = HTTPSConnection(host)
	conn.request("GET", "/")
	response = conn.getresponse()
	if 300 <= response.status < 400:
		if 'logout' in urlsplit(response.getheader('location')).path:
			return True
		return False

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		user = sys.argv[1]
	else:
		user = raw_input("ZDV-Benutzername: ")
	if len(sys.argv) == 3:
		password = sys.argv[2]
		print """
WARNUNG: 
Passwörter sollten niemals auf der Kommandozeile eingegeben werden.
Sie sind für jeden lesbar, der Zugriff auf die History-Datei der Shell hat.
		"""
	else:	
		import getpass
		password = getpass.getpass("ZDV-Passwort: ")
	print "Logged in: %s" % isLoggedIn()
	logout()
	print "Logged in: %s" % isLoggedIn()
	print login(user, password)
	print "Logged in: %s" % isLoggedIn()
