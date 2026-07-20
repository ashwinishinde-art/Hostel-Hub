# ⚠️ URGENT: MySQL Authentication Issue

## Root Cause Identified
```
ERROR 1698 (28000): Access denied for user 'root'@'localhost'
```

MySQL/MariaDB is running but root user has authentication restriction (socket-based auth only, or plugin authentication).

## Solution: Manual Database Setup

Since automated setup hits MySQL auth issues, you need to run a ONE-TIME manual command with proper privileges.

### **FIX (Choose One):**

#### **Option A: Using sudo (Recommended)**
```bash
sudo mysql -u root << 'SQL'
DROP DATABASE IF EXISTS hostel_management;
CREATE DATABASE hostel_management CHARACTER SET utf8mb4;
