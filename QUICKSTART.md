# Hostel Management System - Quick Start Guide

## ✅ What's Been Built

A fully functional hostel management system with the following components:

### Core Infrastructure
- ✅ MySQL Database Schema (13 tables with sample data)
- ✅ Flask Application Setup with Configuration
- ✅ User Authentication System (Admin, Student, Warden roles)
- ✅ Secure Password Hashing (bcrypt)
- ✅ Session Management with Flask-Login

### Frontend Templates
- ✅ Base Template with Navigation Bar
- ✅ Home/Landing Page with Statistics
- ✅ Login Page
- ✅ Registration Page
- ✅ Student Dashboard
- ✅ Student Profile
- ✅ Complaints Module
- ✅ Visitor Requests Module
- ✅ Fees Management
- ✅ Room Details
- ✅ Notices Display
- ✅ Admin Dashboard
- ✅ Room Management

### Backend Functionality
- ✅ User Registration & Login
- ✅ Role-Based Access Control
- ✅ Student Module (Dashboard, Profile, Complaints, Visitors, Fees, Room, Notices)
- ✅ Admin Module (Dashboard, Rooms, Students, Complaints, Visitors, Notices, Fees)
- ✅ Warden Module (Dashboard, Complaints, Visitors, Notices, Rooms, Students)

### Database Tables
1. users - User accounts with roles
2. students - Student-specific information
3. rooms - Room inventory
4. room_occupancy - Student-room allocation
5. complaints - Complaint management
6. visitors - Visitor requests
7. fees - Fee management
8. notices - Hostel notices
9. gallery - Image gallery
10. payment_history - Payment records
11. hostel_settings - Configuration settings

## 🚀 Quick Start

### Prerequisites
```bash
python3 --version  # Should be 3.8+
mysql --version    # Should be 5.7+
```

### Installation Steps

**1. Install Python Dependencies**
```bash
cd /home/prajwal/Programs/Hostel
pip install -r requirements.txt
```

**2. Setup MySQL Database**
```bash
mysql -u root -p < config/database.sql
```
(If prompted for password, press Enter if no password is set)

**3. Configure Environment**
Edit `.env` file with your MySQL credentials:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=  # Your MySQL password
MYSQL_DB=hostel_management
```

**4. Run the Application**
```bash
python app.py
```

**5. Access in Browser**
```
http://localhost:5000
```

## 📝 Test Accounts

### Admin Login
- **Username:** admin
- **Password:** admin123

### Warden Login
- **Username:** warden
- **Password:** admin123

### Student Logins
- **Username:** prajwal | **Password:** admin123
- **Username:** rajdeep | **Password:** admin123
- **Username:** rutuja | **Password:** admin123

## 📁 Project Structure

```
Hostel/
├── app.py                    # Main Flask app with auth & static pages
├── config/
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database connection handler
│   └── database.sql          # MySQL schema with sample data
├── routes/
│   ├── admin_routes.py       # Admin functionality (rooms, students, complaints, etc.)
│   ├── student_routes.py     # Student functionality (dashboard, profile, complaints, etc.)
│   └── warden_routes.py      # Warden functionality (monitoring, approvals, etc.)
├── templates/
│   ├── base.html             # Base template with navigation
│   ├── index.html            # Home page
│   ├── login.html            # Login form
│   ├── register.html         # Registration form
│   ├── admin/
│   │   ├── dashboard.html    # Admin dashboard
│   │   └── rooms.html        # Room management
│   ├── student/
│   │   ├── dashboard.html    # Student dashboard
│   │   ├── profile.html      # Profile management
│   │   ├── complaints.html   # Complaints list
│   │   ├── visitors.html     # Visitor requests
│   │   ├── fees.html         # Fee details
│   │   ├── room.html         # Room info
│   │   └── notices.html      # Notices
│   └── warden/
│       ├── dashboard.html    # Warden dashboard
│       ├── complaints.html   # View complaints
│       └── visitors.html     # Manage visitors
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
└── README.md                 # Full documentation
```

## 🎯 Key Features Implemented

### Student Features
- ✅ Secure Registration & Login
- ✅ Personal Dashboard
- ✅ Profile Management
- ✅ Room Details & Roommate Info
- ✅ Submit & Track Complaints
- ✅ Visitor Entry Requests
- ✅ Fee Status & Payment History
- ✅ Hostel Notices

### Admin Features
- ✅ Dashboard with Statistics
- ✅ Room Management (Add, Edit, Delete, Allocate)
- ✅ Student List & Management
- ✅ Complaint Management & Resolution
- ✅ Visitor Request Approval/Rejection
- ✅ Fee Tracking & Payment Recording
- ✅ Notice Publishing & Management

### Warden Features
- ✅ Dashboard with Activity Overview
- ✅ Complaint Monitoring & Management
- ✅ Visitor Request Approval/Rejection
- ✅ Room Allocation Review
- ✅ Student Information Access

## 🔒 Security Features

- ✅ Bcrypt Password Hashing
- ✅ SQL Injection Prevention (Parameterized Queries)
- ✅ Role-Based Access Control
- ✅ Session Management
- ✅ XSS Protection (Template Escaping)

## 🛠️ Technology Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Authentication:** Flask-Login + bcrypt
- **Database Driver:** MySQLdb

## 📝 Notes

1. **Database File:** `config/database.sql` contains the complete schema and sample data
2. **Environment Variables:** Configure `.env` for your MySQL setup
3. **Sample Data:** The database includes 5 users (1 admin, 1 warden, 3 students) with sample rooms, complaints, notices, etc.
4. **Password Hashing:** All passwords are hashed using bcrypt with salt

## 🚀 Next Steps

1. Test login with provided credentials
2. Navigate through different dashboards
3. Test complaint submission, visitor requests, room allocation
4. Add more rooms and allocate to students
5. Create new notices and manage fees

## ⚠️ Important

- Change the `SECRET_KEY` in `.env` before deploying to production
- Update MySQL credentials in `.env` with your actual database password
- Keep the `.env` file secure and never commit it to version control

## 💡 Tips

- Use Firefox or Chrome for best compatibility
- Clear browser cache if styles don't load properly
- Check MySQL is running before starting the Flask app
- Database queries use parameterized statements for security

---

**System Ready to Use!** 🎉

For detailed documentation, see README.md
