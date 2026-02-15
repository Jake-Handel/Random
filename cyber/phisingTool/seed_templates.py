""" Template seeder for phishing email templates """
from models import db, EmailTemp
from datetime import datetime
from app import create_app

def seed_templates():
    """Seed the database with default phishing email templates"""
    
    # Create app context
    app = create_app()
    with app.app_context():
        templates = [
            {
                'name': 'security_alert',
                'subject': '🚨 URGENT: Account Security Alert - Immediate Action Required',
                'htmlContent': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Urgent: Account Security Alert</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #dc3545; color: white; padding: 20px; text-align: center; }
        .content { background: #f8f9fa; padding: 30px; border: 1px solid #ddd; }
        .btn { display: inline-block; padding: 12px 24px; background: #dc3545; color: white; text-decoration: none; border-radius: 4px; }
        .footer { background: #6c757d; color: white; padding: 15px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 SECURITY ALERT</h1>
        </div>
        <div class="content">
            <h2>Immediate Action Required</h2>
            <p>Dear {{firstName}},</p>
            <p>We detected unusual activity on your account. For your protection, we have temporarily suspended access.</p>
            <p><strong>Reason:</strong> Suspicious login attempt from unrecognized device</p>
            <p><strong>Location:</strong> Unknown IP Address</p>
            <p><strong>Time:</strong> {{timestamp}}</p>
            <p>To secure your account, please verify your identity immediately:</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{{LINK}}" class="btn">SECURE ACCOUNT NOW</a>
            </p>
            <p><strong>Warning:</strong> If you don't verify within 24 hours, your account will be permanently suspended.</p>
            <hr>
            <p><small>If you did not attempt to log in, please ignore this email and contact support immediately.</small></p>
        </div>
        <div class="footer">
            <p>This is an automated security message. Please do not reply to this email.</p>
            <p> 2024 Security Department. All rights reserved.</p>
        </div>
    </div>
</body>
</html>''',
                'difficulty': 'medium'
            },
            {
                'name': 'package_delivery',
                'subject': ' Package Delivery - Action Required',
                'htmlContent': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Package Delivery Notification</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #28a745; color: white; padding: 20px; text-align: center; }
        .content { background: #f8f9fa; padding: 30px; border: 1px solid #ddd; }
        .package-info { background: white; padding: 15px; border: 1px solid #ddd; margin: 15px 0; }
        .btn { display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 4px; }
        .footer { background: #6c757d; color: white; padding: 15px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Package Delivery</h1>
        </div>
        <div class="content">
            <h2>Delivery Attempt Failed</h2>
            <p>Hello {{firstName}},</p>
            <p>We attempted to deliver your package but couldn't complete the delivery due to an incorrect address.</p>
            
            <div class="package-info">
                <h3>Package Details:</h3>
                <p><strong>Tracking Number:</strong> #{{trackingNumber}}</p>
                <p><strong>Carrier:</strong> Express Delivery Services</p>
                <p><strong>Delivery Date:</strong> {{deliveryDate}}</p>
                <p><strong>Reason:</strong> Address verification required</p>
            </div>
            
            <p>To update your delivery information and reschedule delivery:</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{{LINK}}" class="btn">UPDATE DELIVERY INFO</a>
            </p>
            
            <p><strong>Important:</strong> Your package will be returned to sender in 48 hours if action is not taken.</p>
            <hr>
            <p><small>This is an automated delivery notification. Please do not reply to this email.</small></p>
        </div>
        <div class="footer">
            <p>Express Delivery Services - Customer Service</p>
            <p> 2024 All rights reserved.</p>
        </div>
    </div>
</body>
</html>''',
                'difficulty': 'easy'
            },
            {
                'name': 'it_maintenance',
                'subject': ' IT Department - System Maintenance Required',
                'htmlContent': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IT System Maintenance</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; text-align: center; }
        .content { background: #f8f9fa; padding: 30px; border: 1px solid #ddd; }
        .maintenance-info { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 15px 0; }
        .btn { display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; }
        .footer { background: #6c757d; color: white; padding: 15px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> IT Department</h1>
        </div>
        <div class="content">
            <h2>System Maintenance Required</h2>
            <p>Dear {{firstName}},</p>
            <p>As part of our regular security maintenance, all employees are required to update their system credentials.</p>
            
            <div class="maintenance-info">
                <h3>Maintenance Details:</h3>
                <p><strong>Type:</strong> Security Update</p>
                <p><strong>Deadline:</strong> {{deadline}}</p>
                <p><strong>Impact:</strong> Account access will be restricted if not completed</p>
                <p><strong>Duration:</strong> Approximately 5 minutes</p>
            </div>
            
            <p>This update is mandatory for all {{department}} department employees to ensure continued system access.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{{LINK}}" class="btn">START SYSTEM UPDATE</a>
            </p>
            
            <p><strong>Note:</strong> Please save all work before beginning the update process.</p>
            <hr>
            <p><small>If you experience any issues, please contact the IT Help Desk at extension 1234.</small></p>
        </div>
        <div class="footer">
            <p>IT Department - Corporate Systems</p>
            <p> 2024 {{companyName}}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>''',
                'difficulty': 'medium'
            }
        ]
        
        # Clear existing templates
        EmailTemp.query.delete()
        
        # Add new templates
        for template_data in templates:
            template = EmailTemp(**template_data)
            db.session.add(template)
        
        db.session.commit()
        print(f"Successfully seeded {len(templates)} email templates")

if __name__ == '__main__':
    seed_templates()
