# Login Troubleshooting Guide

## Issue: "Invalid username or password" error even with correct credentials

### Root Causes & Solutions

#### 1. **MySQL Database Not Running** (Most Common)
This is the primary issue preventing login from working.

**Check if MySQL is running:**
```bash
ps aux | grep mysqld
```

**If MySQL is NOT running, start it:**

**Option A: Using the provided script**
```bash
bash start_mysql.sh
```

**Option B: Manual start**
```bash
# For Linux/Ubuntu/WSL
sudo service mysql start

# Or for systems with systemctl
sudo systemctl start mysql

# Or for older systems
sudo /etc/init.d/mysql start
```

**Option C: If you don't have sudo access**
```bash
# Check the MySQL error log
cat /var/log/mysql/error.log

# Try starting mysqld directly
mysqld_safe &
```

#### 2. **Database Not Initialized**
The database schema might not be loaded.

**Initialize the database:**
```bash
# Make sure MySQL is running first, then:
mysql -u root -p < config/database.sql

# Or without password (if configured)
mysql -u root < config/database.sql
```

**Verify database exists:**
```bash
mysql -u root -e "SHOW DATABASES;" | grep hostel_management
```

#### 3. **Default Credentials**
Use these credentials to test login:

| Role    | Username | Password   |
|---------|----------|-----------|
| Admin   | `admin`  | `admin123` |
| Warden  | `warden` | `admin123` |
| Student | `prajwal`| `admin123` |
| Student | `rajdeep`| `admin123` |
| Student | `rutuja` | `admin123` |

#### 4. **Check Database Connection Configuration**
Verify `.env` file or `config/database.py`:

```python
# Should match your MySQL setup:
host='127.0.0.1',
user='root',
password='',          # Empty if no password set
database='hostel_management',
port=3306
```

#### 5. **MySQL Not Installed**
If MySQL is not installed:

```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# CentOS/RHEL
sudo yum install mysql-server

# Then start the service:
sudo service mysql start
```

### Quick Diagnostic Steps

Run this to check everything:

```bash
#!/bin/bash

echo "1. Checking if MySQL is running..."
ps aux | grep mysqld | grep -v grep || echo "MySQL not running"

echo -e "\n2. Checking if database exists..."
mysql -u root -e "SHOW DATABASES;" | grep hostel_management || echo "Database not found"

echo -e "\n3. Checking if user table has data..."
mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users;" || echo "Cannot query users"

echo -e "\n4. Checking user accounts..."
mysql -u root -e "SELECT username, role FROM hostel_management.users;" || echo "Cannot list users"
```

### After Fixing

1. **MySQL is running** ✓
2. **Database is initialized** ✓
3. **Try login again with correct credentials**

### Still Having Issues?

Check the Flask console output for detailed error messages:
```bash
python3 app.py
# Look for [LOGIN] debug messages in the output
```

### Common Errors & Meanings

| Error Message | Meaning |
|---|---|
| "Database connection error" | MySQL is not running |
| "Invalid username or password" | User not found OR password is wrong |
| "Cannot connect to server on '127.0.0.1'" | MySQL socket/port issue |
| "Access denied for user 'root'" | MySQL password mismatch |
| "Unknown database" | Database not initialized |

### Reset Everything

If you want to reset the entire setup:

```bash
# 1. Stop MySQL
sudo service mysql stop

# 2. Delete old data (WARNING: DATA LOSS)
sudo rm -rf /var/lib/mysql/hostel_management

# 3. Start MySQL
sudo service mysql start

# 4. Re-initialize database
mysql -u root < config/database.sql

# 5. Start the application
python3 app.py
```
