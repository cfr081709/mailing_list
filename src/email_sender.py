import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv
from mysql.connector import Error, connect

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_recipients():
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "mailing_list")

    connection = None
    try:
        connection = connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM emails")
        rows = cursor.fetchall()
        return [email for (email,) in rows if email]
    except Error as exc:
        raise RuntimeError(f"MySQL error: {exc}") from exc
    finally:
        if connection and connection.is_connected():
            connection.close()


def send_email():
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        raise RuntimeError("Set EMAIL_SENDER and EMAIL_PASSWORD environment variables first.")

    recipients = get_recipients()

    if not recipients:
        raise ValueError("No email addresses were found in the database.")

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