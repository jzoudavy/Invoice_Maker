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





###get time

d = datetime.datetime.now()
u = datetime.timedelta(days=14) 
t = u+d

timezone= pytz.timezone('US/Eastern')
t_end= timezone.localize(t)
t_end=t_end.isoformat('T')

now = datetime.datetime.now()
t_now=timezone.localize(now)
t_now=t_now.isoformat('T')

#print("start is :"+str(t_now))
#print("end is :"+str(t_end))

current_iso_week= datetime.datetime.now().isocalendar()[1]

def str_to_date_int(str_date):

    year,month,day=str_date.split('-')
    print(year,month,day)
    year = int(year)
    month = int(month)
    day = int(day)+1

    return year, month,day


### 
def next_two_weeks(enddate): 
    str_enddate = enddate['values'][0][0].split()[-1] # gets values, which is a double list, that stores our date as a string, so split and get the last element
    year, month, day = str_to_date_int(str_enddate)
    
    

    iso_week1= datetime.date(year, month, day).isocalendar()[1]
    w=Week(year, iso_week1)
                
    week_range1_Mon = w.monday().isoformat()
    week_range1_Sun = w.sunday().isoformat()
    print ("First week's range is ", week_range1_Mon, " to ",week_range1_Sun)

    if iso_week1 == 52:
        iso_week2 = 0
        year = year + 1
    else:
        iso_week2=iso_week1+1
    
    w=Week(year, iso_week2)
    
    week_range2_Mon = w.monday().isoformat()
    week_range2_Sun = w.sunday().isoformat()
    print ("Second week's range is ", week_range2_Mon, " to ",week_range2_Sun)            

    week_range1=week_range1_Mon+" to "+week_range1_Sun
    week_range2=week_range2_Mon+" to "+week_range2_Sun
    print(week_range1, week_range2)
    return week_range1,week_range2
     
  
def main(service,enddate):
    # need to rewrite this section
    timezone= pytz.timezone('US/Eastern')

    year, month, day = str_to_date_int(enddate)
    dt = datetime.datetime(year,month,day)
    t_w1_start = timezone.localize(dt).isoformat('T')
  
    delta = datetime.timedelta(days=7) 
    dt = dt + delta
    t_w1_end = timezone.localize(dt).isoformat('T')


    #now we are in second week
    delta = datetime.timedelta(days=1) 
    dt = dt + delta
    t_w2_start = timezone.localize(dt).isoformat('T')
    delta = datetime.timedelta(days=7)
    dt = dt + delta
    t_w2_end = timezone.localize(dt).isoformat('T')

     
    occurance_week1 = 0
    occurance_week2 = 0

    #we now have the start and stop two week time range to search for occurances
    print('We are in the main of quickstart_caldendar.') 

    print('Getting the upcoming events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=t_w1_start, timeMax=t_w1_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
      
    for event in events:
        #print('this is '+str(i)+'th event.')
        if event['summary'] == 'MS work':
            start = event['start'].get('dateTime', event['start'].get('date'))
            print("*"*50)
            occurance_week1+=1
    
     print('Getting the upcoming events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=t_w2_start, timeMax=t_w2_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
      
    for event in events:
        #print('this is '+str(i)+'th event.')
        if event['summary'] == 'MS work':
            start = event['start'].get('dateTime', event['start'].get('date'))
            print("*"*50)
            occurance_week1+=1
    return occurance_week1,occurance_week2
 

if __name__ == '__main__':
    main()
    
