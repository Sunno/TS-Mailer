TS-Mailer
=========

A class for sending emails in django using template system

Configuration
_____________
settings.py

EMAIL_USER_FROM_DEFAULT = 'Example <no-reply@example.com>'
EMAIL_TEMPLATE_FOLDER = 'email'
EMAIL_SUBJECT_PREFIX = '[MySN]'

Example of usage:
_________________
from django.contrib.auth.models import User
users = []
users.append(User.objects.get(username='admin'))
users.append(User.objects.get(username='sunno'))
mail = Mailer()
mail.users = users
mail.set_message('test.html', {'test': 'blablaa'})
mail.subject = 'test email'
mail.send()
