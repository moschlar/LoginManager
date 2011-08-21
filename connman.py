import httplib, urllib, urlparse

uri = {'loginref': 'https://login.wohnheim.uni-mainz.de/login.html', 'login': 'https://login.wohnheim.uni-mainz.de/cgi-bin/login-cgi', 'logoutref': 'https://login.wohnheim.uni-mainz.de/logout.html', 'logout': 'https://login.wohnheim.uni-mainz.de/cgi-bin/logout.cgi'}

def login(username, password):
	params  = urllib.urlencode({'user': username, 'pass': password, 'submit': '   Login   ', 'forward': '', 's': ''})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Referer": uri['loginref']}
	a = urlparse.urlparse(uri['login'])
	conn = httplib.HTTPConnection(a.hostname)
	conn.request("POST", a.path, params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	print response.read()
	return

def logout():
	params  = urllib.urlencode({'submit': '   Logout   ', 'command': 'logout'})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Referer": uri['logoutref']}
	a = urlparse.urlparse(uri['logout'])
	conn = httplib.HTTPConnection(a.hostname)
	conn.request("POST", a.path, params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	print response.read()
	return

logout()
login('user','dummy')
