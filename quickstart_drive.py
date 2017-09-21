from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

 
 
def copy_file(service, origin_file_id, copy_title):
    """Copy an existing file. Args:
    service: Drive API service instance.
    origin_file_id: ID of the origin file to copy.
    copy_title: Title of the copy.
    
    Returns:
    The copied file if successful, None otherwise.
    """
  
    copied_file = {'name': copy_title}
    print("new file name is ",copied_file)
    try:  
        return service.files().copy(fileId=origin_file_id, body=copied_file).execute()
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)
    return None

#get last created spreadsheet's invoiceID
def get_last_spreadsheetId(service):
    

    results = service.files().list(
        pageSize=20,fields="nextPageToken, files(modifiedTime, name, id)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            #print('This item is', item)
            if 'Invoice' in item['name']:
                print('We found the invoices: ')
                print('{0} {1} {2}'.format(item['name'], item['modifiedTime'],item['id']))
        #we found the invoice, formatted according to time, most recent at the top, get it's ID
        return items[0]['id']
                

 

def copy(service,new_invoice_filename):
    '''
    makes a copy of the new invoice
    '''
    print('We are at quickstart_drive')

    results = service.files().list(
        pageSize=20,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            if item['id'] == '1IaO33cnRu_vVVCjN4yPrGnlUP1t7L46Y7MISAAAIC3c':
                print ('We found sample file now copying it')
                newfile=copy_file(service, item['id'], new_invoice_filename)
    print('new file id is ',newfile['id'])
    return newfile['id'] 
                
 