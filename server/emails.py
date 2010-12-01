import smtplib
from email.mime.text import MIMEText


sender = "mirvestigator@systemsbiology.org"
receivers = ["cbare@systemsbiology.org", "christopherbare@gmail.com"]

subject = "flippety doo"

body = "This is a totally bogus message. Blippety bonk. Flapgaster poodle pucky. Snorklewacker splat sploot gloosh. - mirv"

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender, ", ".join(receivers), subject, body)

try:
   s = smtplib.SMTP()
   s.sendmail(sender, receivers, message)         
   s.quit()
   print "Successfully sent email"
except Exception as e:
   print "Error: unable to send email"
   print e
