from __future__ import print_function
from isoweek import Week
from apiclient import errors 
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os
import datetime
import pytz
import calendar

import quickstart_calendar
import quickstart_drive
import quickstart_sheet

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None