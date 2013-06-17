'''
TS Mailer, class for sending emails in django using template system
It works as a wrapper for EmailMessage
'''
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
'''
getting project.settings
'''
try:
    from settings import EMAIL_SUBJECT_PREFIX
except ImportError:
    EMAIL_SUBJECT_PREFIX = '[TS_MAILER]'

try:
    from settings import EMAIL_USER_FROM_DEFAULT
except ImportError:
    EMAIL_USER_FROM_DEFAULT = 'TS_MAILER <TS@example.com>'

'''
If setting exists, we verify if it finishes in / and add it if required
'''
try:
    from settings import EMAIL_TEMPLATE_FOLDER
    if len(EMAIL_TEMPLATE_FOLDER):
        if EMAIL_TEMPLATE_FOLDER[-1] != '/':
            EMAIL_TEMPLATE_FOLDER = EMAIL_TEMPLATE_FOLDER + '/'
except Exception, e:
    EMAIL_TEMPLATE_FOLDER = 'mail/'


#Exception when there are not users
class UserEmpty(Exception):
    def __init__(self):
        self.value = 'Mail class has no recipient(s) defined'

    def __str__(self):
        return repr(self.value)


class Mailer:
    '''
Class Mail

'''
    #TODO: 'privatize' this
    subject = ''
    users = []  # a list of django auth user objects, can be a queryset
    message = ''
    from_field = EMAIL_USER_FROM_DEFAULT
    is_html = True
    __email_obj = None

    def __init__(self):
        self.__email_obj = EmailMessage()
        self.recipients = []

    # if we want to send a message to one user (and it doesn't have user data associated in email body)
    def send(self):
        if not self.users:
            raise UserEmpty()

    #
        for user in self.users:
            self.recipients.append('%s %s <%s>' % (user.first_name, user.last_name, user.email))
        self.__email_obj.to = self.recipients
        self.__email_obj.subject = EMAIL_SUBJECT_PREFIX + self.subject
        if isinstance(self.message, str):
            self.__email_obj.body = self.message
        else:
            self.__email_obj.body = render_to_string('%s%s' % (EMAIL_TEMPLATE_FOLDER, self.message[0]), self.message[1])

        self.__email_obj.from_email = self.from_field
        self.__email_obj.headers = {'Content-type': 'text/html'}
        if self.is_html:
            self.__email_obj.content_subtype = 'html'
        else:
            self.__email_obj.content_subtype = 'text'
        self.__email_obj.send()

    # This function is used when we want to send custom messages to many users
    def send_mass(self):
    # if users are not set then raises exception
        if not self.users:
            raise UserEmpty()
        for user in self.users:
            self.recipients.append('%s %s <%s>' % (user.first_name, user.last_name, user.email))
        self.__email_obj.connection = get_connection()
        for i, recipient in enumerate(self.recipients):
            self.__email_obj.to = [recipient]
            self.__email_obj.subject = EMAIL_SUBJECT_PREFIX + self.subject
            self.message[1]['user'] = self.users[i]
            if isinstance(self.message, str):
                self.__email_obj.body = self.message
            else:
                self.__email_obj.body = render_to_string('%s%s' % (EMAIL_TEMPLATE_FOLDER, self.message[0]), self.message[1])
            self.__email_obj.from_email = self.from_field
            self.__email_obj.headers = {'Content-type': 'text/html'}
            if self.is_html:
                self.__email_obj.content_subtype = 'html'
            else:
                self.__email_obj.content_subtype = 'text'
            self.__email_obj.send()

    #template: template's name, this file will be in template/mail/ folder
    #context: variables to template
    #Note: user context variable will be overwrite when using send mass
    def setMessage(self, template, context={}):
        #self.message = render_to_string('mail/%s'%template, context)
        self.message = (template, context)
        return self

    def setMessageOnlyText(self, message):
        self.message = message
        return self
        
    def addUser(self, user):
        self.users.append(user)
        return self

    def setUsers(self, users):
        self.users = users
        return self
        
    def getUsers(self):
        return self.users
    
    def setSender(self, sender):
        self.from_field = sender
        return self
        
    def getSender(self):
        return self.from_field
    
    def EmailMessageInstance(self):
        return self.__email_obj


def test():
    from django.contrib.auth.models import User
    users = []
    users.append(User.objects.get(username='admin'))
    users.append(User.objects.get(username='sunno'))
    mail = Mailer()
    mail.users = users
    mail.set_message('test.html', {'test': 'blablaa'})
    mail.subject = 'test email'
    mail.send()
