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
def next_two_weeks(enddate): 
    str_enddate = enddate['values'][0][0].split()[-1] # gets values, which is a double list, that stores our date as a string, so split and get the last element
    print(str_enddate)
    
    year,month,day=str_enddate.split('-')
    print(year,month,day)

     

    return True
  
def main(service):
   
    print('We are in the main of quickstart_caldendar.') 

    print('Getting the upcoming 15 events')
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

            work_day_iso_week= datetime.date(work_year, work_month, work_day).isocalendar()[1]
            print ('The ISO week of work is ',work_day_iso_week)
            print ('Current ISO week is ',current_iso_week)
            

            if work_day_iso_week == current_iso_week:
                
                iso_week1=work_day_iso_week
                print("First week is ",iso_week1)
                occurance_week1+=1
                w=Week(work_year, iso_week1)
                
                week_range1_Mon = w.monday().isoformat()
                week_range1_Sun = w.sunday().isoformat()
                print ("First week's range is ", week_range1_Mon, " to ",week_range1_Sun)

            if work_day_iso_week == current_iso_week+1:
            
                iso_week2=work_day_iso_week
                print("Second week is ",iso_week2)
                occurance_week2+=1
                w=Week(work_year, iso_week2)
                
                week_range2_Mon = w.monday().isoformat()
                week_range2_Sun = w.sunday().isoformat()
                print ("Second week's range is ", week_range2_Mon, " to ",week_range2_Sun)

    week_range1=week_range1_Mon+" to "+week_range1_Sun
    week_range2=week_range2_Mon+" to "+week_range2_Sun
    return week_range1,week_range2,occurance_week1,occurance_week2
 

if __name__ == '__main__':
    main()
    
