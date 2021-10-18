#Notes:
#1. For some reason only the previously saved video is being sent and not the immediate video
#2. Can't put print statements in the program for some reason





import time, glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime
from email import encoders
import os
import sys


COMMASPACE = ', '

# Settings:
fromemail = 'RAE SECURITY <raeprojectthrowaway123@gmail.com> '
loginname = 'raeprojectthrowaway123@gmail.com'
loginpassword = '19r23919r20319r253'
toemail = 'RAE SECURITY <raeprojectthrowaway123@gmail.com> '
SMTPserver = 'smtp.gmail.com'
SMTPort = 587
fileslocation = 'MPMCProject/videos/*'
subject = "Random shit for now"
log = 'logfile.txt'


def mainloop():
    print("Start")
    files = glob.glob(fileslocation)  # Put whatever path and file format you're using in there.
    print("Loop start:")
    while 1:
        f = open(log, 'w')
        sys.stdout = Tee(sys.stdout, f)
        new_files = glob.glob(fileslocation)
        if len(new_files) > len(files):
            for x in new_files:
                if x in files:
                    #print(str(datetime.datetime.now()) + "New file detected " + x)
                    sendMail(loginname, loginpassword, toemail, fromemail, subject, gettext(), x, SMTPserver, SMTPort)
        files = new_files
        f.close()
        time.sleep(1)
    print("Not loop")

def sendMail(login, password, send_to, send_from, subject, text, send_file, server, port):
    #print("Sending Mail")
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(send_file, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(send_file))
    msg.attach(part)

    smtp = smtplib.SMTP(SMTPserver, SMTPort)
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(login, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def gettext():
    text = "A new file has been added to the security footage folder. \nTime Stamp: " + str(datetime.datetime.now())
    return (text)


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)


# Execute loop
mainloop()
