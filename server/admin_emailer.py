import smtplib
from email.mime.text import MIMEText
import datetime
import sys


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
       print >> sys.stderr, "Error: unable to send email"
       print >> sys.stderr, e
       sys.stderr.flush()

class AdminEmailer:
    def __init__(self):
        self.mirv = 'mirvestigator@systemsbiology.org'
        self.admins = ['cbare@systemsbiology.org']
        self.sent_at = None
        self.two_hours = datetime.timedelta(hours=2)

    def warn(self, message):
        try:
            t = datetime.datetime.now()
            if (self.sent_at is not None and t < self.sent_at + self.two_hours):
                # suppress sending emails too often
                return
            self.sent_at = t
            send(self.mirv, self.admins, subject="miRvestigator warning", body=message)
            print >> sys.stderr, "sent a warning email at %s" % (str(t))
            sys.stderr.flush()
        except Exception as e:
            print >> sys.stderr, e
            sys.stderr.flush()

if __name__ == '__main__':
    adminEmailer = AdminEmailer()
    adminEmailer.warn("Disaster!!!")
