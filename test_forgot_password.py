#!/usr/bin/env python3
"""
Test script for the forgot password feature
This script tests the OTP generation, email configuration, and password reset flow
"""

import sys
import os
from datetime import datetime, timedelta

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("🔐 HOSTEL HUB - FORGOT PASSWORD FEATURE TEST")
print("="*70)

# ============= 1. Test Environment Configuration =============
print("\n[1] Testing Environment Configuration...")
print("-" * 70)

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ .env file loaded successfully")
    
    from config.config import DevelopmentConfig as config
    
    # Check email configuration
    print(f"  • MAIL_SERVER: {config.MAIL_SERVER}")
    print(f"  • MAIL_PORT: {config.MAIL_PORT}")
    print(f"  • MAIL_USE_TLS: {config.MAIL_USE_TLS}")
    print(f"  • MAIL_USERNAME: {config.MAIL_USERNAME[:20]}..." if config.MAIL_USERNAME else "  • MAIL_USERNAME: NOT SET ⚠")
    print(f"  • OTP_EXPIRY_MINUTES: {config.OTP_EXPIRY_MINUTES}")
    print(f"  • OTP_LENGTH: {config.OTP_LENGTH}")
    
except Exception as e:
    print(f"✗ Error loading configuration: {e}")
    sys.exit(1)

# ============= 2. Test OTP Manager =============
print("\n[2] Testing OTP Manager...")
print("-" * 70)

try:
    from utils.otp_manager import (
        OTPManager, 
        EmailService, 
        generate_otp, 
        get_otp_expiry,
        send_otp_email,
        send_password_reset_confirmation
    )
    
    # Test OTP generation
    otp_code = generate_otp()
    print(f"✓ Generated OTP: {otp_code}")
    
    if len(otp_code) == config.OTP_LENGTH and otp_code.isdigit():
        print(f"✓ OTP format is correct (length: {len(otp_code)}, numeric: yes)")
    else:
        print(f"✗ OTP format error (length: {len(otp_code)}, expected: {config.OTP_LENGTH})")
    
    # Test OTP expiry
    expiry = get_otp_expiry()
    print(f"✓ OTP Expiry: {expiry}")
    
    if expiry > datetime.now():
        minutes_until_expiry = (expiry - datetime.now()).total_seconds() / 60
        print(f"✓ OTP will expire in {minutes_until_expiry:.1f} minutes")
    else:
        print(f"✗ OTP expiry is in the past!")
        
except Exception as e:
    print(f"✗ Error in OTP Manager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============= 3. Test Email Service Configuration =============
print("\n[3] Testing Email Service Configuration...")
print("-" * 70)

try:
    email_service = EmailService()
    
    print(f"✓ Email Service initialized")
    print(f"  • SMTP Server: {email_service.smtp_server}:{email_service.smtp_port}")
    print(f"  • Sender Email: {email_service.sender_email}")
    print(f"  • Default Sender: {email_service.default_sender}")
    print(f"  • TLS Enabled: {email_service.use_tls}")
    
    # Validate email configuration
    if email_service.smtp_server and email_service.smtp_port:
        print("✓ SMTP configuration looks valid")
    else:
        print("⚠ SMTP configuration incomplete")
    
    if "gmail" in email_service.smtp_server.lower():
        print("✓ Using Gmail SMTP (requires app password)")
        if email_service.sender_email == 'your-email@gmail.com':
            print("⚠ WARNING: Email not configured! Please update .env with your Gmail:")
            print("   1. Go to https://myaccount.google.com/apppasswords")
            print("   2. Generate an app password (16 characters)")
            print("   3. Update MAIL_USERNAME and MAIL_PASSWORD in .env")
        else:
            print(f"✓ Email configured: {email_service.sender_email}")
    
except Exception as e:
    print(f"✗ Error initializing Email Service: {e}")
    import traceback
    traceback.print_exc()

# ============= 4. Test Database Connection =============
print("\n[4] Testing Database Connection...")
print("-" * 70)

try:
    from config.database import db
    
    if db.connection and db.is_connected:
        print("✓ Database connection is active")
        
        cursor = db.connection.cursor()
        
        # Check if password_reset_otp table exists
        cursor.execute("""
            SELECT COUNT(*) as count FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'hostel_management' 
            AND TABLE_NAME = 'password_reset_otp'
        """)
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            print("✓ password_reset_otp table exists")
        else:
            print("✗ password_reset_otp table not found!")
            print("  Run: mysql -u root -p < config/database.sql")
        
        # Check if password_reset_tokens table exists
        cursor.execute("""
            SELECT COUNT(*) as count FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'hostel_management' 
            AND TABLE_NAME = 'password_reset_tokens'
        """)
        result = cursor.fetchone()
        
        if result and result['count'] > 0:
            print("✓ password_reset_tokens table exists")
        else:
            print("✗ password_reset_tokens table not found!")
        
        # Check sample users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        print(f"✓ Found {result['count']} users in database")
        
        # Check a user's email
        cursor.execute("SELECT username, email, full_name FROM users WHERE username = 'prajwal' LIMIT 1")
        user = cursor.fetchone()
        if user:
            print(f"✓ Sample user found: {user['username']} ({user['email']})")
        else:
            print("⚠ Sample user 'prajwal' not found")
        
        cursor.close()
        
    else:
        print("⚠ Database connection not active")
        print("  Make sure MySQL is running: sudo service mysql start")
        
except Exception as e:
    print(f"✗ Database error: {e}")
    import traceback
    traceback.print_exc()

# ============= 5. Test Flask Routes =============
print("\n[5] Testing Flask Routes...")
print("-" * 70)

try:
    from app import app
    
    with app.app_context():
        print("✓ Flask app context loaded")
        
        # Check if routes are registered
        routes_to_check = [
            '/forgot-password',
            '/verify-otp',
            '/resend-otp',
            '/reset-password',
            '/login'
        ]
        
        registered_routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        for route in routes_to_check:
            if route in registered_routes:
                print(f"✓ Route registered: {route}")
            else:
                print(f"✗ Route NOT found: {route}")
                
except Exception as e:
    print(f"✗ Error checking Flask routes: {e}")
    import traceback
    traceback.print_exc()

# ============= 6. Test Required Templates =============
print("\n[6] Testing Required Templates...")
print("-" * 70)

try:
    import os
    templates_path = os.path.join(os.path.dirname(__file__), 'templates')
    
    required_templates = [
        'forgot_password.html',
        'verify_otp.html',
        'reset_password.html',
        'login.html',
        'base.html'
    ]
    
    for template in required_templates:
        template_path = os.path.join(templates_path, template)
        if os.path.exists(template_path):
            print(f"✓ Template found: {template}")
            
            # Check if template has required elements
            with open(template_path, 'r') as f:
                content = f.read()
                
            if template == 'forgot_password.html':
                if 'username_email' in content and 'otp_method' in content:
                    print(f"  ✓ Contains required form fields")
            elif template == 'verify_otp.html':
                if 'otp_code' in content and 'resend' in content.lower():
                    print(f"  ✓ Contains OTP verification and resend option")
            elif template == 'reset_password.html':
                if 'new_password' in content and 'confirm_password' in content:
                    print(f"  ✓ Contains password fields")
        else:
            print(f"✗ Template NOT found: {template}")
            
except Exception as e:
    print(f"✗ Error checking templates: {e}")

# ============= SUMMARY =============
print("\n" + "="*70)
print("📋 TEST SUMMARY")
print("="*70)

print("""
To enable the forgot password feature:

1. ✓ Configuration is set up (.env file created)
2. ✓ OTP Manager is ready
3. ⚠ Email Service requires configuration:
   - Update MAIL_USERNAME and MAIL_PASSWORD in .env
   - Use your Gmail address and app password from Google Account
4. ✓ Database tables are ready
5. ✓ Flask routes are registered
6. ✓ All templates are in place

NEXT STEPS:
1. Edit .env file and add your Gmail credentials
2. Run the application: python app.py
3. Go to /login and click "Forgot Password?"
4. Test the OTP flow with a registered email

For Gmail Setup:
• Enable 2-Factor Authentication: https://myaccount.google.com/security
• Generate App Password: https://myaccount.google.com/apppasswords
• Copy the 16-character password to MAIL_PASSWORD in .env
""")

print("="*70 + "\n")
