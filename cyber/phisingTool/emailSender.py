""" Used to send the emails """
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from datetime import datetime, timedelta
from models import Campaign, Target, EmailLog, EmailTemp
import secrets

class PhishingEmailSender:
    def __init__(self):
        self.smtp_server = current_app.config['MAIL_SERVER']
        self.smtp_port = current_app.config['MAIL_PORT']
        self.username = current_app.config['MAIL_USERNAME']
        self.password = current_app.config['MAIL_PASSWORD']
        self.use_tls = current_app.config['MAIL_USE_TLS']
    
    def send_phishing_email(self, campaign, target):
        """Send phishing email to target"""
        try:
            # Create email log entry
            email_log = EmailLog(
                campaignId=campaign.id,
                targetId=target.id
            )
            
            # Compose email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = campaign.subject
            msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER')
            msg['To'] = target.email
            
            # Add tracking pixel and links
            html_content = self._add_tracking(campaign, target, email_log)
            
            # Add HTML part to email
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            return True, email_log
            
        except Exception as e:
            return False, str(e)
    
    def _add_tracking(self, campaign, target, email_log):
        """Add tracking pixel and links to email"""
        tracking_url = f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/track/{email_log.trackingToken}"
        link_url = f"{current_app.config.get('BASE_URL', 'http://localhost:5000')}/click/{email_log.trackingToken}"
        
        # Get email template
        template = EmailTemp.query.filter_by(name=campaign.templateName).first()
        if not template:
            raise ValueError(f"Template '{campaign.templateName}' not found")
        
        # Replace template variables
        html_content = template.htmlContent
        html_content = html_content.replace('{{LINK}}', link_url)
        html_content = html_content.replace('{{firstName}}', target.firstName or 'User')
        html_content = html_content.replace('{{department}}', target.department or 'Unknown')
        html_content = html_content.replace('{{companyName}}', 'Your Company')
        html_content = html_content.replace('{{timestamp}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        html_content = html_content.replace('{{deliveryDate}}', datetime.now().strftime('%B %d, %Y'))
        html_content = html_content.replace('{{trackingNumber}}', f'TRK{email_log.id:08d}')
        html_content = html_content.replace('{{deadline}}', (datetime.now() + timedelta(days=2)).strftime('%B %d, %Y'))
        
        # Add tracking pixel (1x1 transparent image)
        tracking_pixel = f'<img src="{tracking_url}" width="1" height="1" style="display:none;">'
        html_content += tracking_pixel
        
        return html_content