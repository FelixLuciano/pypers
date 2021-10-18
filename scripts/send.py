from build import get_config, build
from getpass import getpass
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_message(config):
    mail_html, mail_text, meta = build(config, True)
    
    message = MIMEMultipart("alternative")
    message["Subject"] = meta["subject"]
    message["From"] = meta["name"]

    part1 = MIMEText(mail_text, "text")
    part2 = MIMEText(mail_html, "html")

    message.attach(part1)
    message.attach(part2)

    return message


def get_subscribers():
    with open("subscribers.txt", "r", encoding="utf-8") as subscribers_file:
        subscribers = list(subscribers_file.readlines())

    return subscribers


def dispatch_message(server, sender_email, message):
    subscribers = get_subscribers()
    size = len(subscribers)
    index = 1

    for subscriber in subscribers:
        reciver_mail = subscriber.strip()
        message["To"] = reciver_mail

        print(f"Sending {index} of {size}...")
        server.sendmail(sender_email, reciver_mail, message.as_string())

        index += 1


def get_smtp_server(config):
    smtp = config["transport"]["smtp"]
    context = ssl.create_default_context()
    smtp_server = smtplib.SMTP_SSL(smtp, 465, context=context)
    sender_email = config["transport"]["mail"]
    password = getpass("E-mail password:")

    smtp_server.login(sender_email, password)
    print("Login successfully!")

    return smtp_server


def send(message, config):
    smtp_server = get_smtp_server(config)
    sender_email = config["transport"]["mail"]

    with smtp_server as server:
        dispatch_message(server, sender_email, message)

    print("Newsletter launched successfully!")


if __name__ == "__main__":
    config = get_config()
    message = get_message(config)

    do_send = input("Send? (yes/no) ")

    if do_send.lower() in ("y", "yes"):
        send(message, config)
