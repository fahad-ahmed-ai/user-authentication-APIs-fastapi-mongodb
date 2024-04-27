import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.utilities.responses import success_response, error_response
from app.utilities.config import SEND_GRID_API_KEY, SEND_GRID_EMAIL


def Send_OTP(to_email, otp_code):
    message = Mail(
        from_email=SEND_GRID_EMAIL,
        to_emails=to_email,
        subject="Password Reset OTP",
        html_content=f"""
            <p>Dear User,</p>
            <p>We received a request to reset your password. To ensure the security of your account, please enter the One-Time Password (OTP) provided below:</p>
            <p>OTP: {otp_code}</p>
            <p>If you did not initiate this password reset request, please ignore this email and ensure that your account remains secure.</p>
            <p>Thank you for using the AI Chat Bot.</p>
            <p>Best regards,<br>Fahad Ahmed AI</p>
        """,
    )

    try:
        sg = SendGridAPIClient(SEND_GRID_API_KEY)
        sg.send(message)
        response = success_response(msg= "Email Sent Successfully")
        return response
    except Exception as e:
        return error_response(msg="Failed", exception=e)