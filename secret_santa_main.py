import secret_santa_lib

import copy
from email.mime.text import MIMEText
import random
import smtplib
import ssl

SMTP_SERVER = 'smtp.gmail.com'
PORT = 465
SECRET_SANTA = input('Type Secret Santa server email address and press enter: ')
PASSWORD = input('Type password and press enter: ')
PARTICIPANTS_PATH = input('Enter path to participants file, one comma-separated '
                      'name and email address per line: ')
DO_NOT_MATCH_PATH = input(
    '(optional) Enter path to exclusions file, each line is a comma-separated list of '
    'email addresses that should not be matched together: ')

def main():
  santa = secret_santa_lib.Santa(PARTICIPANTS_PATH, DO_NOT_MATCH_PATH)
  matches = santa.match()

  # Create a secure SSL context
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
    server.login(SECRET_SANTA, PASSWORD)
    for sender_id, receiver_id in matches.items():
      sender = santa.get_person(sender_id)
      receiver = santa.get_person(receiver_id)
      msg = MIMEText(
          f'Ho ho ho. {sender.name()}, my elf, please prepare a gift for {receiver.name()}.')
      msg['Subject'] = f'Secret Santa assignment'
      server.sendmail(SECRET_SANTA, sender.email(), msg.as_string())


if __name__ == '__main__':
  main()
