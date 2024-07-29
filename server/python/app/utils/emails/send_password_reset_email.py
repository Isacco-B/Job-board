from ..helpers import send_email

def send_password_reset_email(email, token):
    resetLink = f"http://localhost:4000/api/auth/new-password/${token}"
    text = f"Please click on the following link to reset your password: ${resetLink}"
    html = f"<p>Click <a href=${resetLink}>here</a> to reset your password</p>"
    send_email(
        email,
        "Password Reset Request",
        "emails/password_reset",
        token=token,
    )
