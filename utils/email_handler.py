"""
Email Handler Module
Contains functions for handling email notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from pathlib import Path
import jinja2

class TaxEmailHandler:
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        sender_email: str,
        template_dir: str = 'templates'
    ):
        """Initialize email handler with SMTP settings"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email
        self.logger = logging.getLogger(__name__)
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        is_html: bool = False
    ) -> bool:
        """Send email to recipient"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_welcome_email(self, recipient: str, name: str) -> bool:
        """Send welcome email to new user"""
        template = self.template_env.get_template('welcome.html')
        body = template.render(name=name)
        subject = "Welcome to TaxSage"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_password_reset_email(
        self,
        recipient: str,
        name: str,
        reset_link: str
    ) -> bool:
        """Send password reset email"""
        template = self.template_env.get_template('password_reset.html')
        body = template.render(name=name, reset_link=reset_link)
        subject = "Password Reset Request"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_verification_email(
        self,
        recipient: str,
        name: str,
        verification_link: str
    ) -> bool:
        """Send email verification link"""
        template = self.template_env.get_template('verify_email.html')
        body = template.render(name=name, verification_link=verification_link)
        subject = "Verify Your Email Address"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_tax_calculation_email(
        self,
        recipient: str,
        name: str,
        calculation_data: Dict[str, Any]
    ) -> bool:
        """Send tax calculation results email"""
        template = self.template_env.get_template('tax_calculation.html')
        body = template.render(name=name, data=calculation_data)
        subject = "Your Tax Calculation Results"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_deduction_reminder_email(
        self,
        recipient: str,
        name: str,
        deduction_data: Dict[str, Any]
    ) -> bool:
        """Send deduction reminder email"""
        template = self.template_env.get_template('deduction_reminder.html')
        body = template.render(name=name, data=deduction_data)
        subject = "Tax Deduction Reminder"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_payment_reminder_email(
        self,
        recipient: str,
        name: str,
        payment_data: Dict[str, Any]
    ) -> bool:
        """Send tax payment reminder email"""
        template = self.template_env.get_template('payment_reminder.html')
        body = template.render(name=name, data=payment_data)
        subject = "Tax Payment Reminder"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_document_reminder_email(
        self,
        recipient: str,
        name: str,
        document_data: Dict[str, Any]
    ) -> bool:
        """Send document submission reminder email"""
        template = self.template_env.get_template('document_reminder.html')
        body = template.render(name=name, data=document_data)
        subject = "Document Submission Reminder"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_newsletter_email(
        self,
        recipients: List[str],
        subject: str,
        content: str
    ) -> bool:
        """Send newsletter email to multiple recipients"""
        success = True
        for recipient in recipients:
            if not self.send_email(recipient, subject, content, is_html=True):
                success = False
        return success

    def send_error_notification_email(
        self,
        error_data: Dict[str, Any]
    ) -> bool:
        """Send error notification email to admin"""
        template = self.template_env.get_template('error_notification.html')
        body = template.render(data=error_data)
        subject = "TaxSage Error Notification"
        return self.send_email(
            self.sender_email,  # Send to admin
            subject,
            body,
            is_html=True
        )

    def send_system_update_email(
        self,
        recipients: List[str],
        update_data: Dict[str, Any]
    ) -> bool:
        """Send system update notification email"""
        template = self.template_env.get_template('system_update.html')
        body = template.render(data=update_data)
        subject = "TaxSage System Update"
        return self.send_newsletter_email(recipients, subject, body)

    def send_feedback_response_email(
        self,
        recipient: str,
        name: str,
        feedback_data: Dict[str, Any]
    ) -> bool:
        """Send feedback response email"""
        template = self.template_env.get_template('feedback_response.html')
        body = template.render(name=name, data=feedback_data)
        subject = "Thank You for Your Feedback"
        return self.send_email(recipient, subject, body, is_html=True)

    def send_custom_email(
        self,
        recipient: str,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any]
    ) -> bool:
        """Send custom email using specified template"""
        try:
            template = self.template_env.get_template(template_name)
            body = template.render(**template_data)
            return self.send_email(recipient, subject, body, is_html=True)
        except Exception as e:
            self.logger.error(f"Failed to send custom email: {str(e)}")
            return False 