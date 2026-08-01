import os
import smtplib
import pandas as pd
from email.message import EmailMessage


def send_email():
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        raise RuntimeError("Set EMAIL_SENDER and EMAIL_PASSWORD environment variables first.")

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'emails.csv')
    with open(csv_path, 'r', encoding='utf-8') as handle:
        rows = [line.strip() for line in handle if line.strip()]

    if not rows:
        raise ValueError("CSV file is empty.")

    if rows[0].lower().startswith('email'):
        recipients = [row.split(',')[0].strip().strip('"') for row in rows[1:]]
    else:
        recipients = [row.split(',')[0].strip().strip('"') for row in rows]

    recipients = [recipient for recipient in recipients if recipient]

    if not recipients:
        raise ValueError("No email addresses were found in the CSV file.")

    for recipient in recipients:
        recipient = str(recipient).strip()
        if not recipient:
            continue

        msg = EmailMessage()
        msg['Subject'] = 'Mailing List Test'
        msg['From'] = sender
        msg['To'] = recipient
        msg.set_content('This is a mailing list test.')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)

    print('emails sent')
    return

if __name__ == '__main__':
    send_email()