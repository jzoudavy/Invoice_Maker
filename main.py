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
import quickstart_sheets
import quickstart_mail
import get_credentials

 
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Run this script on Sunday
# 
#    
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
sheet_SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
sheet_CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\Invoice_Maker\.client_secret_sheets.json'
sheet_APPLICATION_NAME= 'Sheets'

calendar_SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
calendar_CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\Invoice_Maker\.client_secret_calendar.json'
calendar_APPLICATION_NAME= 'Calendar' 

drive_SCOPES = 'https://www.googleapis.com/auth/drive'
drive_CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\Invoice_Maker\.client_secret_drive.json'
drive_APPLICATION_NAME = 'Drive' 

mail_SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
mail_CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\Invoice_Maker\.client_secret_mail.json'
mail_APPLICATION_NAME = 'Mail' 


def get_all_credentials():

    calendar_credentials = get_credentials.get_credentials(calendar_SCOPES,calendar_CLIENT_SECRET_FILE,calendar_APPLICATION_NAME)
    calendar_http = calendar_credentials.authorize(httplib2.Http())
    calendar_service = discovery.build('calendar', 'v3', http=calendar_http)

    sheet_credentials = get_credentials.get_credentials(sheet_SCOPES,sheet_CLIENT_SECRET_FILE,sheet_APPLICATION_NAME)
    sheet_http = sheet_credentials.authorize(httplib2.Http())
    sheet_discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    sheet_service = discovery.build('sheets', 'v4', http=sheet_http,
                              discoveryServiceUrl=sheet_discoveryUrl)
    
    drive_credentials = get_credentials.get_credentials(drive_SCOPES,drive_CLIENT_SECRET_FILE,drive_APPLICATION_NAME) 
    drive_http = drive_credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=drive_http) 


    mail_credentials = get_credentials.get_credentials(mail_SCOPES,mail_CLIENT_SECRET_FILE,mail_APPLICATION_NAME)
    mail_http = mail_credentials.authorize(httplib2.Http())
    mail_service = discovery.build('gmail', 'v1', http=mail_http)


    return calendar_service,sheet_service,drive_service,mail_service

def main():
    
    calendar_service,sheet_service,drive_service,mail_service=get_all_credentials()

     
    last_spreadsheetId=quickstart_drive.get_last_spreadsheetId(drive_service)
    
    #write to new spreadsheet, give it sheet, time info, new spreasheetID and the last invoice's ID
    last_spreadsheet_end_dates=quickstart_sheets.get_last_spreadsheet_end_dates(sheet_service,last_spreadsheetId)                              
 
    week_range1,week_range2,occurance_week1,occurance_week2=quickstart_calendar.main(calendar_service,last_spreadsheet_end_dates)
    print ('Our first week of work is {}. We worked {} days. Second week is {}. We worked {} days.'.format(week_range1,occurance_week1,week_range2,occurance_week2))
    new_invoice_filename = 'Invoice '+week_range1.split(' ')[0]+' to '+week_range2.split(' ')[-1]
    spreadsheetId=quickstart_drive.copy(drive_service,new_invoice_filename)
    
    quickstart_sheets.write_to_sheets(sheet_service,week_range1,week_range2,occurance_week1,occurance_week2,spreadsheetId,last_spreadsheetId)
    quickstart_drive.download_sheets(drive_service,spreadsheetId,new_invoice_filename)
    #email new sheet
    quickstart_mail.main(mail_service,drive_service,spreadsheetId,new_invoice_filename)

 
if __name__ == '__main__':
    main()
    
