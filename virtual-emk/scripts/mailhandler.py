import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


smtpserver = 'se-smtp.ericsson.se'
sender = 'vemk'
dest  = "emil.saren@ericsson.com"
text_type = 'plain'

class SmtpMsg(object):
    def __init__(self):
        self.resetText()

    def appendText(self, text):
        """
        Appends a list of text to the current message
        :param text: List with text items
        :return: void
        """
        if len(text) < 1:
            return
        attach_text = ''
        for item in text:
            attach_text += item
            attach_text += '\n'
        attach_text += '\n\n'
        self.part = MIMEText(self.part.get_payload() + attach_text, text_type)


    def resetText(self):
        """
        Resets the payload in the mime text
        :return: void
        """
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = sender
        self.msg['To'] = dest
        self.msg['Subject'] = "V Kim K Report"
        self.part = MIMEText('')

    def sendemail(self):
        """
        Sends email with the appended content
        :return: void
        """
        smtpconn = smtplib.SMTP(smtpserver, 25)
        self.msg.attach(self.part)
        try:
            smtpconn.sendmail(sender, dest, self.msg.as_string())
        finally:
            smtpconn.close()
