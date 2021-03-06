#################################################################
# @Program: miRvestigator                                       #
# @Version: 2                                                   #
# @Author: Chris Plaisier                                       #
# @Author: Christopher Bare                                     #
# @Sponsored by:                                                #
# Nitin Baliga, ISB                                             #
# Institute for Systems Biology                                 #
# 1441 North 34th Street                                        #
# Seattle, Washington  98103-8904                               #
# (216) 732-2139                                                #
# @Also Sponsored by:                                           #
# Luxembourg Systems Biology Grant                              #
#                                                               #
# If this program is used in your analysis please mention who   #
# built it. Thanks. :-)                                         #
#                                                               #
# Copyright (C) 2010 by Institute for Systems Biology,          #
# Seattle, Washington, USA.  All rights reserved.               #
#                                                               #
# This source code is distributed under the GNU Lesser          #
# General Public License, the text of which is available at:    #
#   http://www.gnu.org/copyleft/lesser.html                     #
#################################################################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import sys
import traceback


MAIL_HOST = 'mailhost'


notify_msg_text_template = """Your miRvestigator job %(job_name)s is finished.

Your results can be retrieved at:
http://mirvestigator.systemsbiology.net/results/%(job_uuid)s/

job id: %(job_uuid)s
completed at: %(time)s

Thanks for using mirVestigator.
"""

notify_msg_html_template = """<html>
<head></head>
<body>
<p>Your miRvestigator job %(job_name)s is finished.</p>

<p>Your results can be retrieved <a href="http://mirvestigator.systemsbiology.net/results/%(job_uuid)s/">http://mirvestigator.systemsbiology.net/results/%(job_uuid)s/</a>.</p>

<p>job id: %(job_uuid)s<br />
completed at: %(time)s</p>

<p>Thanks for using mirVestigator.</p>
</body>
</html>
"""


notify_error_msg_text_template = """Sorry, your miRvestigator job %(job_name)s failed.

job id: %(job_uuid)s
completed at: %(time)s
"""

notify_error_msg_html_template = """<html>
<head></head>
<body>
<p>Sorry, your miRvestigator job %(job_name)s failed.</p>

<p>job id: %(job_uuid)s<br />
completed at: %(time)s</p>

</body>
</html>
"""

message_template = """From:%s
To:%s
Subject:%s

%s
"""


# for this to work, we need to install postfix on the server like so:
# sudo apt-get install postfix


# sender: an email address like "mirvestigator@systemsbiology.org"
# recipients: an array of email addresses
# subject: a string
# body: a string
def send(sender, recipients, subject="", body=""):
    # sender = "mirvestigator@systemsbiology.org"
    # recipients = ["cbare@systemsbiology.org", "christopherbare@gmail.com"]
    # subject = "flippety doo"
    # body = "This is a totally bogus message."

    message = message_template % (sender, ", ".join(recipients), subject, body)

    try:
       s = smtplib.SMTP(MAIL_HOST)
       s.sendmail(sender, recipients, message)         
       s.quit()
    except Exception as e:
       print >> sys.stderr, "Error: unable to send email."
       traceback.print_stack()
       traceback.print_exc()
       sys.stderr.flush()


def sendHtml(sender, recipients, subject, text, html):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ",".join(recipients)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    try:
       s = smtplib.SMTP(MAIL_HOST)
       s.sendmail(sender, recipients, msg.as_string())         
       s.quit()
    except Exception as e:
       print >> sys.stderr, "Error: unable to send email.."
       traceback.print_stack()
       traceback.print_exc()
       sys.stderr.flush()


class AdminEmailer:
    def __init__(self):
        self.mirv = 'noreply@noreply.systemsbiology.net'
        self.admins = ['wwu@systemsbiology.org', 'cplaisier@systemsbiology.org']
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
            traceback.print_stack()
            traceback.print_exc()
            sys.stderr.flush()

    def notify_complete(self, recipients, job_uuid, job_name):
        try:
            t = datetime.datetime.now()
            text_msg = notify_msg_text_template % {"job_uuid":job_uuid, "job_name":job_name, "time":t.strftime('%Y.%m.%d %H:%M:%S')}
            html_msg = notify_msg_html_template % {"job_uuid":job_uuid, "job_name":job_name, "time":t.strftime('%Y.%m.%d %H:%M:%S')}
            sendHtml(self.mirv, recipients=recipients, subject="miRvestigator job complete", text=text_msg, html=html_msg)
            print >> sys.stderr, "sent a notification email to %s at %s" % (", ".join(recipients), t.strftime('%Y.%m.%d %H:%M:%S'))
            sys.stderr.flush()
        except Exception as e:
            traceback.print_stack()
            traceback.print_exc()
            sys.stderr.flush()

    def notify_error(self, recipients, job_uuid, job_name):
        try:
            t = datetime.datetime.now()
            text_msg = notify_error_msg_text_template % {"job_uuid":job_uuid, "job_name":job_name, "time":t.strftime('%Y.%m.%d %H:%M:%S')}
            html_msg = notify_error_msg_html_template % {"job_uuid":job_uuid, "job_name":job_name, "time":t.strftime('%Y.%m.%d %H:%M:%S')}
            sendHtml(self.mirv, recipients=recipients, subject="miRvestigator job complete", text=text_msg, html=html_msg)
            print >> sys.stderr, "sent a notification error email to %s at %s" % (", ".join(recipients), t.strftime('%Y.%m.%d %H:%M:%S'))
            sys.stderr.flush()
        except Exception as e:
            traceback.print_stack()
            traceback.print_exc()
            sys.stderr.flush()

if __name__ == '__main__':
    adminEmailer = AdminEmailer()
    adminEmailer.warn("Test Disaster!!!")
