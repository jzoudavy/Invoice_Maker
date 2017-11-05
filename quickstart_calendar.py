from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import pytz
import calendar
from isoweek import Week

 
def give_me_today():
    return datetime.datetime.now()

 

def str_to_date_int(enddate):

    str_date = enddate['values'][0][0].split()[-1]
    # gets values, which is a double list, that stores our date as a string, so split and get the last element

    year,month,day=str_date.split('-')
    print(year,month,day)
    year = int(year)
    month = int(month)
    day = int(day)

    return year,month,day
 
### next_week_dates returns the next dates requested by adding given enddate with delta
def next_week_dates(enddate, delta):
    

    year,month,day=str_to_date_int(enddate)
    dt = datetime.datetime(year,month,day)
    dt= dt + datetime.timedelta(delta) # increase days by delta amount, either next monday or next sunday etc
    print ('dt is ',dt)
    return dt
  
def main(service,enddate):
    occurance_week1 =0
    occurance_week2 =0
    timezone= pytz.timezone('US/Eastern')
    #enddate is a string
    #get nextweek's monday
    w1_Monday = next_week_dates(enddate, 1)
    w1_Monday = timezone.localize(w1_Monday).isoformat('T')
    w1_Sunday = next_week_dates(enddate, 7)
    w1_Sunday = timezone.localize(w1_Sunday).isoformat('T')

    w2_Monday = next_week_dates(enddate, 8)
    w2_Monday = timezone.localize(w2_Monday).isoformat('T')
    w2_Sunday = next_week_dates(enddate, 14)
    w2_Sunday = timezone.localize(w2_Sunday).isoformat('T')

    week_range1 = w1_Monday.split('T')[0] + ' to ' + w1_Sunday.split('T')[0]
    week_range2 = w2_Monday.split('T')[0] + ' to ' + w2_Sunday.split('T')[0]  

    print('Getting the upcoming events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=w1_Monday, timeMax=w1_Sunday, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
      
    for event in events:
        if event['summary'] == 'MS work':
            print("*"*50)
            occurance_week1+=1
    
   
    eventsResult = service.events().list(
        calendarId='primary', timeMin=w2_Monday, timeMax=w2_Sunday, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
      
    for event in events:
        if event['summary'] == 'MS work':
            print("*"*50)
            occurance_week2+=1


    return week_range1,week_range2,occurance_week1,occurance_week2
 

if __name__ == '__main__':
    main()
    
