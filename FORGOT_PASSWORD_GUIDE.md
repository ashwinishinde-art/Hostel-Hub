# Forgot Password Feature - Complete Guide

## Overview

The Hostel Management System now includes a secure forgot password feature with OTP verification via email and SMS. This allows students to reset their passwords safely without requiring administrator intervention.

## Features

✅ **Email & SMS OTP Delivery** - Users can choose their preferred method to receive OTP  
✅ **Secure OTP Generation** - 6-digit random OTP with expiry validation  
✅ **Password Strength Validation** - Real-time strength indicator and requirements  
✅ **Confirmation Emails** - Users receive confirmation when password is reset  
✅ **Resend OTP** - Users can request a new OTP if needed  
✅ **Token-based Reset** - Secure token generation for password reset  
✅ **Session Management** - Secure session handling throughout the process  

## Setup & Configuration

### 1. Gmail SMTP Configuration (Email OTP)

To send OTP via email using Gmail:

**Step 1: Create a Google App Password**

1. Go to [Google Account](https://myaccount.google.com/)
2. Click "Security" in the left menu
3. Enable "2-Step Verification" (if not already enabled)
4. Click "App Passwords" (appears after 2FA is enabled)
5. Select "Mail" and "Windows Computer"
6. Google will generate a 16-character password
7. Copy this password

**Step 2: Update .env file**

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=noreply@hostelhub.com
```

**Example .env:**
```env
MAIL_USERNAME=hostel.system@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=HostelHub <noreply@hostelhub.com>
```

### 2. Twilio SMS Configuration (Optional)

To send OTP via SMS:

**Step 1: Create Twilio Account**

1. Sign up at [Twilio](https://www.twilio.com/try-twilio)
2. Verify your phone number
3. Go to Console Dashboard
4. Copy your Account SID and Auth Token
5. Purchase a phone number

**Step 2: Update .env file**

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

**Step 3: Install Twilio library**

```bash
pip install twilio
```

### 3. OTP Settings

Configure OTP behavior in .env:

```env
OTP_EXPIRY_MINUTES=10      # OTP validity duration
OTP_LENGTH=6               # Number of digits in OTP
```

## User Flow

### 1. Forgot Password Request
```
User clicks "Forgot Password?" link on login page
    ↓
Enters username or email
    ↓
Selects delivery method (Email or SMS)
    ↓
Submits form
```

### 2. OTP Verification
```
System generates OTP
    ↓
Sends OTP via selected method
    ↓
Displays OTP verification page
    ↓
User enters OTP within time limit
    ↓
System verifies OTP
    ↓
If correct → Generate reset token → Proceed to password reset
If wrong → Show error → Allow retry or resend
```

### 3. Password Reset
```
User enters new password
    ↓
System validates password strength
    ↓
Confirms password match
    ↓
Updates password in database
    ↓
Sends confirmation email
    ↓
Redirects to login page
```

## API Routes

### `/forgot-password` (GET/POST)
- **GET**: Display forgot password form
- **POST**: Process forgot password request
  - Parameters: `username_email`, `otp_method` (email/sms)
  - Validates user exists
  - Generates OTP
  - Sends OTP
  - Redirects to `/verify-otp`

### `/verify-otp` (GET/POST)
- **GET**: Display OTP verification form
- **POST**: Verify OTP code
  - Parameters: `otp_code`, `user_id`, `otp_method`
  - Validates OTP
  - Checks expiry
  - Generates reset token
  - Redirects to `/reset-password`

### `/resend-otp` (POST)
- Resend OTP to user
- Parameters: `user_id`, `otp_method`
- Generates new OTP
- Sends via selected method

### `/reset-password` (GET/POST)
- **GET**: Display password reset form
- **POST**: Reset user password
  - Parameters: `new_password`, `confirm_password`, `token`
  - Validates password strength
  - Updates password
  - Sends confirmation email
  - Redirects to `/login`

## Database Schema

### `password_reset_otp` Table
```sql
- id (INT): Primary key
- user_id (INT): Reference to user
- email (VARCHAR): User's email
- phone (VARCHAR): User's phone
- otp_code (VARCHAR): Generated OTP
- otp_method (ENUM): 'email' or 'sms'
- is_verified (BOOLEAN): OTP verification status
- is_used (BOOLEAN): OTP usage status
- created_at (TIMESTAMP): Creation time
- expires_at (TIMESTAMP): Expiry time
- verified_at (DATETIME): Verification time
```

### `password_reset_tokens` Table
```sql
- id (INT): Primary key
- user_id (INT): Reference to user
- token (VARCHAR): Reset token
- otp_id (INT): Reference to OTP record
- is_used (BOOLEAN): Token usage status
- created_at (TIMESTAMP): Creation time
- expires_at (TIMESTAMP): Expiry time
- reset_at (DATETIME): Reset time
```

## Security Features

✅ **OTP Expiry** - OTP expires after configured time (default 10 minutes)  
✅ **One-time Use** - Each OTP can only be used once  
✅ **Token Validation** - Reset tokens are verified before password change  
✅ **Password Hashing** - New passwords are hashed with bcrypt  
✅ **Rate Limiting** - Consider implementing rate limiting in production  
✅ **Masked Display** - Email/phone partially masked in verification form  
✅ **Session Security** - Sensitive data stored in secure sessions  

## Testing the Feature

### Test Email OTP Flow

1. Start the application
   ```bash
   python3 app.py
   ```

2. Go to login page: `http://localhost:5000/login`

3. Click "Forgot Password?"

4. Enter username: `admin`

5. Select "Email" method

6. Submit form

7. Check console or email for OTP

8. Enter OTP on verification page

9. Set new password

10. Login with new password

### Test SMS OTP Flow (if Twilio configured)

1. Follow steps 1-4 above

2. Select "SMS" method

3. Submit form

4. Check phone for OTP message

5. Continue with steps 8-10

### Test Data

**Test Accounts:**
- Username: `admin` | Password: `admin123`
- Username: `prajwal` | Password: `admin123`
- Username: `rajdeep` | Password: `admin123`
- Username: `warden` | Password: `admin123`

## Email Templates

### OTP Email
- Professional HTML template
- Displays OTP prominently
- Shows expiry time
- Includes security warning
- Contains support contact info

### Password Reset Confirmation Email
- Confirms successful password change
- Includes security notice
- Provides login link
- Alert for unauthorized changes

## Error Handling

The system handles various error scenarios:

| Error | Handling |
|-------|----------|
| User not found | Friendly message without revealing existence |
| No phone/email | Suggests alternative method |
| OTP expired | User can request new OTP |
| Invalid OTP | Shows error, allows retry |
| SMS service unavailable | Falls back to email with warning |
| Database connection error | Displays error message |
| Email sending failed | Graceful error handling with support info |

## Troubleshooting

### Email OTP Not Sending

**Problem:** Emails not received after submitting forgot password form

**Solutions:**
1. Check .env file for correct Gmail credentials
2. Verify Gmail app password (not account password)
3. Ensure 2-Step Verification is enabled on Gmail account
4. Check Flask console for error messages
5. Verify MAIL_USERNAME has app password set correctly
6. Check spam/junk folder

**Debug:**
```bash
# In Python shell
from utils.otp_manager import EmailService
service = EmailService()
service.send_otp_email('test@example.com', 'Test User', '123456')
```

### OTP Verification Failing

**Problem:** Valid OTP shows as invalid

**Solutions:**
1. Check OTP hasn't expired (default 10 minutes)
2. Verify OTP matches exactly (case-sensitive for codes)
3. Check database connection
4. Ensure JavaScript input masking isn't interfering
5. Verify OTP is from latest request (not old one)

### SMS Not Sending

**Problem:** SMS OTP not received

**Solutions:**
1. Verify Twilio credentials in .env
2. Check phone number format (include country code)
3. Ensure Twilio account has sufficient credits
4. Verify phone number isn't on Twilio blocklist
5. Check Twilio logs for delivery status
6. Install Twilio library: `pip install twilio`

## Production Recommendations

Before deploying to production:

1. **Implement Rate Limiting**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   @limiter.limit("5 per minute")
   @app.route('/forgot-password', methods=['POST'])
   ```

2. **Add Security Headers**
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       return response
   ```

3. **Log All Password Reset Attempts**
   ```python
   # Log successful and failed attempts
   logger.info(f"Password reset attempt for user_id: {user_id}")
   ```

4. **Implement CAPTCHA**
   - Add Google reCAPTCHA to forgot password form
   - Prevents brute force attacks

5. **Email Verification**
   - Send confirmation before processing reset
   - Helps prevent account takeovers

6. **Use HTTPS Only**
   - Ensure all communication is encrypted
   - Set SECURE cookie flag in production

7. **Audit Logging**
   - Log all password changes
   - Track OTP generation and verification
   - Monitor suspicious patterns

## Support

For issues or questions:

1. Check Flask console output for error messages
2. Review database for OTP and token records
3. Verify .env configuration
4. Check email/SMS provider logs
5. Contact support with error details

## Files Modified/Created

### New Files:
- `templates/forgot_password.html` - Forgot password form
- `templates/verify_otp.html` - OTP verification form
- `templates/reset_password.html` - Password reset form
- `utils/otp_manager.py` - OTP and email utilities
- `config/migrations/001_add_otp_tables.sql` - Database schema

### Modified Files:
- `app.py` - Added forgot password routes
- `config/config.py` - Added email/SMS configuration
- `config/database.sql` - Added OTP tables
- `.env` - Added email/SMS credentials
- `templates/login.html` - Added "Forgot Password?" link

## Version Information

- **Feature Version:** 1.0.0
- **Database Schema Version:** 1
- **Date Added:** July 2024
- **Status:** Production Ready

---

**Last Updated:** July 2024  
**Maintained By:** Development Team
