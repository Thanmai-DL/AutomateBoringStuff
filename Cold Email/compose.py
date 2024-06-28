import os
import sys
import base64
import mimetypes
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from docx import Document

def recipient(first, middle, last, domain):
    f, m, l = [], [], []
    f.append(first);f.append(first[0])
    l.append(last);l.append(last[0])
    sep = '.'
    d = '@' + domain
    comb = []
    for i in f:
        for k in l:
            if not (len(i) == 1 and len(k) == 1):
                comb.append(i + k + d)
                comb.append(i + sep + k + d)
                comb.append(k + i + d)
                comb.append(k + sep + i + d)
    if middle != 'N/A':
        m.append(middle);m.append(middle[0])
        for i in f:
            for j in m:
                for k in l:
                    if not (len(i) == 1 and len(k) == 1):
                        comb.append(i + j + k + d)
                        comb.append(i + sep + j + sep + k + d)
                        comb.append(i + sep + j + k + d)
                        comb.append(i + j + sep + k + d)
                        comb.append(j + i + k + d)
                        comb.append(j + sep + i + sep + k + d)
                        comb.append(j + sep + i + k + d)
                        comb.append(j + i + sep + k + d)
                        comb.append(k + i + j + d)
                        comb.append(k + sep + i + sep + j + d)
                        comb.append(k + sep + i + j + d)
                        comb.append(k + i + sep + j + d)
    comb.sort()
    return ",".join(comb)

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email with an attachment."""
    # Create a multipart message
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Add the html text message part
    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    # Add the attachment part
    content_type, encoding = mimetypes.guess_type(file)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)

    with open(file, 'rb') as f:
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(f.read())

    encoders.encode_base64(msg)
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    # Encode the message to base64
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_email(sender, to, subject, message_text, file, credentials):
    """Send an email with an attachment."""
    try:
        # Create the email message
        message = create_message_with_attachment(sender, to, subject, message_text, file)

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=credentials)

        # Send the email
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f'Message Id: {sent_message["id"]}')
        return sent_message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def read_message_from_html(file_path):
    """Read HTML content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Step 1: Authenticate and get credentials
credentials = authenticate()

# Step 2: Read the message from the Word document
html_file = './message.html'
message_text = read_message_from_html(html_file)

# Step 3: Define the email details and send the email
sender = 'thanmaidl@gmail.com'
subject = sys.argv[-1]
attachment = './ThanmaiDL_Résumé.pdf'

if len(sys.argv) == 6:
    to = recipient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
else:
    to = recipient(sys.argv[1], 'N/A', sys.argv[2], sys.argv[3])

send_email(sender, to, subject, message_text, attachment, credentials)