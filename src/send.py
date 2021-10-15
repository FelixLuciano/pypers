import json
from getpass import getpass
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import build
import helper

with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
  
do_send = helper.valid_input(str, "Deseja disparar os e-mails? (s/n) ", ("S", "SIM"), persist=False, apply=str.upper)

if do_send:
    password = getpass("Insira a senha da conta de envio:")
    sender_email = config["email"]["address"]

    message = MIMEMultipart("alternative")
    message["Subject"] = config["news"]["subject"]
    message["From"] = config["news"]['name']

    part1 = MIMEText(build.mail_text, "text")
    part2 = MIMEText(build.mail_html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config["email"]["smtp"], 465, context=context) as server:
        server.login(sender_email, password)

        with open("subscribers.txt", "r", encoding="utf-8") as subscribers_file:
            subscribers = list(subscribers_file.readlines())

        i = 1
        for subscriber in subscribers:
            mail = subscriber.strip()
            message["To"] = mail

            print(f"Enviando mensagem {i} de {len(subscribers)}...")
            i += 1

            server.sendmail(sender_email, mail, message.as_string())

    print("Newsletter disparada com sucesso!")
