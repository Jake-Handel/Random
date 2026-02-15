from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

""" Used to store the data """
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    templateName = db.Column(db.String(50), nullable=False)
    landingPageURL = db.Column(db.String(500), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    isActive = db.Column(db.Boolean, default=True)
    emailLogs = db.relationship('EmailLog', backref='campaign', lazy=True)
    
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    firstName = db.Column(db.String(50))
    department = db.Column(db.String(50))  
    active = db.Column(db.Boolean, default=True)
    emailLogs = db.relationship('EmailLog', backref='target', lazy=True)
    
class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaignId = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    targetId = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)
    sentAt = db.Column(db.DateTime, default=datetime.utcnow)
    openedAt = db.Column(db.DateTime)
    clickedAt = db.Column(db.DateTime)
    trackingToken = db.Column(db.String(100), unique=True, nullable=False)
    
    def __init__(self, **kwargs):
        super(EmailLog, self).__init__(**kwargs)
        if not self.trackingToken:
            self.trackingToken = secrets.token_urlsafe(16)

class EmailTemp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    htmlContent = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
