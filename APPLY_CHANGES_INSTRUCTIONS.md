# 🔄 APPLY HOSTEL INFORMATION CHANGES

## Current Status
✅ Files prepared with new information:
- Address: Zeal Chowk, Narhe, Pune
- Phone: 7030710886
- Email: hostelhub@work.com

⚠️ MySQL is currently not running, which prevents automatic updates.

---

## How to Apply Changes

### Option 1: Start MySQL Service & Apply (Recommended)

Open a terminal and run these commands:

```bash
# Start MySQL/MariaDB
sudo systemctl start mariadb
# OR
sudo service mysql start

# Wait for it to start
sleep 3

# Apply the updates
mysql -u root hostel_management < /home/prajwal/Programs/Hostel/UPDATE_HOSTEL_INFO.sql
```

### Option 2: Using Python Script (After MySQL is running)

```bash
# First start MySQL as shown above, then:
cd /home/prajwal/Programs/Hostel
python direct_update_hostel_info.py
```

### Option 3: Recreate Database with New Information

This will reset all data and create fresh database with new hostel information:

```bash
# First start MySQL, then:
mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql
```

### Option 4: Manual MySQL Commands

Start MySQL client and paste these commands:

```sql
USE hostel_management;

UPDATE hostel_settings SET setting_value = 'Zeal Chowk, Narhe, Pune' WHERE setting_key = 'hostel_address';
UPDATE hostel_settings SET setting_value = '7030710886' WHERE setting_key = 'hostel_phone';
UPDATE hostel_settings SET setting_value = 'hostelhub@work.com' WHERE setting_key = 'hostel_email';
UPDATE hostel_settings SET setting_value = 'HostelHub' WHERE setting_key = 'hostel_name';
UPDATE hostel_settings SET setting_value = '7030710886' WHERE setting_key = 'warden_phone';

-- Verify
SELECT * FROM hostel_settings WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_phone');
```

---

## After Applying Changes

### 1. Hard Refresh Browser
- Press: `Ctrl + Shift + R` (Windows/Linux)
- Or: `Cmd + Shift + R` (Mac)

### 2. Verify Changes

**Check Contact Page:**
- Navigate to `/contact`
- Look for the updated hostel information
- Verify all details are correct

**Check Footer:**
- Scroll to bottom of any page
- Should show hostel contact information

**Check Database:**
```sql
SELECT setting_key, setting_value FROM hostel_settings 
WHERE setting_key IN ('hostel_address', 'hostel_phone', 'hostel_email');
```

---

## Files Created

| File | Purpose |
|------|---------|
| `UPDATE_HOSTEL_INFO.sql` | Direct SQL script to update existing database |
| `direct_update_hostel_info.py` | Python script to apply updates |
| `apply_changes.sh` | Bash script to start MySQL and apply updates |
| `config/database.sql` | Updated database schema with new hostel info |
| `HOSTEL_INFO_UPDATED.md` | Documentation of changes |

---

## Troubleshooting

### MySQL Won't Start
```bash
# Check if MySQL is installed
which mysqld

# Try different start commands
sudo systemctl start mysql
sudo systemctl start mariadb
sudo service mysql start
sudo service mariadb start
```

### Connection Refused Error
```bash
# Make sure MySQL is actually running
ps aux | grep -i mysql
ps aux | grep -i mariadb

# Try restarting
sudo systemctl restart mariadb
```

### Permission Denied
```bash
# May need to provide password
mysql -u root -p hostel_management < UPDATE_HOSTEL_INFO.sql
```

### Database Not Found
```sql
-- First create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hostel_management;
USE hostel_management;
-- Then run the SQL file
```

---

## Summary of Changes

The hostel information will be updated in the database and displayed in:

1. ✅ Contact Page (`/contact`)
2. ✅ Footer (all pages)
3. ✅ Admin Dashboard
4. ✅ Public Landing Page
5. ✅ About section

---

## Need Help?

1. Verify MySQL is running: `systemctl status mysql`
2. Check database exists: `mysql -u root -e "SHOW DATABASES;"`
3. Verify credentials: user=`root`, password=empty
4. Check for error logs in MySQL logs

---

**Next Step:** Start MySQL and run the SQL update file shown above!
