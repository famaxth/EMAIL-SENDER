# -*- coding: utf-8 -*-

import os
import time
import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from tqdm import tqdm

from settings import EMAIL, PASSWORD


banner = """
╔==========================================================================================================╗
║                                                                                                          ║
║        ███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗███████╗███╗   ██╗██████╗ ███████╗██████╗       ║
║        ██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗      ║
║        █████╗  ██╔████╔██║███████║██║██║         ███████╗█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝      ║
║        ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ╚════██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗      ║
║        ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████║███████╗██║ ╚████║██████╔╝███████╗██║  ██║      ║
║        ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝      ║
╚==========================================================================================================╝
"""


def send_email(type, recipient, path=None, text=None, path_to_text=None, path_to_audio=None, path_to_image=None, path_to_application=None, subject=None):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(EMAIL, PASSWORD)
    except:
        login = input("\nEnter the login: ")
        password = input("Enter the password: ")
        with open('login.txt', 'w') as file_login:
            file_login.write(login)
        with open('password.txt', 'w') as file_password:
            file_password.write(password)
        server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()

    try:
        msg["From"] = EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        if type == 1:
            file = MIMEText(text)
            msg.attach(file)
            print("\nSending...")
        elif type == 2:
            filename = os.path.basename(path)
            ftype = mimetypes.guess_type(path)
            subtype = str((ftype[0].split("/"))[0])
            with open(path, 'rb') as f:
                file = MIMEAudio(f.read(), subtype)
                file.add_header('Content-Disposition', 'attachment',
                                filename=filename)
            msg.attach(file)
            print("\nSending...")
        elif type == 3:
            filename = os.path.basename(path)
            ftype = mimetypes.guess_type(path)
            subtype = str((ftype[0].split("/"))[0])
            with open(path, 'rb') as f:
                file = MIMEImage(f.read(), subtype)
                file.add_header('Content-Disposition', 'attachment',
                                filename=filename)
            msg.attach(file)
            print("\nSending...")
        elif type == 4:
            filename = os.path.basename(path)
            ftype = mimetypes.guess_type(path)
            subtype = str((ftype[0].split("/"))[0])
            with open(path, 'rb') as f:
                file = MIMEApplication(f.read(), subtype)
                file.add_header('Content-Disposition', 'attachment',
                                filename=filename)
            msg.attach(file)
            print("\nSending...")
        else:
            print("\nCollecting...")
            time.sleep(0.4)

            with open(path_to_text) as f:
                filename = os.path.basename(path_to_text)
                ftype = mimetypes.guess_type(path_to_text)
                file = MIMEText(f.read())
                file.add_header('content-disposition',
                                'attachment', filename=filename)
                msg.attach(file)
            with open(path_to_image, "rb") as f:
                filename = os.path.basename(path_to_image)
                ftype = mimetypes.guess_type(path_to_image)
                subtype = str((ftype[0].split("/"))[0])
                file = MIMEImage(f.read(), subtype)
                file.add_header('content-disposition',
                                'attachment', filename=filename)
                msg.attach(file)
            with open(path_to_audio, "rb") as f:
                filename = os.path.basename(path_to_audio)
                ftype = mimetypes.guess_type(path_to_audio)
                subtype = str((ftype[0].split("/"))[0])
                file = MIMEAudio(f.read(), subtype)
                file.add_header('content-disposition',
                                'attachment', filename=filename)
                msg.attach(file)
            with open(path_to_application, "rb") as f:
                filename = os.path.basename(path_to_application)
                ftype = mimetypes.guess_type(path_to_application)
                subtype = str((ftype[0].split("/"))[0])
                file = MIMEApplication(f.read(), subtype)
                file.add_header('content-disposition',
                                'attachment', filename=filename)
                msg.attach(file)

        server.sendmail(EMAIL, recipient, msg.as_string())
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    print(banner)
    print("[?] Github - https://github.com/famaxth/EMAIL-SENDER")
    print("[?] Author - famaxth")

    recipient = input("\n[*] Enter the recipient's address: ")
    subject = input("[*] Enter the subject of the message: ")
    type_of_message = int(input(
        "\n[01] text\n[02] audio\n[03] image\n[04] application\n[05] all\n\n[*] The type of message being sent: "))

    if type_of_message == 1:
        text = input("[*] Type your text: ")
        print(send_email(type=type_of_message,
                         recipient=recipient, text=text, subject=subject))
    elif type_of_message != 5:
        path = input("[*] Enter the path to the file: ")
        print(send_email(type=type_of_message,
                         recipient=recipient, path=path, subject=subject))
    else:
        path_to_text = input("[*] Enter the path to the file (text): ")
        path_to_audio = input("[*] Enter the path to the file (audio): ")
        path_to_image = input("[*] Enter the path to the file (image): ")
        path_to_application = input(
            "[*] Enter the path to the file (application): ")
        print(send_email(type=type_of_message, recipient=recipient, path_to_text=path_to_text, path_to_audio=path_to_audio,
                         path_to_image=path_to_image, path_to_application=path_to_application, subject=subject))


if __name__ == "__main__":
    main()
