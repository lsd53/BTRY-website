#!/usr/bin/python
#-------------------------------------
print "Content-type: text/html"
print
#-------------------------------------
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage
import cgitb
cgitb.enable()

print 'CGI is working!'
