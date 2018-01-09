import smtplib
import json

with open('config.json') as data_file:
    config = json.load(data_file)

smtpUsername = config["email"]["smtpUsername"]
smtpPassword = config["email"]["smtpPassword"]
smtpUrl = config["email"]["smtpUrl"]
sender = config["email"]["sender"]
reciepent = config["email"]["reciepent"]

server = smtplib.SMTP(smtpUrl, timeout=5)
server.starttls()
server.set_debuglevel(True)
server.login(smtpUsername, smtpPassword)

msg = "\nMessage test"

server.sendmail(sender, reciepent, msg)
server.quit()