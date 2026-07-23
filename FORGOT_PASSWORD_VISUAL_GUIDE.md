# 📱 Forgot Password Feature - Visual Guide

## User Experience Flow

### Screen 1: Login Page
```
┌──────────────────────────────────────────┐
│                                          │
│            HOSTEL HUB LOGIN              │
│         Hostel Management System         │
│                                          │
│  Username: [____________]                │
│                                          │
│  Password: [____________]  [👁️ toggle]   │
│                                          │
│            [🔐 LOGIN]                    │
│                                          │
│  Forgot Password? ← CLICK HERE          │
│                                          │
│  Don't have account? [Register]          │
│                                          │
└──────────────────────────────────────────┘
```

**User Action:** Click "Forgot Password?"

---

### Screen 2: Forgot Password Form
```
┌──────────────────────────────────────────┐
│                                          │
│          🔑 FORGOT PASSWORD?             │
│                                          │
│  Enter your username or email to         │
│  reset your password                     │
│                                          │
│  Username or Email:                      │
│  [prajwal_____________]                  │
│                                          │
│  How would you like to receive OTP?      │
│                                          │
│  ┌─────────────┬──────────────┐         │
│  │ ✉️  Email   │  💬  SMS      │         │
│  │   (selected)│   (grayed)    │         │
│  └─────────────┴──────────────┘         │
│                                          │
│         [✈️ SEND OTP]                    │
│                                          │
│  OR                                      │
│  Remember password? [Sign in]            │
│                                          │
└──────────────────────────────────────────┘
```

**User Action:** 
1. Enter: `prajwal`
2. Select: `Email`
3. Click: "Send OTP"

**System Action:**
- Generate OTP: `123456`
- Save to database with 10-min expiry
- Send email immediately
- Store session data

---

### Email Received (What User Sees)

```
From: noreply@hostelhub.com
To: prajwal@student.com
Subject: Hostel Management - Password Reset OTP

╔════════════════════════════════════════════╗
║         🏨 HostelHub                       ║
║  Hostel Management System                  ║
╚════════════════════════════════════════════╝

Hello Prajwal Tandekar,

We received a request to reset your password. If you 
did not make this request, please ignore this email.

Your One-Time Password (OTP) is:

    ┌─────────────────┐
    │    123456       │
    └─────────────────┘

⏰ This OTP will expire in 10 minutes

⚠️ Security Tip: Never share this OTP with anyone. 
   HostelHub support will never ask for your OTP.

If you need further assistance, contact our support team.

---
HostelHub Support Team
hostelhub@work.com | 7030710886
© 2024 HostelHub. All rights reserved.
```

**User Action:** Copy OTP `123456`

---

### Screen 3: OTP Verification Form
```
┌──────────────────────────────────────────┐
│                                          │
│           🛡️ VERIFY OTP                   │
│                                          │
│  Enter the OTP sent to your email        │
│                                          │
│  📧 Sent to: **wa**@st******.com         │
│              (masked for security)       │
│                                          │
│  Enter OTP Code:                         │
│  ┌──────────────────┐                   │
│  │  1  2  3  4  5 6 │ (auto-formatted)  │
│  └──────────────────┘                   │
│                                          │
│  ⏱️ OTP expires at: 14:47               │
│  (appears to be 10 minutes from now)     │
│                                          │
│       [✓ VERIFY OTP]                    │
│                                          │
│  Didn't receive the OTP?                │
│  [🔄 Resend OTP] ← Can click anytime    │
│                                          │
│  OR                                      │
│  [← Back to Login]                      │
│                                          │
│  ⚠️ Security Notice: Never share OTP     │
│     with anyone!                         │
│                                          │
└──────────────────────────────────────────┘
```

**User Action:**
1. Paste/Enter: `123456`
2. Click: "Verify OTP"

**System Action:**
- Validate OTP format (6 digits)
- Check expiry time
- Verify it matches database
- Mark as verified
- Create reset token

---

### Screen 4: Reset Password Form
```
┌──────────────────────────────────────────┐
│                                          │
│       🔓 SET NEW PASSWORD                │
│    Create a strong new password for      │
│        your account                      │
│                                          │
│  Progress: ████████████ Step 3 of 3      │
│                                          │
│  New Password:                           │
│  ┌──────────────────────┐               │
│  │ MyNewPassword123! [👁️] │ (show/hide) │
│  └──────────────────────┘               │
│                                          │
│  Password Strength: ▓▓▓▓▓░░░░░░ STRONG   │
│                                          │
│  Confirm Password:                       │
│  ┌──────────────────────┐               │
│  │ MyNewPassword123! [👁️] │              │
│  └──────────────────────┘               │
│                                          │
│  ✓ Passwords match                      │
│                                          │
│  Password Requirements:                 │
│  • At least 8 characters long ✓         │
│  • Mix of upper/lowercase ✓             │
│  • At least one number ✓                │
│  • At least one special char ✓          │
│                                          │
│      [✓ RESET PASSWORD]                 │
│                                          │
│  🔒 Keep your password safe: Never       │
│     share it with anyone.                │
│                                          │
└──────────────────────────────────────────┘
```

**User Action:**
1. Enter new password
2. Confirm password
3. Click: "Reset Password"

**System Action:**
- Validate password (8+ chars, match)
- Hash with bcrypt
- Update users table
- Mark token as used
- Send confirmation email

---

### Email: Password Reset Successful
```
From: noreply@hostelhub.com
To: prajwal@student.com
Subject: Hostel Management - Password Changed Successfully

╔════════════════════════════════════════════╗
║         🏨 HostelHub                       ║
║  Hostel Management System                  ║
╚════════════════════════════════════════════╝

Hello Prajwal Tandekar,

✓ Your password has been successfully changed!

You can now log in with your new password at:
[LOGIN TO HOSTELHUB]

💡 Tip: If you did not request this password change, 
   please contact our support team immediately.

Your account security is important to us.

---
HostelHub Support Team
hostelhub@work.com | 7030710886
© 2024 HostelHub. All rights reserved.
```

---

### Screen 5: Success Message
```
┌──────────────────────────────────────────┐
│                                          │
│  ✅ PASSWORD RESET SUCCESSFULLY          │
│                                          │
│  Your password has been changed!        │
│                                          │
│  You can now log in with your            │
│  new password.                           │
│                                          │
│     [→ GO TO LOGIN PAGE]                 │
│                                          │
│  A confirmation email has been sent      │
│  to your registered email address.       │
│                                          │
└──────────────────────────────────────────┘

↓ Automatically redirects to login...
```

---

### Screen 6: Login with New Password
```
┌──────────────────────────────────────────┐
│                                          │
│            HOSTEL HUB LOGIN              │
│         Hostel Management System         │
│                                          │
│  Username: [prajwal________]             │
│                                          │
│  Password: [MyNewPassword123!] [👁️]      │
│                                          │
│            [🔐 LOGIN]                    │
│                                          │
│  Forgot Password? [Link]                 │
│                                          │
│  Don't have account? [Register]          │
│                                          │
│  ✅ Login successful!                    │
│  → Redirecting to dashboard...           │
│                                          │
└──────────────────────────────────────────┘
```

---

## Error Scenarios

### Scenario 1: Wrong OTP
```
┌──────────────────────────────────────────┐
│       🛡️ VERIFY OTP                       │
│                                          │
│  Enter OTP Code:                         │
│  [999999] ← Wrong OTP entered           │
│                                          │
│       [✓ VERIFY OTP]                    │
│                                          │
│  ❌ Invalid OTP. Please try again.       │
│                                          │
│  [🔄 Resend OTP] or try different code  │
│                                          │
└──────────────────────────────────────────┘
```

**What Happens:**
- User can retry immediately
- Or click "Resend OTP" for a new code

---

### Scenario 2: OTP Expired
```
┌──────────────────────────────────────────┐
│       🛡️ VERIFY OTP                       │
│                                          │
│  Enter OTP Code:                         │
│  [______] (but 10+ minutes passed)      │
│                                          │
│       [✓ VERIFY OTP]                    │
│                                          │
│  ❌ OTP has expired. Please request a    │
│     new one.                             │
│                                          │
│  [🔄 Resend OTP] ← Get new OTP          │
│                                          │
└──────────────────────────────────────────┘
```

**What Happens:**
- Click "Resend OTP" to get new code
- Receive new OTP in email
- Can try again

---

### Scenario 3: Weak Password
```
┌──────────────────────────────────────────┐
│       🔓 SET NEW PASSWORD                 │
│                                          │
│  New Password:                           │
│  [pass] ← Too short!                     │
│                                          │
│  Password Strength: ▓░░░░░░░░░░ WEAK    │
│  • At least 8 characters ✗               │
│  • Mix of upper/lowercase ✗              │
│  • At least one number ✗                 │
│  • Special character ✗                   │
│                                          │
│      [✓ RESET PASSWORD] (disabled)      │
│                                          │
│  ❌ Password must be at least 8          │
│     characters long.                     │
│                                          │
└──────────────────────────────────────────┘
```

**What Happens:**
- Button remains disabled until criteria met
- User cannot submit weak password
- Must meet all requirements

---

### Scenario 4: Passwords Don't Match
```
┌──────────────────────────────────────────┐
│       🔓 SET NEW PASSWORD                 │
│                                          │
│  New Password:                           │
│  [MyNewPassword123! ]                    │
│                                          │
│  Confirm Password:                       │
│  [DifferentPassword! ] ← Doesn't match   │
│                                          │
│  ✗ Passwords do not match                │
│                                          │
│      [✓ RESET PASSWORD]                 │
│                                          │
│  ❌ Passwords do not match. Please       │
│     confirm your password.               │
│                                          │
└──────────────────────────────────────────┘
```

**What Happens:**
- User must type matching password
- Can see match status in real-time

---

## Mobile View

### Mobile Login with Forgot Password Link
```
┌────────────────────┐
│  HOSTEL HUB LOGIN  │
│                    │
│ Username:          │
│ [____________]     │
│                    │
│ Password:          │
│ [____________]     │
│                    │
│ [🔐 LOGIN]         │
│                    │
│ 🔗 Forgot Pass?    │ ← Responsive link
│                    │
│ Register           │
│                    │
└────────────────────┘
```

### Mobile OTP Entry
```
┌────────────────────┐
│ 🛡️ VERIFY OTP      │
│                    │
│ Sent to:           │
│ **wa****com        │
│                    │
│ OTP Code:          │
│ ┌──────────────┐   │
│ │ 1 2 3 4 5 6  │   │
│ │(large input) │   │
│ └──────────────┘   │
│                    │
│ ⏱️ Expires: 14:47  │
│                    │
│ [✓ VERIFY]         │
│                    │
│ [🔄 RESEND]        │
│                    │
└────────────────────┘
```

---

## Backend Flow (What Happens Behind Scenes)

```
User Clicks "Forgot Password?"
        ↓
    /forgot-password GET → Show form
        ↓
User enters: prajwal, Email selected
        ↓
    /forgot-password POST
        ↓
Database Query: SELECT user WHERE username="prajwal"
        ↓
Result: id=3, email=prajwal@student.com, full_name="Prajwal Tandekar"
        ↓
Generate OTP: random(100000, 999999) → "123456"
        ↓
Calculate Expiry: now() + 10 minutes
        ↓
Insert into password_reset_otp table:
  - user_id: 3
  - otp_code: "123456"
  - expires_at: 2026-07-22 14:47:19
        ↓
Send Email via SMTP:
  - To: prajwal@student.com
  - Subject: Hostel Management - Password Reset OTP
  - Body: (HTML email with OTP 123456)
        ↓
Store Session:
  - session['otp_user_id'] = 3
  - session['otp_method'] = 'email'
        ↓
Redirect to /verify-otp
        ↓
User receives email in ~1 second ✅
```

---

## Summary of Screens

| # | Screen | Purpose | User Action |
|---|--------|---------|------------|
| 1 | Login | Access form | Click "Forgot Password?" |
| 2 | Forgot Password | Request OTP | Enter username + select method |
| 3 | OTP Verification | Verify identity | Enter 6-digit OTP from email |
| 4 | Password Reset | Set new password | Enter new password (8+ chars) |
| 5 | Success | Confirm reset | Click "Go to Login" |
| 6 | Login | Use new password | Login with new credentials |

---

## Key Features Illustrated

✅ **Beautiful UI** - Glass-morphism design, modern colors
✅ **Clear Progress** - User knows they're on step 3 of 3
✅ **Real-time Feedback** - Password strength, match status shown live
✅ **Security** - Masked email, password visibility toggle, warnings
✅ **Error Handling** - Clear error messages with next steps
✅ **Mobile Ready** - All screens responsive and touch-friendly
✅ **Accessibility** - Icons, colors, text for clarity

---

That's the complete visual experience! 🎨
