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
### 

  
def main(service):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    print('We are in the main of quickstart_caldendar.') 

    
    print('Getting the upcoming 15 events')
    #this function returns 15 events by default. 
    eventsResult = service.events().list(
        calendarId='primary', timeMin=t_now, timeMax=t_end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    
    if not events:
        print('No upcoming events found.')
    
    iso_week1 =0
    iso_week2 =0
    occurance_week1 = 0
    occurance_week2 = 0
    for event in events:
        #print('this is '+str(i)+'th event.')
        if event['summary'] == 'MS work':
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start,"--",event['summary'])
            print("*"*50)
 
            work_year,work_month,work_day = start.split('-')

            work_year=int(float(work_year))
            work_month=int(float(work_month))
            work_day=int(float(work_day))

            #print (int(float(work_year)))
            #print (int(float(work_month)))
            #print (int(float(work_day)))

            iso_week= datetime.date(work_year, work_month, work_day).isocalendar()[1]
            #print (iso_week)
            if iso_week == current_iso_week:
                
                iso_week1=iso_week
                print("First week is ",iso_week1)
                occurance_week1+=1
                w=Week(work_year, iso_week1)
                
                week_range1_Mon = w.monday().isoformat()
                week_range1_Sun = w.sunday().isoformat()
                print ("First week's range is ", week_range1_Mon, " to ",week_range1_Sun)
            if iso_week == current_iso_week+1:
            
                iso_week2=iso_week
                print("Second week is ",iso_week2)
                occurance_week2+=1
                w=Week(work_year, iso_week2)
                
                week_range2_Mon = w.monday().isoformat()
                week_range2_Sun = w.sunday().isoformat()
                print ("Second week's range is ", week_range2_Mon, " to ",week_range2_Sun)

            #we ignore anything but the next two weeks.
       
    #print ("The first week is week # ",iso_week1,", it is from ",week_range1,". We worked ",occurance_week1," days.")
    #print ("The second week is week # ",iso_week2,", it is from ",week_range2,". We worked ",occurance_week2," days.")
    week_range1=week_range1_Mon+" to "+week_range1_Sun
    week_range2=week_range2_Mon+" to "+week_range2_Sun
    return week_range1,week_range2,occurance_week1,occurance_week2
 

if __name__ == '__main__':
    main()
    
