#sheets calls calendar to get the right dates
#sheets calls drive to get the right file and create the right file.

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import quickstart_calendar
import quickstart_drive

  
 
def get_last_spreadsheet_end_dates(service, spreadsheetId):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Invoice!B20').execute()
    print('Our invoice end date is: ',result['values'])
    return result

  
def write_to_sheets(service,week_range1,week_range2,return_occurance_week1,return_occurance_week2,spreadsheetId,last_spreadsheetId):
    print('We are in quickstart_sheets')
     
    ##write to the number of days we worked  
    values = [[return_occurance_week1],[return_occurance_week2]]
    value_input_option='RAW'
    body = {'values': values}
    rangeName = 'Invoice!E19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

    #write to sheets the week range, bla-day to bla-bla-day
    week_range_value=[[week_range1],[week_range2]]
    body = {'values': week_range_value}
    rangeName = 'Invoice!B19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

    #set invoice ID to be from the Invoice field of last spreadsheet created, then increment, write to cell F12 
    result = service.spreadsheets().values().get(spreadsheetId=last_spreadsheetId, range='Invoice!F12').execute()
    invoice_ID = int(result['values'][0][0])
    invoice_ID +=1
    result['values'][0][0] = invoice_ID
    body = result
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range='Invoice!F12',valueInputOption=value_input_option, body=body).execute()
    
    #set submission date
    #B9
    today=quickstart_calendar.give_me_today()
    print(today.strftime("%Y %m %d"))
    submission_date = [['Created on '+today.strftime("%Y %m %d")]]
    body = {'values': submission_date}
    rangeName = 'Invoice!B9'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

    #set due date
    #F15
    print(week_range2.split()[-1])
    due_date = [[week_range2.split()[-1]]]
    body = {'values': due_date}
    rangeName = 'Invoice!F15'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()
