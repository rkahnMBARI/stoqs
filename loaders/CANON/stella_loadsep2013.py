#!/usr/bin/env python
__author__    = 'Mike McCann,Duane Edgington,Reiko Michisaki'
__copyright__ = '2013'
__license__   = 'GPL v3'
__contact__   = 'duane at mbari.org'

__doc__ = '''

Stella loader for all CANON activities in September 2013

Mike McCann; Modified by Duane Edgington and Reiko Michisaki
MBARI 02 September 2013

@var __date__: Date of last svn commit
@undocumented: __doc__ parser
@status: production
@license: GPL
'''

import os
import sys
import datetime  # needed for glider data
import time      # for startdate, enddate args
import csv
os.environ['DJANGO_SETTINGS_MODULE']='settings'
project_dir = os.path.dirname(__file__)

# the next line makes it possible to find CANON
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../"))  # this makes it possible to find CANON, one directory up

from CANON import CANONLoader
       
# building input data sources object
from socket import gethostname
hostname=gethostname()
print hostname
if hostname=='odss-test.shore.mbari.org':
    cl = CANONLoader('stoqs_september2011', 'CANON - September 2011')
else:
    cl = CANONLoader('stoqs_september2013', 'CANON - September 2013')

# default location of thredds and dods data:
cl.tdsBase = 'http://odss.mbari.org/thredds/'
cl.dodsBase = cl.tdsBase + 'dodsC/'


######################################################################
#  GLIDERS
######################################################################
# Set start and end dates for all glider loads
# startdate is 24hours from now
ts=time.time()-(2.2*60*60)  
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
t=time.strptime(st,"%Y-%m-%d %H:%M")
#t =time.strptime("2013-09-05 0:01", "%Y-%m-%d %H:%M")
startdate=t[:6]
t =time.strptime("2013-10-15 0:01", "%Y-%m-%d %H:%M")
enddate=t[:6]

 
#######################################################################################
# DRIFTERS
#######################################################################################

# Stella drifters, requires input file stella_load.csv with the names of the 
# stella drifters to load, i.e. stella202 or stella205 etc.
stella_list=[]
csvfile='./stella_load.csv'    
if os.path.exists(csvfile):
    myReader = csv.DictReader(open(csvfile, 'r'))
    stella_list=[]
    for row in myReader:
        stella_list.append(row['drifter']+'_data.nc')

    cl.stella_base = cl.dodsBase + 'CANON_september2013/Platforms/Drifters/Stella_1/'
    cl.stella_parms = [ 'TEMP', 'pH' ]
    cl.stella_files=stella_list

###################################################################################################################
# Execute the load
    cl.process_command_line()

    if cl.args.test:
#        cl.loadStella203(stride=1)
    #    cl.loadStella204(stride=1)
        cl.loadStella(stride=1)

    elif cl.args.optimal_stride:
    #    cl.loadStella203(stride=1)
    #    cl.loadStella204(stride=1)
        cl.loadStella(stride=1)

    else:
    #    cl.loadStella203(stride=1)
    #    cl.loadStella204(stride=1)
        cl.loadStella(stride=1)

else:
    print "ERROR: File list of drifter names to load, stella_load.csv, not found."
