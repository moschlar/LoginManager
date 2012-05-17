#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

"""connman contains simple functions that perform login and logout related tasks.

It is only useful in the network of the Johannes Gutenberg University Mainz where this special type of login measures is performed."""

import sys
import re
from urlparse import urlsplit, urlunsplit
from httplib import HTTPSConnection
from urllib import urlencode

scheme = "https"
host = 'login.wohnheim.uni-mainz.de'
path = {'loginref': '/login.html', 'login': '/cgi-bin/login-cgi', 'logoutref': '/logout.html', 'logout': '/cgi-bin/logout.cgi'}

def login(username, password):
	"""Call the login site for the current host with supplied username and password.
	
	Returns tuple of consumed download/upload traffic in percent."""
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
	site = site.split('table')[1]
	#pattern = re.compile(r'You have consumed (\d*)/(\d*) % of your monthly')
	pattern_traffic = re.compile(r'consumed (.*?)/(.*?) % of your', re.MULTILINE)
	#str_consumed = u'consumed your montly traffic allowance'
	match = pattern_traffic.search(site)
	if match:
		return match.groups()
	else:
		return (100,100)

def logout():
	"""Call the logout site for the current host"""
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
	"""Check if the current host is logged in"""
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
