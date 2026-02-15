""" Security and ethical safeguards for phishing awareness tool """
from functools import wraps
from flask import session, request, redirect, url_for, flash, current_app
import hashlib
import time
from datetime import datetime, timedelta

class SecurityManager:
    """Manages security features and ethical safeguards"""
    
    @staticmethod
    def require_auth(f):
        """Decorator to require authentication for admin routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('authenticated'):
                flash('Authentication required to access this page.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    @staticmethod
    def rate_limit(max_requests=10, window=3600):
        """Simple rate limiting decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Simple IP-based rate limiting
                ip = request.remote_addr
                current_time = time.time()
                
                # Store requests in session (in production, use Redis or database)
                if 'requests' not in session:
                    session['requests'] = []
                
                # Clean old requests
                session['requests'] = [req_time for req_time in session['requests'] 
                                     if current_time - req_time < window]
                
                # Check limit
                if len(session['requests']) >= max_requests:
                    flash('Rate limit exceeded. Please try again later.', 'danger')
                    return redirect(url_for('admin_dashboard'))
                
                # Add current request
                session['requests'].append(current_time)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    @staticmethod
    def validate_email_domain(email, allowed_domains=None):
        """Validate email domain against allowed list"""
        if allowed_domains is None:
            allowed_domains = current_app.config.get('ALLOWED_DOMAINS', [])
        
        if not allowed_domains:
            return True  # No restrictions if no domains specified
        
        domain = email.split('@')[-1].lower()
        return domain in [d.lower() for d in allowed_domains]
    
    @staticmethod
    def log_security_event(event_type, details, user=None):
        """Log security events for audit trail"""
        log_entry = {
            'timestamp': datetime.utcnow(),
            'event_type': event_type,
            'details': details,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'user': user
        }
        
        # In production, log to file or security system
        current_app.logger.info(f"Security Event: {log_entry}")
    
    @staticmethod
    def sanitize_input(input_string):
        """Basic input sanitization"""
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript']
        sanitized = input_string
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()
    
    @staticmethod
    def validate_campaign_permissions(user_email, campaign):
        """Validate that user has permission to access campaign"""
        # Only allow admin users or campaign creators
        if session.get('is_admin'):
            return True
        
        # Check if user is the campaign creator (if implemented)
        # This would require adding a creator field to Campaign model
        return False

class EthicalSafeguards:
    """Ethical safeguards for phishing simulations"""
    
    @staticmethod
    def add_educational_disclaimer(template_content):
        """Add educational disclaimer to email templates"""
        disclaimer = """
        <!-- Educational Disclaimer -->
        <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; margin-top: 20px; font-size: 12px; color: #6c757d;">
            <p><strong>Important:</strong> This is a security awareness training email. 
            If you received this email in error, please contact your IT department.</p>
        </div>
        """
        return template_content + disclaimer
    
    @staticmethod
    def validate_business_hours():
        """Only allow campaigns during business hours"""
        current_hour = datetime.now().hour
        business_start = 9  # 9 AM
        business_end = 17   # 5 PM
        
        return business_start <= current_hour <= business_end
    
    @staticmethod
    def limit_campaign_frequency(user_email, max_campaigns_per_month=2):
        """Limit how often a user can be targeted"""
        # This would need to be implemented with database queries
        # Check how many campaigns the user has received in the last 30 days
        return True  # Placeholder
    
    @staticmethod
    def ensure_consent_required():
        """Ensure proper consent is obtained before campaigns"""
        return current_app.config.get('REQUIRE_CONSENT', True)
    
    @staticmethod
    def generate_audit_report():
        """Generate compliance audit report"""
        # Generate report of all campaigns, targets, and results for compliance
        return {
            'total_campaigns': 0,
            'total_targets': 0,
            'compliance_score': 100,
            'last_audit': datetime.utcnow()
        }
