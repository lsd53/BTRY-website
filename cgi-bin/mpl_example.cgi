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

import tempfile
import os
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import random

x = [random.random() for i in range(10)]
y = [random.random() for i in range(10)]

plt.scatter(x,y)
plt.savefig('../images/plot.png')

print '''
<html>
<body>
<h1>CGI is working. Image should display below:</h1>
<img src="../images/plot.png">
<h1>Image should display above</h1>
</body>
</html>
'''
