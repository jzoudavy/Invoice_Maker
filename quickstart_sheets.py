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
 
  
 

 

def main(service,week_range1,week_range2,return_occurance_week1,return_occurance_week2,spreadsheetId):
    print('We are in quickstart_sheets')
     
    ##write to sheet  
 
  
    values = [[return_occurance_week1],[return_occurance_week2]]
    value_input_option='RAW'
    body = {'values': values}
    rangeName = 'Invoice!E19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()
    print(result)

    week_range_value=[[week_range1],[week_range2]]
    body = {'values': week_range_value}
    rangeName = 'Invoice!B19'
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,valueInputOption=value_input_option, body=body).execute()

    #set invoice ID to be from the Invoice field of last spreadsheet created, write to cell F12
    
    result = service.spreadsheets().values().get(spreadsheetId=last_spreadsheetId, range='Invoice!F12').execute()
    #print('Our invoice result is: ',result)
    print('Our invoice result key is values: ',result['values'])
    invoice_ID = int(result['values'][0][0])
    invoice_ID +=1
    result['values'][0][0] = invoice_ID

    print('New ID is ',invoice_ID)
    #update invoice id.
    body = result
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range='Invoice!F12',valueInputOption=value_input_option, body=body).execute()
    
    



if __name__ == '__main__':
    main()