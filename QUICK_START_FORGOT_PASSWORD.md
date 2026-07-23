# ⚡ Quick Start - Forgot Password Feature

## What's Already Done ✅

The forgot password feature is **100% implemented** with:
- ✅ OTP generation and validation
- ✅ Email sending via Gmail SMTP
- ✅ 4 complete routes (forgot-password, verify-otp, resend-otp, reset-password)
- ✅ Beautiful UI with password strength indicator
- ✅ Database tables for OTP and token management
- ✅ Session-based security

## 3-Step Quick Setup

### Step 1: Enable Gmail App Password (2 minutes)
```
1. Go to https://myaccount.google.com/apppasswords
2. Generate a password for "Mail" + "Windows Computer"
3. Copy the 16-character password
```

### Step 2: Update .env (1 minute)
```bash
nano .env
```
Find and update these lines:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-password
```
Save: Ctrl+X → Y → Enter

### Step 3: Start MySQL & Run App (1 minute)
```bash
sudo service mysql start
cd /home/prajwal/Desktop/Hostel-Hub
python app.py
```

## Test It (30 seconds)

1. Go to http://localhost:5000/login
2. Click "Forgot Password?"
3. Enter: `prajwal` and select "Email"
4. Check your email for 6-digit OTP
5. Paste OTP and verify
6. Set new password
7. Login with new password ✅

## Done!

That's it. The feature is live and ready to use.

---

## Troubleshooting Quick Links

| Problem | Fix |
|---------|-----|
| "Failed to send email" | Update .env with correct Gmail + app password |
| "Can't connect to MySQL" | Run: `sudo service mysql start` |
| "OTP has expired" | Click "Resend OTP" to get a new one |
| "No email received" | Check spam folder or check .env credentials |

---

## Need More Details?

Read the full setup guide: `FORGOT_PASSWORD_SETUP_GUIDE.md`

Or run the test script to verify everything:
```bash
python test_forgot_password.py
```
