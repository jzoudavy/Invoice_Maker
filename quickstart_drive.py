from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'D:\My Documents\GitHub\GsheetAPI\.client_secret_drive_write.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
 

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

#get last created spreadsheet's ID
def get_last_spreadsheetId():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

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

        return items[0]['id']
                



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(new_invoice_filename):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

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
                

if __name__ == '__main__':
    main()