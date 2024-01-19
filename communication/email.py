import email
import imaplib
from typing import List
import re

from flask_mail import Message


class Mailer:
    def __init__(self, mail, mail_server: str, email_account: str, password: str):
        self.mail = mail
        self.mail_server = mail_server
        self.email_account = email_account
        self.password = password
        self.test_client_name = "Jonas Zausinger"
        self.test_client_email = "jonas.zausinger1@gmail.com"
        self.lawyer_name = "Max Mustermann"

    def set_test_client(self, name: str, email_address: str):
        self.test_client_name = name
        self.test_client_email = email_address

    def set_lawyer_name(self, name: str):
        self.lawyer_name = name

    def send_mail(self, subject: str, body: str) -> None:
        msg = Message(subject, sender=self.email_account, recipients=[self.test_client_email])
        msg.body = body
        self.mail.send(msg)

    def get_unread_emails(self, search_criteria: str = "UNSEEN") -> List[dict]:
        # Connect to the mail server
        mail = imaplib.IMAP4_SSL(self.mail_server)
        mail.login(self.email_account, self.password)
        mail.select('inbox')  # Connect to the inbox

        search = f"({search_criteria} FROM \"{self.test_client_email}\")"
        # Search for unseen emails
        status, response = mail.search(None, search)
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

                    # Get the email body
                    if msg.is_multipart():
                        for part in msg.walk():
                            # Find the content type of the email part
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" not in content_disposition:
                                try:
                                    # Get the email body
                                    body = part.get_payload(decode=True).decode()
                                except Exception as e:
                                    print("Error", e)
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # Print text/plain emails and skip attachments
                                print("Body:", body)
                                break
                    else:
                        # If the email is not multipart, just get the payload
                        body = msg.get_payload(decode=True).decode()

                    body = re.sub(r'\r\n', '\n', body)
                    emails.append(
                        {'from': email_from, 'subject': email_subject, 'body': body, "written_from_lawyer": 0})

        mail.logout()
        return emails
