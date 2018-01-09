import json
import smtplib

with open('config.json') as data_file:
    config = json.load(data_file)

smtpUsername = config["email"]["smtpUsername"]
smtpPassword = config["email"]["smtpPassword"]
smtpUrl = config["email"]["smtpUrl"]
sender = config["email"]["sender"]
recipient = config["email"]["reciepent"]


def send_email(message):
    server = smtplib.SMTP(smtpUrl, timeout=5)
    server.starttls()
    server.set_debuglevel(True)
    server.login(smtpUsername, smtpPassword)
    server.sendmail(sender, recipient, message)
    server.quit()
