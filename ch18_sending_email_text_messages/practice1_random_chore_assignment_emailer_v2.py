#! /usr/bin/env python3
# random_chore_assignment_emailer.py
# Randomly assigns chores to people. Emails each person their assigned chores.
# V2 keeps a record of each person’s previously assigned chores
# so the program avoids assigning anyone the same chore they did last time.

import random, smtplib, pprint, os
from dotenv import load_dotenv

emails = [
    'email1@example.com',
    'email2@example.com'
]
chores = ['wash socks', 'clean shoes', 'vacuum', 'wash dishes', 'clean bathroom', 'wipe dust']

assigned_chores = {}

if os.path.exists('assigned_chores_record.py'):
    from assigned_chores_record import assigned_chores as previously_assigned_chores
else:
    previously_assigned_chores = None

while chores:
    random_chore = random.choice(chores)
    chores.remove(random_chore)    # this chore is now taken, so remove it

    emails_to_choose_from = emails[:]  # fastest technique to clone list without referencing original list
    if previously_assigned_chores:
        for email in previously_assigned_chores:
            if random_chore in previously_assigned_chores[email]:
                emails_to_choose_from.remove(email)
                break
    random_email = random.choice(emails_to_choose_from)
    assigned_chores.setdefault(random_email, [])
    assigned_chores[random_email].append(random_chore)

with open('assigned_chores_record.py', 'w') as file:
    file.write('assigned_chores = ' + pprint.pformat(assigned_chores))

load_dotenv()
SMTP_SERVER_HOST = os.environ.get('SMTP_SERVER_HOST')
SMTP_SERVER_PORT = int(os.environ.get('SMTP_SERVER_PORT'))
SMTP_SERVER_USERNAME = os.environ.get('SMTP_SERVER_USERNAME')
SMTP_SERVER_PASSWORD = os.environ.get('SMTP_SERVER_PASSWORD')
EMAIL_ADDRESS_FROM = os.environ.get('EMAIL_ADDRESS_FROM')

smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
smtp_obj.ehlo()
smtp_obj.login(SMTP_SERVER_USERNAME, SMTP_SERVER_PASSWORD)

for email in assigned_chores:
    smtp_obj.sendmail(EMAIL_ADDRESS_FROM, email, 'Subject: Your assigned chores\n' + '\n'.join(assigned_chores[email]))

smtp_obj.quit()
