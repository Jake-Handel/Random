# Phishing Awareness Simulation Tool

A comprehensive Python-based tool for conducting phishing awareness simulations to improve organizational security training.

## 🎯 Purpose

This tool helps organizations:
- Measure employee susceptibility to phishing attacks
- Provide immediate educational feedback
- Track security awareness improvement over time
- Conduct ethical phishing simulations for training purposes

## 🚀 Features

### Core Functionality
- **Email Campaign Management**: Create and manage phishing simulation campaigns
- **Template System**: Pre-built realistic phishing email templates
- **Target Management**: Add and organize employee targets
- **Real-time Tracking**: Monitor email opens and link clicks
- **Educational Landing Pages**: Immediate training when users click
- **Admin Dashboard**: Comprehensive campaign analytics

### Security Features
- **Authentication**: Secure admin access controls
- **Rate Limiting**: Prevent abuse of the system
- **Input Validation**: Protection against injection attacks
- **Audit Logging**: Complete activity tracking
- **Ethical Safeguards**: Built-in compliance features

### Analytics & Reporting
- **Campaign Statistics**: Open rates, click rates, and trends
- **Performance Metrics**: Track awareness improvement
- **Compliance Reports**: Generate audit documentation
- **Real-time Dashboard**: Live campaign monitoring

## 📋 Requirements

### System Requirements
- Python 3.7+
- SMTP email server (Gmail recommended)
- Modern web browser
- 2GB+ RAM
- 100MB+ disk space

### Python Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Mail==0.9.1
SQLAlchemy==2.0.21
Jinja2==3.1.2
Werkzeug==2.3.7
email-validator==2.0.0
python-dotenv==1.0.0
```

## 🛠️ Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd phishingTool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Initialize Database
```bash
python seed_templates.py
```

### 5. Run Application
```bash
python app.py
```

## ⚙️ Configuration

### Environment Variables (.env)

#### Flask Configuration
```env
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_CONFIG=development
DATABASE_URL=sqlite:///phishing_tool.db
```

#### Email Configuration (Gmail)
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

#### Application Settings
```env
BASE_URL=http://localhost:5000
ADMIN_EMAIL=admin@yourcompany.com
EDUCATION_MODE=true
REQUIRE_ADMIN_APPROVAL=false
```

### Gmail Setup
1. Enable 2-factor authentication
2. Generate an App Password
3. Use App Password in `MAIL_PASSWORD`

## 📖 Usage Guide

### 1. Access the Application
- Open browser to `http://localhost:5000`
- Navigate to `/admin` for dashboard

### 2. Add Targets
- Go to "Targets" → "Add Targets"
- Enter email addresses (one per line)
- Set default first name and department

### 3. Create Campaign
- Go to "Campaigns" → "Create Campaign"
- Enter campaign name and subject
- Select email template
- Set landing page URL

### 4. Send Campaign
- View campaigns list
- Click "Send" next to desired campaign
- Confirm sending to all targets

### 5. Monitor Results
- View real-time statistics on dashboard
- Check detailed reports
- Track individual user responses

## 🔒 Security Considerations

### Ethical Guidelines
- **Authorization**: Only test employees with proper consent
- **Education First**: Always provide immediate educational feedback
- **Privacy**: Protect employee data and results
- **Frequency**: Limit campaigns to avoid harassment
- **Transparency**: Be clear about training purposes

### Technical Security
- **Authentication**: Protect admin interfaces
- **Data Encryption**: Secure sensitive information
- **Access Controls**: Limit who can create campaigns
- **Audit Trails**: Log all activities
- **Input Validation**: Prevent injection attacks

## 📊 Templates Included

### Security Alert Template
- **Difficulty**: Medium
- **Scenario**: Account security breach notification
- **Psychology**: Urgency and fear tactics

### Package Delivery Template
- **Difficulty**: Easy
- **Scenario**: Failed package delivery
- **Psychology**: Curiosity and convenience

### IT Maintenance Template
- **Difficulty**: Medium
- **Scenario**: System update required
- **Psychology**: Authority and compliance

## 📈 Analytics

### Key Metrics
- **Open Rate**: Percentage of emails opened
- **Click Rate**: Percentage of links clicked
- **Conversion Rate**: Overall engagement
- **Time to Click**: Average response time
- **Department Performance**: Comparison by department

### Reporting Features
- **Campaign Overview**: Summary statistics
- **Individual Tracking**: Per-user results
- **Trend Analysis**: Improvement over time
- **Compliance Reports**: Audit documentation

## 🛡️ Compliance

### GDPR Considerations
- **Data Minimization**: Only collect necessary data
- **Purpose Limitation**: Use data only for training
- **Transparency**: Inform users about data usage
- **Retention Limits**: Don't keep data longer than needed
- **Security**: Implement appropriate technical measures

### Best Practices
- **Written Consent**: Document employee agreement
- **Opt-out Options**: Allow employees to decline participation
- **Clear Communication**: Explain training purposes
- **Regular Reviews**: Assess program effectiveness
- **Legal Review**: Consult with legal counsel

## 🔧 Troubleshooting

### Common Issues

#### Email Not Sending
- Check SMTP credentials
- Verify App Password (not regular password)
- Confirm firewall settings
- Check email quota limits

#### Database Errors
- Ensure write permissions
- Check disk space
- Verify SQLite installation

#### Tracking Not Working
- Confirm BASE_URL configuration
- Check firewall blocking
- Verify DNS resolution

### Error Messages
- **"Template not found"**: Run `seed_templates.py`
- **"Authentication failed"**: Check email credentials
- **"Database locked"**: Restart application

## 📞 Support

### Getting Help
1. Check this documentation
2. Review error logs
3. Test configuration
4. Contact IT support

### Contributing
- Report bugs via GitHub issues
- Submit pull requests for improvements
- Follow coding standards
- Include tests with new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Core phishing simulation functionality
- Admin dashboard
- Email template system
- Basic analytics

### Planned Features
- Advanced reporting
- Multi-language support
- API integration
- Mobile app
- Machine learning templates

---

**⚠️ Important**: This tool is for educational and training purposes only. Always obtain proper authorization before conducting phishing simulations.
