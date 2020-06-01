import smtplib

host = "smtp.gmail.com"
subject = "writting"
sender = "akitestmessage@gmail.com"
pwd = "asada123Z"

class EmailSender:

    def __init__(self):
        self.host =host
        self.subject = subject
        self.sender = sender
        self.pwd = pwd

    def sendmsg(self, reciever, text):
        BODY = "\r\n".join((
            "From: %s" % self.sender,
            "To: %s" % reciever,
            "Subject: %s" % self.subject,
            "",
            text
        ))
        server = smtplib.SMTP_SSL(self.host, 465)
        server.login(self.sender, self.pwd)
        server.sendmail(self.sender, [reciever], BODY)
        server.quit()