#coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

import config
import dogpics

logger = logging.getLogger(__name__)

message_greetings = u"""
I found {} new flats!

"""

message_flat = u"""
Address: {addr}
Kiez: {kiez}

Cold rent: €{kalt}
Warm rent: €{total}

Size: {sqm} m²

Link: {link}
"""

html_message_flat = u"""
<p>
<a href="{link}"><b>Address</b>: {addr}</a> <br>
<b>Kiez</b>: {kiez} <br>

<b>Cold rent</b>: €{kalt}  <br>
<b>Warm rent</b>: €{total}  <br>

<b>Size</b>: {sqm} m²  <br>
</p>
"""


section = u"""
===
"""

html_section = u"""<hr>"""

dog = u"""
Dog: {dog}
"""

html_dog = u"""<p><img src="{dog}"></p>"""



def get_dogpic():
    try:
        return dogpics.get_random_dogpic()
    except Exception as e:
        logging.error(e)
        return dogpics.DEFAULTDOG


def create_html_email_body(flats, dogpic):
    flatmsgs = html_section.join([html_message_flat.format(**a) for a in flats])
    msg = message_greetings.format(len(flats)) + html_section + flatmsgs
    html = msg + html_section + html_dog.format(dog=dogpic)
    return html

def create_email_body(flats, dogpic):
    flatmsgs = section.join([message_flat.format(**a) for a in flats])
    msg = message_greetings.format(len(flats)) + section + flatmsgs
    plain = msg + section + dog.format(dog=dogpic)
    return plain

def create_email(flats, emails):
    dogpic = get_dogpic()

    msg = MIMEMultipart('alternative')

    plain = MIMEText(create_email_body(flats, dogpic), "text", _charset="utf-8")
    html = MIMEText(create_html_email_body(flats, dogpic), "html", _charset="utf-8")
    msg.attach(plain)
    msg.attach(html)

    msg['Subject'] = "Found {} new flats".format(len(flats))
    msg["From"] = config.email_from
    msg["To"] = ", ".join(emails)
    return msg

def send_email(flats, emails):
    msg = create_email(flats, emails)

    try:
        logger.info("Sending email to: {}".format(", ".join(emails)))
        s = smtplib.SMTP(config.smtp_server)
        s.sendmail(config.email_from, emails, msg.as_string())
        s.quit()
    except Exception as e:
        logger.error(e)
        raise
