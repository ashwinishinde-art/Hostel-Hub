"""
Utility functions for OTP generation, email, and SMS sending
"""

import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config.config import DevelopmentConfig as config

class OTPManager:
    """Manages OTP generation and validation"""
    
    @staticmethod
    def generate_otp(length=None):
        """Generate a random OTP"""
        if length is None:
            length = config.OTP_LENGTH
        digits = string.digits
        otp = ''.join(secrets.choice(digits) for _ in range(length))
        return otp
    
    @staticmethod
    def get_otp_expiry():
        """Get OTP expiry datetime"""
        expiry_minutes = config.OTP_EXPIRY_MINUTES
        return datetime.now() + timedelta(minutes=expiry_minutes)


class EmailService:
    """Handles email sending for OTP and password reset"""
    
    def __init__(self):
        self.smtp_server = config.MAIL_SERVER
        self.smtp_port = config.MAIL_PORT
        self.sender_email = config.MAIL_USERNAME
        self.sender_password = config.MAIL_PASSWORD
        self.default_sender = config.MAIL_DEFAULT_SENDER
        self.use_tls = config.MAIL_USE_TLS
    
    def send_otp_email(self, recipient_email, full_name, otp_code):
        """Send OTP to user's email"""
        try:
            subject = "Hostel Management - Password Reset OTP"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h2 style="color: #667eea; margin: 0;">HostelHub</h2>
                            <p style="color: #999; margin: 5px 0 0 0;">Hostel Management System</p>
                        </div>
                        
                        <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h3 style="color: #2c3e50; margin-top: 0;">Hello {full_name},</h3>
                            
                            <p>We received a request to reset your password. If you did not make this request, please ignore this email.</p>
                            
                            <p style="margin: 30px 0;">Your One-Time Password (OTP) is:</p>
                            
                            <div style="background: #f0f0f0; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                                <h1 style="color: #667eea; letter-spacing: 3px; margin: 0; font-size: 2.5em; font-weight: bold;">
                                    {otp_code}
                                </h1>
                            </div>
                            
                            <p style="color: #e74c3c; font-weight: bold;">⏰ This OTP will expire in {config.OTP_EXPIRY_MINUTES} minutes</p>
                            
                            <p style="margin: 30px 0; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px; color: #856404;">
                                <strong>⚠️ Security Tip:</strong> Never share this OTP with anyone. HostelHub support will never ask for your OTP.
                            </p>
                            
                            <p>If you need further assistance, please contact our support team.</p>
                            
                            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                            
                            <p style="color: #999; font-size: 0.9em; margin: 0;">
                                <strong>HostelHub Support Team</strong><br>
                                hostelhub@work.com | 7030710886<br>
                                © 2024 HostelHub. All rights reserved.
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
Hello {full_name},

We received a request to reset your password. If you did not make this request, please ignore this email.

Your One-Time Password (OTP) is:

    {otp_code}

⏰ This OTP will expire in {config.OTP_EXPIRY_MINUTES} minutes.

⚠️ Security Tip: Never share this OTP with anyone. HostelHub support will never ask for your OTP.

If you need further assistance, please contact our support team.

Best regards,
HostelHub Support Team
hostelhub@work.com | 7030710886
            """
            
            return self._send_email(recipient_email, subject, html_body, text_body)
            
        except Exception as e:
            print(f"Error sending OTP email: {e}")
            return False
    
    def send_password_reset_confirmation(self, recipient_email, full_name):
        """Send password reset confirmation email"""
        try:
            subject = "Hostel Management - Password Changed Successfully"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 8px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h2 style="color: #667eea; margin: 0;">HostelHub</h2>
                            <p style="color: #999; margin: 5px 0 0 0;">Hostel Management System</p>
                        </div>
                        
                        <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h3 style="color: #2c3e50; margin-top: 0;">Hello {full_name},</h3>
                            
                            <p style="font-size: 1.1em; color: #27ae60;">✓ Your password has been successfully changed!</p>
                            
                            <p>You can now log in with your new password at:</p>
                            <p style="text-align: center;"><a href="http://localhost:5000/login" style="color: #667eea; text-decoration: none; font-weight: bold;">Login to HostelHub</a></p>
                            
                            <p style="margin: 30px 0; padding: 15px; background: #f0f8ff; border-left: 4px solid #2196F3; border-radius: 4px; color: #01579b;">
                                <strong>💡 Tip:</strong> If you did not request this password change, please contact our support team immediately.
                            </p>
                            
                            <p>Your account security is important to us. If you have any concerns, please don't hesitate to reach out.</p>
                            
                            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">
                            
                            <p style="color: #999; font-size: 0.9em; margin: 0;">
                                <strong>HostelHub Support Team</strong><br>
                                hostelhub@work.com | 7030710886<br>
                                © 2024 HostelHub. All rights reserved.
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            text_body = f"""
Hello {full_name},

Your password has been successfully changed!

You can now log in with your new password at: http://localhost:5000/login

💡 Tip: If you did not request this password change, please contact our support team immediately.

Your account security is important to us.

Best regards,
HostelHub Support Team
hostelhub@work.com | 7030710886
            """
            
            return self._send_email(recipient_email, subject, html_body, text_body)
            
        except Exception as e:
            print(f"Error sending confirmation email: {e}")
            return False
    
    def _send_email(self, recipient_email, subject, html_body, text_body):
        """Internal method to send email"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.default_sender
            message['To'] = recipient_email
            
            # Attach text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✓ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"✗ Email authentication failed. Check MAIL_USERNAME and MAIL_PASSWORD in .env")
            return False
        except smtplib.SMTPException as e:
            print(f"✗ SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            return False


class SMSService:
    """Handles SMS sending via Twilio (Optional)"""
    
    def __init__(self):
        self.account_sid = config.TWILIO_ACCOUNT_SID
        self.auth_token = config.TWILIO_AUTH_TOKEN
        self.phone_number = config.TWILIO_PHONE_NUMBER
        self.available = bool(self.account_sid and self.auth_token)
    
    def send_otp_sms(self, recipient_phone, otp_code):
        """Send OTP via SMS using Twilio"""
        if not self.available:
            print("⚠ SMS service not configured. Set Twilio credentials in .env file.")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            message_body = f"Your HostelHub password reset OTP is: {otp_code}\nValid for {config.OTP_EXPIRY_MINUTES} minutes. Do not share with anyone."
            
            message = client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=recipient_phone
            )
            
            print(f"✓ SMS sent successfully to {recipient_phone}. Message SID: {message.sid}")
            return True
            
        except ImportError:
            print("⚠ Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"✗ Error sending SMS: {e}")
            return False


# Convenience functions
def generate_otp(length=None):
    """Generate OTP"""
    return OTPManager.generate_otp(length)

def get_otp_expiry():
    """Get OTP expiry time"""
    return OTPManager.get_otp_expiry()

def send_otp_email(email, name, otp):
    """Send OTP email"""
    service = EmailService()
    return service.send_otp_email(email, name, otp)

def send_password_reset_confirmation(email, name):
    """Send password reset confirmation"""
    service = EmailService()
    return service.send_password_reset_confirmation(email, name)

def send_otp_sms(phone, otp):
    """Send OTP SMS"""
    service = SMSService()
    return service.send_otp_sms(phone, otp)
