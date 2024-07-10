import os
import smtplib, ssl
from dotenv import load_dotenv


port = 587
smtp_server = "smtp.gmail.com"
load_dotenv()
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
password = os.environ.get("PASSKEY")

print(sender_email, receiver_email, password)


def send_email(message):
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted, called implicitly by the method if required
            server.starttls(context=context)
            server.ehlo()  # Can be omitted, called implicitly by the method if required
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Sent email with message:", message)
    except Exception as error:
        print("Error:\n", error)


test = False

if __name__ == "__main__":
    if test:
        message = """\
Subject: Test for trade-bot, remove from spam

This is a test email for a tradeing system in development. Please remove from spam to ensure further messages get received"""
    send_email(message=message)
