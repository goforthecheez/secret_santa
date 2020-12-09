import secret_santa_lib as santa

import copy
from email.mime.text import MIMEText
import random
import smtplib
import ssl

SMTP_SERVER = 'smtp.gmail.com'
PORT = 465
SECRET_SANTA = input('Type Secret Santa server email address and press enter: ')
PASSWORD = input('Type password and press enter: ')
PARTICIPANTS = input('Enter path to participants file, one comma-separated '
                      'name and email address per line: ')
EXCLUSIONS = input(
    'Enter path to exclusions file, each line is a comma-separated list of '
    'email addresses that should not be matched together: ')

def main():
  participants = santa.parse_participants(PARTICIPANTS)
  exclusions = santa.parse_bad_matches(EXCLUSIONS)
  matches = santa.match(participants, exclusions)

  # Create a secure SSL context
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
    server.login(SECRET_SANTA, PASSWORD)
    for sender_email, receiver_email in matches.items():
      sender = participants[sender_email]
      receiver = participants[receiver_email]
      msg = MIMEText(
          f'Ho ho ho. {sender}, my elf, please prepare a gift for {receiver}.')
      msg['Subject'] = f'Secret Santa assignment'
      server.sendmail(SECRET_SANTA, sender_email, msg.as_string())


if __name__ == '__main__':
  main()