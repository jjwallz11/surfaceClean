# app/utils/email.py

async def send_password_reset_email(email: str, token: str):
    reset_link = f"https://your-frontend-app.com/reset-password?token={token}"
    print(f"🔐 Send this link to {email}: {reset_link}")
    # TODO: Integrate real mail service like SendGrid or SMTP