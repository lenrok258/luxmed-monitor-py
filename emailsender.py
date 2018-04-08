import json
import smtplib

from logger import Logger

log = Logger()

with open('config.json') as data_file:
    config = json.load(data_file)

smtpUsername = config["email"]["smtpUsername"]
smtpPassword = config["email"]["smtpPassword"]
smtpUrl = config["email"]["smtpUrl"]
smtpPort = config["email"].get("smtpPort") # optional
sender = config["email"]["sender"]
recipient = config["email"]["recipient"]


def send_email(message):
    email = """From: Lux Med monitor <{}>
To: Szukajacy lekarza {}
Subject: Lux med monitor mowi czesc

Cos sie stalo: 
{}
""".format(sender, recipient, message)

    msg = {}
    msg['Subject'] = 'Test'
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP(host=smtpUrl, port=smtpPort, timeout=5)
        server.starttls()
        server.set_debuglevel(True)
        server.login(smtpUsername, smtpPassword)
        server.sendmail(sender, recipient, email)
        server.quit()
    except Exception as e:
        log.warn("Unable to send email. Error was: {}", e)
