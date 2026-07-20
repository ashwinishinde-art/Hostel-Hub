# Forgot Password Feature - Architecture & Flow Diagrams

## 🔄 Complete User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOGIN PAGE                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Username: [_________________]                         │   │
│  │  Password: [_________________]                         │   │
│  │  [Sign In] [Forgot Password?] ← CLICK HERE            │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              FORGOT PASSWORD PAGE                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Username or Email: [_________________]               │   │
│  │                                                        │   │
│  │  How would you like to receive OTP?                  │   │
│  │  ◉ Email  ○ SMS                                       │   │
│  │                                                        │   │
│  │  [Send OTP]                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Generate 6-digit   │
        │ OTP (random)       │
        │ Expiry: 10 minutes │
        └────────┬───────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
    ┌─────────┐   ┌──────────┐
    │  EMAIL  │   │   SMS    │
    │  SMTP   │   │  TWILIO  │
    │ Gmail   │   │ Optional │
    └────┬────┘   └────┬─────┘
         │             │
         └──────┬──────┘
                ▼
    ┌──────────────────────┐
    │ OTP Record Created   │
    │ - Stored in DB       │
    │ - Marked unverified  │
    │ - Expires in 10 min  │
    └──────────┬───────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│              OTP VERIFICATION PAGE                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Enter OTP Code: [0][0][0][0][0][0]                  │   │
│  │  ⏰ OTP expires at: 10:35 AM                          │   │
│  │                                                        │   │
│  │  [Verify OTP]  [Didn't receive?]                     │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Validate OTP:      │
        │ ✓ Matches code     │
        │ ✓ Not expired      │
        │ ✓ Not already used │
        └────────┬───────────┘
                 │
         ┌───────┴───────┐
         │               │
      VALID            INVALID
         │               │
         ▼               ▼
    ┌─────────┐      ┌──────────┐
    │ Generate│      │ Show     │
    │ Reset   │      │ Error    │
    │ Token   │      │ Msg      │
    └────┬────┘      └────┬─────┘
         │                │
         ▼                ▼
    Create record   [Retry/Resend]
    in reset token      │
    table               ▼
         │         (return to OTP page)
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              RESET PASSWORD PAGE                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  New Password: [_________________]                    │   │
│  │  [████████░░░░░░░░░░░░░░░░░░░░░] Strength: Fair    │   │
│  │                                                        │   │
│  │  Confirm Password: [_________________]              │   │
│  │  ✓ Passwords match                                  │   │
│  │                                                        │   │
│  │  [Reset Password]                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Validate Password: │
        │ ✓ 8+ characters    │
        │ ✓ Uppercase + Lower│
        │ ✓ Numbers          │
        │ ✓ Matches confirm  │
        └────────┬───────────┘
                 │
         ┌───────┴───────┐
         │               │
      VALID            INVALID
         │               │
         ▼               ▼
    ┌─────────┐      ┌──────────┐
    │ Hash    │      │ Show     │
    │ with    │      │ Error    │
    │ bcrypt  │      │ Message  │
    └────┬────┘      └────┬─────┘
         │                │
         ▼                ▼
    Update user   (return to form)
    in DB          │
         │          ▼
         │     [User fixes]
         │          │
         └──────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Mark Token as Used       │
    │ Mark OTP as Used         │
    │ Send Confirmation Email  │
    └──────────┬───────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│              LOGIN SUCCESS                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ✓ Password reset successfully!                        │   │
│  │  Please log in with your new password.                │   │
│  │  [Go to Login]                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
        Username + New Password
               │
               ▼
         ✅ LOGIN SUCCESS
```

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        FLASK APP                                │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                      ROUTES                             │  │
│  │  • /forgot-password    (GET/POST)                      │  │
│  │  • /verify-otp         (GET/POST)                      │  │
│  │  • /resend-otp         (POST)                          │  │
│  │  • /reset-password     (GET/POST)                      │  │
│  └──────┬──────────────────────────────────────────────────┘  │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              UTILS / OTP_MANAGER                        │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ OTPManager                                      │   │  │
│  │  │ • generate_otp()                               │   │  │
│  │  │ • get_otp_expiry()                             │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ EmailService                                    │   │  │
│  │  │ • send_otp_email()                             │   │  │
│  │  │ • send_password_reset_confirmation()           │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │ SMSService (Optional)                           │   │  │
│  │  │ • send_otp_sms()                               │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └──────┬──────────────────────────────────────────────────┘  │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────┐  ┌──────────────────┐                  │
│  │   Gmail SMTP     │  │  Twilio API      │                  │
│  │   (Primary)      │  │  (Secondary)     │                  │
│  └──────────────────┘  └──────────────────┘                  │
└────────────────────────────────────────────────────────────────┘
         │                         │
         ▼                         ▼
    ┌─────────────┐         ┌──────────┐
    │   Email     │         │   SMS    │
    │   Server    │         │  Gateway │
    └─────────────┘         └──────────┘
         │                         │
         ▼                         ▼
    ┌─────────────┐         ┌──────────┐
    │   User's    │         │ User's   │
    │   Inbox     │         │ Phone    │
    └─────────────┘         └──────────┘
```

---

## 📊 Database Interaction Flow

```
User Form Input
      │
      ▼
┌──────────────────────────────┐
│   Password Reset OTP Table   │
│  ┌────────────────────────┐ │
│  │ id (PK)              │ │
│  │ user_id (FK)         │ │
│  │ email                │ │
│  │ phone                │ │
│  │ otp_code             │ │
│  │ otp_method           │ │
│  │ is_verified          │ │
│  │ is_used              │ │
│  │ created_at           │ │
│  │ expires_at           │ │
│  │ verified_at          │ │
│  └────────────────────────┘ │
└──────────────────────────────┘
      │
      ▼
┌──────────────────────────────┐
│  Password Reset Tokens Table │
│  ┌────────────────────────┐ │
│  │ id (PK)              │ │
│  │ user_id (FK)         │ │
│  │ token                │ │
│  │ otp_id (FK)          │ │
│  │ is_used              │ │
│  │ created_at           │ │
│  │ expires_at           │ │
│  │ reset_at             │ │
│  └────────────────────────┘ │
└──────────────────────────────┘
      │
      ▼
┌──────────────────────────────┐
│        Users Table           │
│  ┌────────────────────────┐ │
│  │ id                   │ │
│  │ username             │ │
│  │ email                │ │
│  │ password_hash ◄────┐ │ │ (Updated)
│  │ phone                │ │
│  │ updated_at           │ │
│  └────────────────────────┘ │
└──────────────────────────────┘
```

---

## 🔐 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│              LAYER 1: INPUT VALIDATION                      │
│  • Username/Email format check                             │
│  • OTP code format (numeric only, 6 digits)               │
│  • Password length (8+ characters)                         │
│  • Whitespace trimming                                     │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 2: OTP VALIDATION                        │
│  • Exact code matching                                     │
│  • Expiry time checking                                    │
│  • One-time use enforcement                               │
│  • User verification status                                │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 3: TOKEN VALIDATION                      │
│  • Token existence checking                                │
│  • Token expiry verification                               │
│  • Usage status verification                               │
│  • User association confirmation                           │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 4: PASSWORD HASHING                      │
│  • Bcrypt algorithm                                        │
│  • Salt generation                                         │
│  • 12-round hashing (default)                             │
│  • No plaintext storage                                    │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 5: DATABASE SECURITY                     │
│  • Parameterized queries (SQL injection prevention)       │
│  • Foreign key constraints                                 │
│  • Transaction management                                  │
│  • Error handling                                          │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 6: SESSION SECURITY                      │
│  • Server-side session storage                             │
│  • Automatic session cleanup                               │
│  • HTTPS support (production)                              │
│  • Secure cookie flags (production)                        │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LAYER 7: AUDIT LOGGING                         │
│  • Login attempts tracked                                  │
│  • Password resets logged                                  │
│  • Email/SMS delivery status                               │
│  • Error tracking                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 State Transitions

```
OTP Record Lifecycle:
┌──────────────────┐
│   GENERATED      │
│  is_verified: 0  │
│  is_used: 0      │
└────────┬─────────┘
         │
    [User enters correct OTP]
         │
         ▼
┌──────────────────┐
│  VERIFIED        │
│  is_verified: 1  │
│  is_used: 0      │
└────────┬─────────┘
         │
    [Password successfully reset]
         │
         ▼
┌──────────────────┐
│  USED            │
│  is_verified: 1  │
│  is_used: 1      │
└──────────────────┘

Token Record Lifecycle:
┌──────────────────┐
│   GENERATED      │
│  is_used: 0      │
└────────┬─────────┘
         │
    [User sets new password]
         │
         ▼
┌──────────────────┐
│  USED            │
│  is_used: 1      │
└──────────────────┘
```

---

## 🚨 Error Handling Flow

```
Input Received
      │
      ▼
Is username/email valid?
   YES │ NO
      │  └─► "No account found with this username or email"
      ▼
Is OTP method compatible?
   YES │ NO
      │  └─► "No phone/email on file. Use alternative method"
      ▼
OTP Generated & Sent
      │
      ▼
User enters OTP
      │
      ▼
Is OTP code present?
   YES │ NO
      │  └─► "OTP code is required"
      ▼
Is OTP expired?
   YES │ NO
      │  └─► "OTP has expired. Request new one"
      ▼
Does OTP match?
   YES │ NO
      │  └─► "Invalid OTP. Try again or resend"
      ▼
OTP Verified ✓
      │
      ▼
User enters new password
      │
      ▼
Is password 8+ characters?
   YES │ NO
      │  └─► "Password must be at least 8 characters"
      ▼
Do passwords match?
   YES │ NO
      │  └─► "Passwords do not match"
      ▼
Password Reset ✓
      │
      ▼
Confirmation Email Sent
      │
      ▼
Redirect to Login
      │
      ▼
    SUCCESS ✅
```

---

## 📱 Mobile Flow Diagram

```
┌─────────────────────┐
│   LOGIN PAGE        │
│ ┌─────────────────┐ │
│ │ Username        │ │
│ │ Password        │ │
│ │ [Forgot Pwd?]   │ │
│ └─────────────────┘ │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   FORGOT PASSWORD (Mobile)          │
│ ┌───────────────────────────────┐   │
│ │ Username or Email:          │   │
│ │ ┌─────────────────────────┐ │   │
│ │ │                         │ │   │
│ │ └─────────────────────────┘ │   │
│ │                             │   │
│ │ ◉ Email    ○ SMS           │   │
│ │                             │   │
│ │ [SEND OTP]                  │   │
│ └───────────────────────────────┘   │
└──────────┬──────────────────────────┘
           │
           ▼
    📧 EMAIL RECEIVED
           │
           ▼
┌─────────────────────────────────────┐
│   OTP VERIFICATION (Mobile)         │
│ ┌───────────────────────────────┐   │
│ │ Enter OTP:                  │   │
│ │ [0] [0] [0] [0] [0] [0]    │   │
│ │                             │   │
│ │ ⏰ Expires: 10:35 AM        │   │
│ │                             │   │
│ │ [VERIFY]  [RESEND]         │   │
│ └───────────────────────────────┘   │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   RESET PASSWORD (Mobile)           │
│ ┌───────────────────────────────┐   │
│ │ New Password:               │   │
│ │ ┌─────────────────────────┐ │   │
│ │ │ Pass•••••••••••••••     │ │   │
│ │ │ [👁️]                     │ │   │
│ │ └─────────────────────────┘ │   │
│ │ [████░░░░░░░░░░] Fair      │   │
│ │                             │   │
│ │ Confirm Password:          │   │
│ │ ┌─────────────────────────┐ │   │
│ │ │ Pass•••••••••••••••     │ │   │
│ │ │ [👁️]                     │ │   │
│ │ └─────────────────────────┘ │   │
│ │ ✓ Passwords match          │   │
│ │                             │   │
│ │ [RESET PASSWORD]            │   │
│ └───────────────────────────────┘   │
└──────────┬──────────────────────────┘
           │
           ▼
    ✅ SUCCESS MESSAGE
           │
           ▼
    [Go to Login]
```

---

## 🔗 Component Dependencies

```
app.py (Main Routes)
    ├─ config.config (Configuration)
    │   └─ .env (Environment variables)
    ├─ config.database (DB Connection)
    │   └─ config/database.sql (Schema)
    └─ utils.otp_manager (OTP Logic)
        ├─ EmailService (Gmail SMTP)
        │   └─ smtplib
        └─ SMSService (Twilio API)
            └─ twilio library

templates/
    ├─ forgot_password.html
    ├─ verify_otp.html
    ├─ reset_password.html
    └─ base.html (Inheritance)

Database Tables:
    ├─ users (existing)
    ├─ password_reset_otp (new)
    └─ password_reset_tokens (new)
```

---

This complete diagram set helps visualize how the forgot password feature works at every level!
