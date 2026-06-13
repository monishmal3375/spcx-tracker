import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, html_body, is_urgent=False):
    sender_email = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient_email = os.environ.get("DAD_EMAIL")
    if not all([sender_email, sender_password, recipient_email]):
        print("ERROR: Missing email credentials in environment variables.")
        return False
    if is_urgent:
        subject = f"🚨 {subject}"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"SPCX Tracker <{sender_email}>"
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_body, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent successfully: {subject}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
