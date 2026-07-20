# ✅ Fix: "Database connection error. Please try again." During Registration

## ❌ Problem
When registering a new student, you get:
```
Database connection error. Please try again.
```

## ✅ Root Cause
MySQL has authentication issues. The root user can only connect via socket, not TCP.

## 🔧 Solution: Quick Setup

### **Option 1: Automated Setup (RECOMMENDED)**

Run this script (it will do everything):
```bash
bash /home/prajwal/Programs/Hostel/setup_mysql.sh
```

This will:
1. ✅ Start MySQL service
2. ✅ Create database properly
3. ✅ Load all tables
4. ✅ Insert sample data
5. ✅ Verify everything works

**Then run Flask:**
```bash
cd /home/prajwal/Programs/Hostel
python app.py
```

### **Option 2: Manual Setup**

If script doesn't work, do this manually:

#### Step 1: Start MySQL
```bash
sudo service mysql start
```

#### Step 2: Create Database
```bash
sudo mysql -u root << 'SQL'
DROP DATABASE IF EXISTS hostel_management;
CREATE DATABASE hostel_management;
SQL
```

#### Step 3: Load Schema
```bash
sudo mysql -u root hostel_management < /home/prajwal/Programs/Hostel/config/database.sql
```

#### Step 4: Verify
```bash
sudo mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;"
```

Should show:
```
COUNT(*)
5
```

Then run Flask:
```bash
cd /home/prajwal/Programs/Hostel
python app.py
```

---

## 🎯 Complete Commands (Copy & Paste)

**All-in-one command:**
```bash
sudo service mysql start && sleep 2 && sudo mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql && cd /home/prajwal/Programs/Hostel && python app.py
```

Or use the script:
```bash
bash /home/prajwal/Programs/Hostel/setup_mysql.sh && cd /home/prajwal/Programs/Hostel && python app.py
```

---

## 📋 Test Registration

After Flask starts:

1. Open: `http://10.252.129.72:5000`
2. Click "Register"
3. Fill in the form:
   - Full Name: Test Student
   - Username: teststudent
   - Email: test@student.com
   - Password: test123
   - Roll Number: CO1234
   - Branch: CSE
4. Click "Register"

Should see: **"Registration successful! Please log in."**

---

## 👥 Then Login With

- **Admin**: admin / admin123
- **Existing Student**: prajwal / admin123
- **Your New Account**: teststudent / test123

---

## ✨ What Changed

Database connection now:
1. ✅ Tries TCP connection (host/port)
2. ✅ Falls back to socket connection for root user
3. ✅ Better error messages
4. ✅ Automatic reconnection

---

## 🆘 If Still Not Working

**Check MySQL is running:**
```bash
sudo systemctl status mysql
```

**Check database exists:**
```bash
sudo mysql -u root -e "SHOW DATABASES;"
```

Should include `hostel_management`

**Check tables exist:**
```bash
sudo mysql -u root hostel_management -e "SHOW TABLES;"
```

Should show 11 tables

**Reset everything:**
```bash
bash /home/prajwal/Programs/Hostel/setup_mysql.sh
```

---

## 🎉 NOW YOU'RE READY!

Run Flask and test registration! It will work now! 🚀
