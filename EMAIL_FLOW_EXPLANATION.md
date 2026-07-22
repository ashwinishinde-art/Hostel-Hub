# Email Flow - How OTP is Sent to Registered Email

## Complete Email Sending Process

### When User Requests Forgot Password:

```
User enters username/email → Click "Send OTP"
                           ↓
         /forgot-password route processes request
                           ↓
         Query database for user by username or email
                           ↓
         User found? Yes ↓ User found? No → Error: "No account found"
                        ↓
         User has email on file? (otp_method=email)
                        ↓
                 Generate random 6-digit OTP
                        ↓
              Save to password_reset_otp table
                 (with 10-min expiry)
                        ↓
        ┌─────────────────────────────────────┐
        │  SEND EMAIL VIA GMAIL SMTP          │
        ├─────────────────────────────────────┤
        │ from: noreply@hostelhub.com         │
        │ to: user@example.com                │
        │ subject: Hostel Management -        │
        │          Password Reset OTP         │
        │ content: HTML + Text version        │
        │ otp: 123456 (example)               │
        │ valid: 10 minutes                   │
        └─────────────────────────────────────┘
                        ↓
         Email delivered to user's inbox
                        ↓
         User redirected to /verify-otp page
                        ↓
         User enters OTP from email
                        ↓
     OTP validated against database record
                        ↓
   If valid → Password reset form shown
   If invalid → Error message, user can retry
```

---

## Email Service Architecture

### EmailService Class (utils/otp_manager.py)

```python
class EmailService:
    def send_otp_email(recipient_email, full_name, otp_code):
        """
        Sends OTP email to user
        
        Parameters:
            recipient_email: user's email (from database)
            full_name: user's full name (from database)
            otp_code: 6-digit OTP (generated randomly)
        
        Returns:
            True if email sent successfully
            False if error occurred
        """
```

### SMTP Configuration (from .env)

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com          ← Your Gmail
MAIL_PASSWORD=your-16-char-app-password     ← Gmail App Password
MAIL_DEFAULT_SENDER=noreply@hostelhub.com   ← Sender name
```

### What Happens Inside send_otp_email():

1. **Create email message:**
   - Subject: "Hostel Management - Password Reset OTP"
   - From: noreply@hostelhub.com
   - To: recipient's email

2. **Generate email body (HTML):**
   ```html
   - Welcome message
   - Your OTP code (large, centered)
   - Expiry time (10 minutes)
   - Security warning
   - Footer with contact info
   ```

3. **Generate email body (Text):**
   - Plain text version for clients that don't support HTML
   - Same content, no formatting

4. **Connect to Gmail SMTP:**
   - Server: smtp.gmail.com (port 587)
   - TLS encryption enabled
   - Login with your Gmail credentials

5. **Send message:**
   - Use SMTP to transmit email
   - Return success/failure status

---

## Email Example

### What User Receives:

```
From: noreply@hostelhub.com
To: prajwal@student.com
Subject: Hostel Management - Password Reset OTP

╔════════════════════════════════════════╗
║           HostelHub                    ║
║  Hostel Management System              ║
╚════════════════════════════════════════╝

Hello Prajwal Tandekar,

We received a request to reset your password. If you did not make 
this request, please ignore this email.

Your One-Time Password (OTP) is:

        123456

⏰ This OTP will expire in 10 minutes

⚠️ Security Tip: Never share this OTP with anyone. HostelHub 
support will never ask for your OTP.

If you need further assistance, please contact our support team.

---
HostelHub Support Team
hostelhub@work.com | 7030710886
© 2024 HostelHub. All rights reserved.
```

---

## Step-by-Step Email Flow

### Step 1: User Action
```
User goes to /login
User clicks "Forgot Password?" link
→ Redirected to /forgot-password page (GET)
```

### Step 2: Form Submission
```
User enters: prajwal (username) or prajwal@student.com (email)
User selects: Email (vs SMS)
User clicks: "Send OTP" button
→ POST request to /forgot-password
```

### Step 3: Backend Processing (app.py)
```python
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    # 1. Get form data
    username_email = "prajwal"
    otp_method = "email"
    
    # 2. Query database
    SELECT id, username, email, full_name FROM users 
    WHERE username = "prajwal" AND is_active = TRUE
    # Result: prajwal@student.com
    
    # 3. Generate OTP
    otp_code = generate_otp()  # Returns: "123456"
    
    # 4. Calculate expiry
    otp_expiry = get_otp_expiry()  # Returns: 2026-07-22 14:47:19
    
    # 5. Save to database
    INSERT INTO password_reset_otp 
    (user_id, email, otp_code, otp_method, expires_at)
    VALUES (3, 'prajwal@student.com', '123456', 'email', expiry_time)
    
    # 6. Send email
    send_otp_email('prajwal@student.com', 'Prajwal Tandekar', '123456')
    
    # 7. Store session data
    session['otp_user_id'] = 3
    session['otp_method'] = 'email'
    
    # 8. Redirect to verification page
    return redirect('/verify-otp')
```

### Step 4: Email Transmission
```python
def _send_email(recipient_email, subject, html_body, text_body):
    # 1. Create MIMEMultipart message
    message = MIMEMultipart('alternative')
    message['Subject'] = "Hostel Management - Password Reset OTP"
    message['From'] = "noreply@hostelhub.com"
    message['To'] = "prajwal@student.com"
    
    # 2. Attach text and HTML versions
    message.attach(MIMEText(text_body, 'plain'))
    message.attach(MIMEText(html_body, 'html'))
    
    # 3. Connect to Gmail SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # TLS encryption
        server.login('your-email@gmail.com', 'app-password')
        server.send_message(message)
    
    # 4. Return success status
    return True
```

### Step 5: Email Delivery
```
Gmail receives email from your app
↓
Gmail checks credentials (MUST match .env)
↓
Gmail sends to recipient (prajwal@student.com)
↓
Email arrives in user's inbox (usually within seconds)
```

### Step 6: User Receives Email
```
User checks email inbox
User sees email from: noreply@hostelhub.com
User copies OTP: 123456
User goes to /verify-otp page
User enters: 123456
User clicks: "Verify OTP"
```

### Step 7: Verification
```python
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    # 1. Get form data
    otp_code = "123456"
    user_id = 3
    
    # 2. Query database for stored OTP
    SELECT * FROM password_reset_otp 
    WHERE user_id = 3 
    AND is_used = FALSE
    ORDER BY created_at DESC LIMIT 1
    
    # 3. Validate OTP
    if otp_record['otp_code'] == "123456":  # ✓ Match
        if datetime.now() < otp_record['expires_at']:  # ✓ Not expired
            # Mark as verified
            UPDATE password_reset_otp SET is_verified = TRUE
            
            # Create reset token
            INSERT INTO password_reset_tokens (user_id, token, otp_id, expires_at)
            
            # Redirect to reset password form
            return redirect('/reset-password')
```

### Step 8: Password Reset
```python
@app.route('/reset-password', methods=['POST'])
def reset_password():
    # 1. Get new password
    new_password = "NewSecure123!"
    
    # 2. Validate
    if len(new_password) < 8:  # Error!
    
    # 3. Hash password
    password_hash = bcrypt.hashpw(new_password.encode(), salt)
    
    # 4. Update database
    UPDATE users SET password_hash = hash WHERE id = 3
    
    # 5. Mark token as used
    UPDATE password_reset_tokens SET is_used = TRUE
    
    # 6. Send confirmation email
    send_password_reset_confirmation('prajwal@student.com', 'Prajwal Tandekar')
    
    # 7. Redirect to login
    flash('Password reset successfully!')
    return redirect('/login')
```

### Step 9: Confirmation Email Sent
```
User receives second email confirming password changed
From: noreply@hostelhub.com
Message: "Your password has been successfully changed! 
         You can now log in with your new password."
```

### Step 10: User Logs In
```
User goes to /login
User enters:
  - Username: prajwal
  - Password: NewSecure123! (the new password)
User clicks: "Log In"
→ Login successful! User is now logged in.
```

---

## Database Records Created

### 1. password_reset_otp table entry:

```sql
id: 1
user_id: 3
email: prajwal@student.com
phone: 9876543210
otp_code: 123456
otp_method: email
is_verified: 1 (becomes TRUE after verification)
is_used: 0 (becomes 1 after password reset)
created_at: 2026-07-22 14:37:19
expires_at: 2026-07-22 14:47:19
verified_at: 2026-07-22 14:38:30
```

### 2. password_reset_tokens table entry:

```sql
id: 1
user_id: 3
token: abc123def456ghi789jkl012mno345pqr678stu901vwx
otp_id: 1
is_used: 1 (becomes TRUE after password reset)
created_at: 2026-07-22 14:38:30
expires_at: 2026-07-22 14:08:30 (30 minutes)
reset_at: 2026-07-22 14:39:15
```

---

## Error Handling

### What if email send fails?

```python
try:
    server.login(email, password)
    server.send_message(message)
except smtplib.SMTPAuthenticationError:
    # Credentials wrong
    print("Email authentication failed")
    flash("Failed to send email - check credentials", 'danger')
    
except smtplib.SMTPException as e:
    # SMTP error
    print(f"SMTP error: {e}")
    flash("SMTP error occurred", 'danger')
    
except Exception as e:
    # Generic error
    print(f"Error sending email: {e}")
    flash("Failed to send email", 'danger')
```

---

## Security Measures

### Email Security:
1. **TLS Encryption** - All emails sent over encrypted connection
2. **App Passwords** - Not using main Gmail password
3. **Masked Display** - Email only partially shown in UI
4. **SMTP Authentication** - Only authorized sender can send

### OTP Security:
1. **Random Generation** - 6-digit random numeric code
2. **Expiry** - OTP expires after 10 minutes
3. **One-Time Use** - OTP can only be used once
4. **Per-User** - Each user can only reset their own password
5. **Validation** - Server validates on all steps

---

## Testing Email Sending

### Manual Test:

```python
from utils.otp_manager import send_otp_email

result = send_otp_email(
    recipient_email='prajwal@student.com',
    full_name='Prajwal Tandekar',
    otp_code='123456'
)

if result:
    print("✓ Email sent successfully")
else:
    print("✗ Email failed - check credentials")
```

### Production Deployment:

For production, you may want to use:
- **SendGrid** - Professional email service
- **AWS SES** - Amazon email service
- **Mailgun** - Developer-friendly email API
- **Postmark** - Transactional email service

Just update MAIL_SERVER and credentials in .env.

---

## Summary

✅ **Email is sent automatically when user requests OTP**

The complete flow:
1. User requests forgot password
2. App generates 6-digit OTP
3. App saves OTP to database with 10-min expiry
4. App sends OTP via Gmail SMTP to user's registered email
5. User receives email within seconds
6. User enters OTP to verify identity
7. App allows password reset
8. User sets new password
9. Confirmation email sent

**No manual intervention needed** - Email sending is fully automated! 🚀
