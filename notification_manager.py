import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)
        self.my_email = os.environ["MY_EMAIL"]
        self.app_password = os.environ["MY_APP_PASSWORD"]

    def send_whatsapp(self, msg_body):
        message = self.client.messages.create(
            from_="whatsapp:+14155238886",
            body=msg_body,
            to="whatsapp:+12055677883"
        )
        print(message.sid)

    def send_email(self, customer_emails, email_body):
        connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
        with connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.app_password)
            for email in customer_emails:
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=email,
                    msg=f"Subject: Low Price Alert!\n\n{email_body}".encode("utf-8")
                )

