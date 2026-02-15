""" Main Flask Application """
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from config import config
from models import db, Campaign, Target, EmailLog, EmailTemp
from emailSender import PhishingEmailSender

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Tracking routes
    @app.route('/track/<token>')
    def track_email(token):
        """Track email opens via tracking pixel"""
        email_log = EmailLog.query.filter_by(trackingToken=token).first()
        if email_log and not email_log.openedAt:
            email_log.openedAt = datetime.utcnow()
            db.session.commit()
        
        # Return 1x1 transparent pixel
        response = make_response()
        response.data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Length'] = len(response.data)
        return response
    
    @app.route('/click/<token>')
    def track_click(token):
        """Track link clicks and show educational page"""
        email_log = EmailLog.query.filter_by(trackingToken=token).first()
        if email_log and not email_log.clickedAt:
            email_log.clickedAt = datetime.utcnow()
            db.session.commit()
        
        # Show educational landing page
        return render_template('education.html', 
                             campaign=email_log.campaign,
                             target=email_log.target)
    
    # Admin routes
    @app.route('/admin')
    def admin_dashboard():
        """Admin dashboard"""
        campaigns = Campaign.query.all()
        total_emails = EmailLog.query.count()
        total_clicks = EmailLog.query.filter(EmailLog.clickedAt.isnot(None)).count()
        click_rate = round((total_clicks / total_emails * 100) if total_emails > 0 else 0, 2)
        
        return render_template('admin/dashboard.html', 
                             campaigns=campaigns,
                             total_emails=total_emails,
                             total_clicks=total_clicks,
                             click_rate=click_rate)
    
    @app.route('/campaigns')
    def campaigns():
        """Manage campaigns"""
        campaigns = Campaign.query.all()
        return render_template('admin/campaigns.html', campaigns=campaigns)
    
    @app.route('/create_campaign', methods=['GET', 'POST'])
    def create_campaign():
        """Create new campaign"""
        if request.method == 'POST':
            campaign = Campaign(
                name=request.form['name'],
                subject=request.form['subject'],
                templateName=request.form['template_name'],
                landingPageURL=request.form['landing_url']
            )
            db.session.add(campaign)
            db.session.commit()
            flash('Campaign created successfully!', 'success')
            return redirect(url_for('campaigns'))
        
        templates = EmailTemp.query.all()
        return render_template('admin/create_campaign.html', templates=templates)
    
    @app.route('/targets')
    def targets():
        """Manage targets"""
        targets = Target.query.all()
        return render_template('admin/targets.html', targets=targets)
    
    @app.route('/add_targets', methods=['GET', 'POST'])
    def add_targets():
        """Add new targets"""
        if request.method == 'POST':
            emails = request.form['emails'].strip().split('\n')
            for email in emails:
                email = email.strip()
                if email and '@' in email:
                    target = Target(
                        email=email,
                        firstName=request.form.get('first_name', ''),
                        department=request.form.get('department', '')
                    )
                    db.session.add(target)
            db.session.commit()
            flash(f'Added {len(emails)} targets successfully!', 'success')
            return redirect(url_for('targets'))
        
        return render_template('admin/add_targets.html')
    
    @app.route('/send_campaign/<int:campaign_id>')
    def send_campaign(campaign_id):
        """Send campaign to all targets"""
        campaign = Campaign.query.get_or_404(campaign_id)
        targets = Target.query.filter_by(active=True).all()
        sender = PhishingEmailSender()
        
        sent_count = 0
        for target in targets:
            success, result = sender.send_phishing_email(campaign, target)
            if success:
                db.session.add(result)
                sent_count += 1
        
        db.session.commit()
        flash(f'Campaign sent to {sent_count} targets!', 'success')
        return redirect(url_for('campaigns'))
    
    @app.route('/reports')
    def reports():
        """View campaign reports"""
        campaigns = Campaign.query.all()
        return render_template('admin/reports.html', campaigns=campaigns)
    
    @app.route('/api/campaign_stats/<int:campaign_id>')
    def campaign_stats(campaign_id):
        """API endpoint for campaign statistics"""
        campaign = Campaign.query.get_or_404(campaign_id)
        email_logs = EmailLog.query.filter_by(campaignId=campaign.id).all()
        
        total_sent = len(email_logs)
        total_opened = len([log for log in email_logs if log.openedAt])
        total_clicked = len([log for log in email_logs if log.clickedAt])
        
        return jsonify({
            'total_sent': total_sent,
            'total_opened': total_opened,
            'total_clicked': total_clicked,
            'open_rate': round((total_opened / total_sent * 100) if total_sent > 0 else 0, 2),
            'click_rate': round((total_clicked / total_sent * 100) if total_sent > 0 else 0, 2)
        })
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.run(debug=True)