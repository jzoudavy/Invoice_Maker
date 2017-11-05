#send our spreadsheet
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from apiclient import errors
from googleapiclient import http
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload
import io

import mimetypes 
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  fp = open(file, 'rb')
  msg = MIMEBase(main_type, sub_type)
  msg.set_payload(fp.read())
  fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}
  #return {'raw': base64.urlsafe_b64encode(message.as_bytes())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def main(mail_service,spreadsheetId,new_invoice_filename):
    print('We are emailing the spreadsheet.')
    sender = 'jzoudavy@gmail.com'
    to = 'jzoudavy@gmail.com'
    subject = 'test '+new_invoice_filename
    message_text = 'Hi Susan \n Please find attched the next invoice. \n thanks \n davy'
    attachment = 'D:/My Documents/GitHub/Invoice_Maker/'+new_invoice_filename+'.pdf'
    print(message_text,attachment)
    msg = create_message_with_attachment(sender, to, subject, message_text, attachment)

    send_message(mail_service, sender, msg)

     
   


