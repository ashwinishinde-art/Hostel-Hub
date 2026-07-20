# Forgot Password Feature - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Option 1: Test with Email OTP (Recommended)

#### Prerequisites:
- Gmail account
- Gmail app password generated

#### Step 1: Generate Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/security)
2. Enable 2-Step Verification (if not already enabled)
3. Go to "App Passwords"
4. Select "Mail" and "Windows Computer"
5. Copy the 16-character password

#### Step 2: Update .env file

```bash
nano .env
```

Update these lines:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

#### Step 3: Database Setup

Make sure OTP tables exist. If starting fresh:

```bash
mysql -u root < config/database.sql
```

#### Step 4: Start Application

```bash
python3 app.py
```

#### Step 5: Test the Flow

1. Open: http://localhost:5000/login
2. Click "Forgot Password?"
3. Enter: `admin`
4. Select: Email
5. Click: "Send OTP"
6. Check Gmail for OTP email
7. Copy OTP (6 digits)
8. Paste OTP in verification page
9. Set new password
10. Login with new password

---

### Option 2: Test Without Email (Mock Mode)

If Gmail isn't configured, OTP will still be generated but won't be sent.

#### Check Console Output

When you submit the forgot password form:
- The OTP will appear in the Flask console output
- Look for: `[OTP] Generated OTP: 123456`
- Use this OTP on the verification page

#### Steps:

1. Open: http://localhost:5000/login
2. Click "Forgot Password?"
3. Enter: `admin` or `prajwal`
4. Select: Email or SMS
5. Click: "Send OTP"
6. **Check console for OTP code**
7. Enter OTP in verification form
8. Set new password
9. Login!

---

## 🧪 Testing Guide

### Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Student | `prajwal` | `admin123` |
| Student | `rajdeep` | `admin123` |
| Warden | `warden` | `admin123` |

### Test Scenarios

#### ✅ Happy Path
1. Click Forgot Password
2. Enter `admin`
3. Select Email
4. Enter received OTP
5. Set new password
6. Login successfully

#### ❌ Error Cases to Test

**Invalid Username:**
- Enter: `invaliduser`
- Expected: "No account found with this username or email"

**Wrong OTP:**
- Enter: `000000`
- Expected: "Invalid OTP. Please try again."

**Expired OTP:**
- Wait 11 minutes (OTP expires in 10)
- Expected: "OTP has expired"

**Password Mismatch:**
- Password: `MyNewPass123!`
- Confirm: `MyNewPass124!`
- Expected: "Passwords do not match"

**Weak Password:**
- Password: `short`
- Expected: "Password must be at least 8 characters long"

---

## 📱 Resend OTP Test

1. On OTP verification page, click "Didn't receive the OTP?"
2. Click "Resend OTP"
3. New OTP should arrive
4. Previous OTP becomes invalid

---

## 🔧 Troubleshooting Quick Fixes

### Email Not Sending
```bash
# Check if Gmail credentials are correct
python3
>>> from utils.otp_manager import EmailService
>>> svc = EmailService()
>>> svc.send_otp_email('test@gmail.com', 'Test', '123456')
```

### OTP Not Appearing in Console
1. Make sure Flask debug mode is on
2. Check console wasn't scrolled up
3. Look for "[OTP]" prefix in logs

### Database Error
```bash
# Reinitialize database
mysql -u root < config/database.sql
```

### Can't Login After Password Reset
- Make sure you entered the correct new password
- Try password reset again
- Check .env file for database configuration

---

## 📊 What Gets Created

When user resets password:

**`password_reset_otp` table:**
- OTP code (6 digits)
- User ID
- Email/Phone
- Delivery method
- Expiry time
- Verification status

**`password_reset_tokens` table:**
- Reset token (secure)
- User ID
- OTP reference
- Reset time

**Emails sent:**
- OTP email with 6-digit code
- Confirmation email when password reset

---

## 🎯 Next Steps

### For Production:

1. **Configure Twilio** (optional SMS support)
   - Get Account SID, Auth Token
   - Add to .env
   - Purchase phone number

2. **Add Rate Limiting**
   - Prevent brute force OTP attempts
   - Limit resend requests

3. **Enable HTTPS**
   - Use SSL certificates
   - Secure all communications

4. **Add Logging**
   - Log password reset attempts
   - Monitor suspicious patterns

5. **Implement CAPTCHA**
   - Add to forgot password form
   - Prevent automated attacks

---

## 📞 Support

### If Something Doesn't Work:

1. **Check console output** for error messages
2. **Verify .env file** is correctly formatted
3. **Ensure MySQL is running**: `service mysql status`
4. **Check database tables exist**:
   ```bash
   mysql -u root -e "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='hostel_management'"
   ```
5. **Review FORGOT_PASSWORD_GUIDE.md** for detailed troubleshooting

---

## 📝 Test Checklist

- [ ] Can navigate to forgot password page
- [ ] Can select email/SMS method
- [ ] Can submit form with valid username
- [ ] OTP is generated and logged
- [ ] Can verify OTP successfully
- [ ] Can set new password with strength indicator
- [ ] Can resend OTP
- [ ] Can login with new password
- [ ] Confirmation email is received (if configured)
- [ ] Error messages display correctly

---

**Ready to test? Start with:**
```bash
cd /home/prajwal/Programs/Hostel
python3 app.py
```

Then go to: http://localhost:5000/login and click "Forgot Password?"
