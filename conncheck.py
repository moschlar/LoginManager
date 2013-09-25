#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

from connman import isLoggedIn

if __name__ == '__main__':
	status = isLoggedIn()
	print status
	sys.exit(0 if status else 1)
