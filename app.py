from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import imaplib
import email

import imaplib

app = Flask(__name__)

# Configure the email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # or 465 for SSL
app.config['MAIL_USERNAME'] = 'techchallengetum@gmail.com'
app.config['MAIL_PASSWORD'] = 'Cuthi5-hankan-jaqgaq'
app.config['MAIL_USE_TLS'] = True  # Set to False if using SSL
app.config['MAIL_USE_SSL'] = False  # Set to True if using SSL

mail = Mail(app)

import imaplib
import email
from flask import Flask, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)

@app.route('/viewEmails')
def view_emails():
    # Load your OAuth2 credentials
    creds = None
    # Load the saved token.json file that contains your access and refresh tokens.
    # If using a different email provider, adjust accordingly.

    # If there are no valid credentials available, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=['https://mail.google.com/'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run

    # Use the credentials to access the email server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.auth(creds)

    mail.select('inbox')  # Connect to the inbox
    status, response = mail.search(None, 'UNSEEN')
    email_ids = response[0].split()

    emails = []
    for e_id in email_ids:
        _, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                emails.append({'from': email_from, 'subject': email_subject})

    mail.logout()

    return render_template('emails.html', emails=emails)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

####
'''

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get('subject', 'No Subject')
    recipient = data.get('recipient')
    body = data.get('body', '')

    if not recipient:
        return jsonify({"error": "Recipient is required"}), 400

    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = body
    mail.send(msg)

    return jsonify({"message": "Email sent successfully to {}".format(recipient)})

@app.route('/viewEmails')
def view_emails():
    mail_server = 'smtp.gmail.com'  # Replace with your IMAP server
    email_account = 'techchallengetum@gmail.com'  # Your full email address
    password = 'Cuthi5-hankan-jaqgaq'  # Your email password

    # Connect to the mail server
    mail = imaplib.IMAP4_SSL(mail_server)
    mail.login(email_account, password)
    mail.select('inbox')  # Connect to the inbox

    # Search for unseen emails
    status, response = mail.search(None, 'UNSEEN')
    email_ids = response[0].split()

    emails = []
    for e_id in email_ids:
        # Fetch the email's full data
        _, msg_data = mail.fetch(e_id, '(RFC822)')

        # Parse the email data
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                emails.append({'from': email_from, 'subject': email_subject})

    mail.logout()

    # Render a template to display emails
    return render_template('emails.html', emails=emails)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
'''