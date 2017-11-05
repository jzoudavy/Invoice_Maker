from __future__ import print_function
from isoweek import Week
from apiclient import errors 
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
    
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
    
    if APPLICATION_NAME is 'Calendar':
        credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')
    elif APPLICATION_NAME is 'Sheets':
        credential_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')
    elif APPLICATION_NAME is 'Drive':
        credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')
    elif APPLICATION_NAME is 'Mail':
        credential_path = os.path.join(credential_dir,'gmail-python-quickstart.json')

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

if __name__ == '__name__':
    get_credentials()