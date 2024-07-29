from ..helpers import send_email


def send_verification_email(email, token):
    resetLink = f"http://localhost:4000/api/auth/new-verification/${token}"
    text = f"Please click on the following link to verify your email: ${resetLink}"
    html = f"<p>Click <a href=${resetLink}>here</a> to verify your email</p>"
    send_email(
        email,
        "Password Reset Request",
        "emails/password_reset",
        token=token,
    )
