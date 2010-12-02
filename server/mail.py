import smtplib
from email.mime.text import MIMEText
import datetime
import time


MAIL_HOST = 'localhost'

# for this to work, we need to install postfix on the server like so:
# sudo apt-get install postfix


# sender: an email address like "mirvestigator@systemsbiology.org"
# receivers: an array of email addresses
# subject: a string
# body: a string
def send(sender, receivers, subject="", body=""):
    # sender = "mirvestigator@systemsbiology.org"
    # receivers = ["cbare@systemsbiology.org", "christopherbare@gmail.com"]
    # subject = "flippety doo"
    # body = "This is a totally bogus message."

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sender, ", ".join(receivers), subject, body)

    try:
       s = smtplib.SMTP(MAIL_HOST)
       s.sendmail(sender, receivers, message)         
       s.quit()
    except Exception as e:
       print "Error: unable to send email"
       print e

class AdminEmailer:
    mirv = 'mirvestigator@systemsbiology.org'
    admins = ['cplaisier@systemsbiology.org', 'cbare@systemsbiology.org']
    sent_at = None
    two_hours = timedelta(hours=2)

    def warn(message):
        t = datetime.datetime.now()
        if (sent_at and t < sent_at + two_hours):
            # suppress sending emails too often
            return
        sent_at = t
        send(mirv, admins, "miRvestigator warning", message)

