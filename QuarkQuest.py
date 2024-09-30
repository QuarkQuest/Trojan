import smtplib
import socket
from getpass import getpass
from requests import get
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
public_ip = get('http://api.ipify.org').text

gmail_sender = 'tester8977@gmail.com'
gmail_passwd = '7gM-UUD-zUh-zFa'

TO = 'egor40361@gmail.com'
SUBJECT = 'TEST MAIL'
TEXT = 'Here is a message from python.'

server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.login(gmail_sender,gmail_passwd)

BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()