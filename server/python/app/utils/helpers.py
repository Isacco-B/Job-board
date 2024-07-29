from flask_mail import Mail, Message
from ..secrets import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
)

app.config["MAIL_SERVER"] = EMAIL_HOST
app.config["MAIL_PORT"] = EMAIL_PORT
app.config["MAIL_USERNAME"] = EMAIL_ADDRESS
app.config["MAIL_PASSWORD"] = EMAIL_PASSWORD
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

def send_email(email, subject, template, **kwargs):
    msg = Message(
        subject,
        recipients=[email],
        html=template,
    )
    mail.send(msg)
