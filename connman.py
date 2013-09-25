#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""connman contains simple functions that perform login and logout related tasks.

It is only useful in the network of the Johannes Gutenberg University Mainz where this
special type of login measures is performed."""

import sys
import re

if sys.version_info[0] == 2:
	from urlparse import urlsplit, urlunsplit
	from httplib import HTTPSConnection
	from urllib import urlencode
	input = raw_input
elif sys.version_info[0] == 3:
	from urllib.parse import urlsplit, urlunsplit, urlencode
	from http.client import HTTPSConnection
else:
	raise Exception('Can not determine sys.version')

scheme = "https"
host = 'login.wohnheim.uni-mainz.de'
path = {'loginref': '/login.html', 'login': '/cgi-bin/login-cgi',
		'logoutref': '/logout.html', 'logout': '/cgi-bin/logout.cgi'}

def login(username, password):
	"""Call the login site for the current host with supplied username and password.
	
	Returns tuple of consumed download/upload traffic in percent."""
	params  = urlencode({'user': username, 'pass': password, 'submit': '   Login   ',
						'forward': '', 's': ''})
	headers = {"Content-type": "application/x-www-form-urlencoded",
				"Referer": urlunsplit((scheme, host, path['loginref'], "", ""))}
	conn = HTTPSConnection(host)
	conn.request("POST", path['login'], params, headers)
	response = conn.getresponse()
	if 300 <= response.status < 400:
		# Handle possible redirection
		conn.close()
		b = urlsplit(response.getheader('location'))
		conn.request("GET", b.path)
		response = conn.getresponse()
	site = response.read()
	site = str(site)
	return 'LogIn successful.' in site

def logout():
	"""Call the logout site for the current host"""
	params  = urlencode({'submit': '   Logout   ', 'command': 'logout'})
	headers = {"Content-type": "application/x-www-form-urlencoded",
				"Referer": urlunsplit((scheme, host, path['logoutref'], "", ""))}
	conn = HTTPSConnection(host)
	conn.request("POST", path['logout'], params, headers)
	response = conn.getresponse()
	if 300 <= response.status < 400:
		# Handle possible redirection
		conn.close()
		b = urlsplit(response.getheader('location'))
		conn.request("GET", b.path)
		response = conn.getresponse()
	site = response.read()
	site = str(site)
	return 'Your IP has been successfully disabled.' in site

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
	if len(sys.argv) < 2 or sys.argv[1] not in ('status', 'login', 'logout'):
		print("Usage: %s <status|login|logout>")
		sys.exit(1)

	if sys.argv[1] == 'status':
		status = isLoggedIn()
	elif sys.argv[1] == 'logout':
		status = logout()
	elif sys.argv[1] == 'login':
		if len(sys.argv) >= 3:
			user = sys.argv[2]
		else:
			user = input("ZDV-Benutzername: ")
		if len(sys.argv) == 4:
			password = sys.argv[3]
			print("""
WARNUNG:
Passwörter sollten niemals auf der Kommandozeile eingegeben werden.
Sie sind für jeden lesbar, der Zugriff auf die History-Datei der Shell hat.
""")
		else:	
			import getpass
			password = getpass.getpass("ZDV-Passwort: ")
		status = login(user, password)

	print(status)

	status = 0 if status else 1

	sys.exit(status)
