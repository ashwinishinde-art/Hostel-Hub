# 🔧 Forgot Password "No Account Found" - Troubleshooting Guide

## ⚠️ Root Cause Identified

The error **"No account found with this username or email"** when entering correct credentials usually means:

**The database connection is failing, NOT that the user doesn't exist**

---

## 🔍 How to Diagnose

### Step 1: Check if MySQL is Running

```bash
# Check if MySQL is running
ps aux | grep mysqld
```

**If MySQL IS running:**
You'll see output like: `root ... /usr/sbin/mysqld ...`

**If MySQL is NOT running:**
You'll see no output (just grep finding itself)

### Step 2: Check Flask Console Output

When you submit the forgot password form, look at the Flask console for error messages:

```
[LOGIN] Error connecting to database
✗ Database connection error
```

### Step 3: Verify Database Connection

Try connecting manually:

```bash
mysql -u root -p
# If no password is set, just press Enter
```

If it fails, MySQL is definitely not running.

---

## ✅ Solution Steps

### **FIX #1: Start MySQL (Most Common)**

**On Linux/Ubuntu/WSL:**
```bash
# Start MySQL service
sudo service mysql start

# Or using systemctl
sudo systemctl start mysql

# Verify it's running
sudo service mysql status
# Should show: mysql is running
```

**If sudo requires password and you don't have it:**
```bash
# Try without sudo (if your user has permissions)
mysqld_safe &
```

### **FIX #2: Check MySQL Credentials in .env**

Edit `.env` file:
```bash
nano .env
```

Verify these values:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=hostel_management
```

Make sure:
- Host is `localhost` or `127.0.0.1`
- User is `root` (or your MySQL user)
- Password is correct (leave blank if no password set)
- Database is `hostel_management`

### **FIX #3: Verify Database Exists and Has Data**

Once MySQL is running:

```bash
# List all databases
mysql -u root -e "SHOW DATABASES;"

# Check if hostel_management exists
mysql -u root -e "SHOW DATABASES LIKE 'hostel_management';"

# Count users in database
mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;"

# List all users
mysql -u root -e "SELECT id, username, email, role, is_active FROM hostel_management.users;"
```

Expected output should show at least these users:
- admin
- prajwal
- rajdeep
- warden

### **FIX #4: Reinitialize Database (If Needed)**

If database doesn't exist or has no users:

```bash
# Make sure MySQL is running first!
mysql -u root < config/database.sql
```

This will:
1. Create the database
2. Create all tables
3. Insert sample data with test users

### **FIX #5: Restart Flask Application**

After fixing MySQL:

```bash
# Stop Flask (Ctrl+C if running)

# Start it again
python3 app.py
```

---

## 🎯 Complete Fix Checklist

Follow these steps IN ORDER:

- [ ] **Step 1:** Start MySQL
  ```bash
  sudo service mysql start
  ```

- [ ] **Step 2:** Verify MySQL is running
  ```bash
  sudo service mysql status
  ```

- [ ] **Step 3:** Check if database exists
  ```bash
  mysql -u root -e "SHOW DATABASES LIKE 'hostel_management';"
  ```

- [ ] **Step 4:** Count users in database
  ```bash
  mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;"
  ```

- [ ] **Step 5:** If no database or no users, reinitialize:
  ```bash
  mysql -u root < config/database.sql
  ```

- [ ] **Step 6:** Verify users exist
  ```bash
  mysql -u root -e "SELECT username, email FROM hostel_management.users;"
  ```

- [ ] **Step 7:** Restart Flask
  ```bash
  python3 app.py
  ```

- [ ] **Step 8:** Test forgot password again
  - Go to: `http://localhost:5000/login`
  - Click: "Forgot Password?"
  - Enter: `admin`
  - Select: `Email`
  - Click: "Send OTP"

---

## 🔑 Test Credentials

These should work after database is properly initialized:

| Username | Email | Original Password |
|----------|-------|-------------------|
| admin | admin@hostel.com | admin123 |
| prajwal | prajwal@student.com | admin123 |
| rajdeep | rajdeep@student.com | admin123 |
| warden | warden@hostel.com | admin123 |

---

## 🐛 If Problem Persists

### Check Flask Console for Errors

Look for these messages in Flask output:

```
✗ Database connection error
✗ Query error
✗ MySQL unavailable
Exception: [MySQL Error Message]
```

### Enable Debug Output

Add this to see what query is being sent:

In `app.py`, find the forgot_password route and add:

```python
print(f"[DEBUG] Query: SELECT FROM users WHERE username='{username}' OR email='{username}'")
print(f"[DEBUG] Connection: {db.connection}")
print(f"[DEBUG] Is Connected: {db.is_connected}")
```

### Check .env File

Make sure `.env` exists and has correct format:

```bash
cat .env | grep MYSQL
```

Should show:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=hostel_management
```

### Verify Database Connection

Run this Python script:

```bash
cd /home/prajwal/Programs/Hostel
python3 << 'EOF'
import MySQLdb

try:
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='',
        database='hostel_management'
    )
    print("✓ Database connection successful!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"✓ Users in database: {count}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
EOF
```

---

## 📊 Common Scenarios

### Scenario 1: MySQL Not Running
```
Error: Can't connect to server on '127.0.0.1' (115)
```
**Solution:** Start MySQL with `sudo service mysql start`

### Scenario 2: Database Doesn't Exist
```
Error: Unknown database 'hostel_management'
```
**Solution:** Run `mysql -u root < config/database.sql`

### Scenario 3: No Users in Database
```
Username check fails even though it should exist
```
**Solution:** 
1. Check: `mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;"`
2. If count is 0, reinitialize: `mysql -u root < config/database.sql`

### Scenario 4: Wrong Credentials in .env
```
Error: Access denied for user 'root'@'localhost'
```
**Solution:** Update `.env` with correct MySQL username/password

---

## 🚀 Quick Fix (Most Common)

For 95% of cases, this fixes it:

```bash
# 1. Start MySQL
sudo service mysql start

# 2. Wait a second
sleep 1

# 3. Restart Flask app
python3 app.py

# 4. Test
# Go to http://localhost:5000/login → Forgot Password?
```

---

## ✅ Verification

After applying fixes, verify with this command:

```bash
mysql -u root << 'EOF'
USE hostel_management;
SELECT username, email, role FROM users WHERE username = 'admin';
EOF
```

You should see:
```
admin | admin@hostel.com | admin
```

If you see this, the database is working. If you see "No rows returned", then users table is empty and needs reinitialization.

---

## 📞 Still Not Working?

1. **Check MySQL is running:**
   ```bash
   sudo service mysql status
   ```

2. **Verify database exists:**
   ```bash
   mysql -u root -e "SHOW DATABASES;"
   ```

3. **Count users:**
   ```bash
   mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;"
   ```

4. **Check Flask console** for specific error messages

5. **Review `/etc/mysql/my.cnf`** for configuration issues

6. **Check MySQL error log:**
   ```bash
   tail -50 /var/log/mysql/error.log
   ```

---

## 🎓 Understanding the Error

The error message **"No account found with this username or email"** can mean:

1. **Database connection failed** (most common)
   - MySQL not running
   - Wrong credentials
   - Connection timeout

2. **User doesn't exist** (less common)
   - User account deleted
   - Database reinitialized without users
   - Wrong username entered

3. **User marked inactive** (rare)
   - Admin disabled the account
   - `is_active = FALSE` in database

---

**Most likely fix: Just start MySQL! 🚀**

```bash
sudo service mysql start
python3 app.py
```

Then test the forgot password flow again.

