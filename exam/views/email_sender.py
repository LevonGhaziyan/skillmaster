import smtplib
import ssl
import threading
import os
from dotenv import load_dotenv

load_dotenv()
EMIL_USERNAME = os.getenv("EMAIL_USERNAME", default = "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", default = "")

from threading import Thread

class EmailSender(threading.Thread):
    def __init__(self, subject, message, receiver_email):
        self.port = 587
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = EMIL_USERNAME
        self.receiver_email = receiver_email
        self.password = EMAIL_PASSWORD
        self.subject = subject
        self.message = message

        threading.Thread.__init__(self)

    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message)
    
    def run(self):
        self.send_email()