from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from subprocess import Popen, PIPE

def send(from_address, to_address, subject, text, attachment_filename=None, attachment_bytes=None):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    if attachment_filename is not None:
        def make_attachment(attach_bytes):
            attachment = MIMEApplication(attach_bytes, 'subtype')
            attachment['Content-Disposition'] = 'attachment; filename="{}";'.format(attachment_filename)
            msg.attach(attachment)

        if attachment_bytes is None:
            with open(attachment_filename, 'rb') as f:
                make_attachment(f.read())
        else:
            make_attachment(attachment_bytes)

    p = Popen(["/usr/sbin/sendmail", "-i", "-t"], stdin=PIPE)
    message_str = msg.as_string()
    p.communicate(bytes(message_str, "utf-8"))


def send_safe(from_address, to_address, subject, text, attachment_filename=None):
    try:
        send(from_address, to_address, subject, text, attachment_filename)
        return True
    except Exception as e:
        # fixme: put to log
        return False
