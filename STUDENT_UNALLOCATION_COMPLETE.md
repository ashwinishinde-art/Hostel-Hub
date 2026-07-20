# Student Unallocation - Complete Guide

## Overview
This document explains how to unallocate all students from their rooms without unregistering them from the system.

## What Gets Changed?
✅ **Room allocations**: Marked as 'Inactive'
✅ **Student registrations**: REMAIN ACTIVE (students are NOT unregistered)
✅ **Student data**: Preserved (all fees, complaints, profiles remain)
✅ **Room availability**: Rooms become available for new allocations

## Methods to Unallocate Students

### Method 1: Web Interface (Easiest for Most Users)

**Steps:**
1. **Start the Flask app:**
   ```bash
   cd /home/prajwal/Programs/Hostel
   python app.py
   ```

2. **Login as Admin:**
   - URL: `http://localhost:5000/login`
   - Username: `admin`
   - Password: `admin123`

3. **Go to Unallocate Page:**
   - Navigate to: `Admin → Rooms → Unallocate All Students`
   - Or direct URL: `http://localhost:5000/admin/unallocate-all-students`

4. **Review Students:**
   - The page shows all currently allocated students
   - Room numbers and check-in dates are displayed

5. **Confirm Unallocation:**
   - Check the confirmation checkbox
   - Click "Unallocate X Student(s)" button
   - Confirm in the popup dialog

6. **Done!**
   - Success message appears
   - Redirects back to Rooms page
   - All students are now unallocated but registered

---

### Method 2: Command Line Python Script

**Prerequisites:**
- MySQL/MariaDB service must be running

**Steps:**
```bash
# 1. Navigate to project directory
cd /home/prajwal/Programs/Hostel

# 2. Start MySQL service (if not running)
sudo systemctl start mysql
# or
sudo service mysql start

# 3. Run the unallocation script
python unallocate_students.py

# 4. Review the list of students
# The script will display all allocated students

# 5. Confirm when prompted
# Type 'yes' and press Enter
```

**Script Output:**
```
============================================================
🏠 HOSTEL MANAGEMENT SYSTEM - STUDENT UNALLOCATION
============================================================

📊 Found 3 student(s) allocated to rooms.

============================================================

📋 Students Currently Allocated:
------------------------------------------------------------
1. Prajwal Tandekar (CO1265) - Room 101
2. Rajdeep Patil (CO1288) - Room 103
3. Rutuja Patil (CO1240) - Room 201

============================================================

⚠️  Are you sure you want to unallocate all 3 student(s)? (yes/no): 
```

---

### Method 3: Direct SQL Execution

**Option A: Execute SQL File**
```bash
mysql -u root hostel_management < /home/prajwal/Programs/Hostel/unallocate_students.sql
```

**Option B: Interactive MySQL Shell**
```bash
# Start MySQL
mysql -u root

# In MySQL shell:
USE hostel_management;

-- View current allocations before unallocation
SELECT 
    u.full_name,
    s.roll_number,
    r.room_number,
    ro.check_in_date
FROM room_occupancy ro
JOIN users u ON ro.student_id = u.id
JOIN students s ON u.id = s.user_id
JOIN rooms r ON ro.room_id = r.id
WHERE ro.status = 'Active'
ORDER BY r.room_number;

-- Unallocate all students
UPDATE room_occupancy 
SET status = 'Inactive'
WHERE status = 'Active';

-- Verify (should return 0)
SELECT COUNT(*) as active_allocations FROM room_occupancy WHERE status = 'Active';

-- Verify all students are still registered
SELECT COUNT(*) as total_students FROM users WHERE role = 'student';
```

---

## Database Changes

### Before Unallocation
```sql
-- View room allocations
SELECT ro.id, u.full_name, r.room_number, ro.status
FROM room_occupancy ro
JOIN users u ON ro.student_id = u.id
JOIN rooms r ON ro.room_id = r.id;

-- Result:
| id  | full_name         | room_number | status   |
|-----|-------------------|-------------|----------|
| 1   | Prajwal Tandekar  | 101         | Active   |
| 2   | Rajdeep Patil     | 103         | Active   |
| 3   | Rutuja Patil      | 201         | Active   |
```

### After Unallocation
```sql
-- Same query:
SELECT ro.id, u.full_name, r.room_number, ro.status
FROM room_occupancy ro
JOIN users u ON ro.student_id = u.id
JOIN rooms r ON ro.room_id = r.id;

-- Result:
| id  | full_name         | room_number | status   |
|-----|-------------------|-------------|----------|
| 1   | Prajwal Tandekar  | 101         | Inactive |
| 2   | Rajdeep Patil     | 103         | Inactive |
| 3   | Rutuja Patil      | 201         | Inactive |
```

### Verification Queries

```sql
-- Check unallocated students (should be 0 after unallocation)
SELECT COUNT(*) FROM room_occupancy WHERE status = 'Active';
-- Result: 0

-- Verify all students are still registered
SELECT COUNT(*) FROM users WHERE role = 'student' AND is_active = TRUE;
-- Result: 3 (or however many you had)

-- Check all inactive allocations
SELECT COUNT(*) FROM room_occupancy WHERE status = 'Inactive';
-- Result: 3 (or however many students were allocated)

-- Verify rooms are now available
SELECT room_number, 
       (SELECT COUNT(*) FROM room_occupancy WHERE room_id = rooms.id AND status = 'Active') as occupied
FROM rooms
ORDER BY room_number;
```

---

## Important Notes

⚠️ **What remains unchanged:**
- Student registrations (all students remain in the system)
- User accounts and login credentials
- Student personal information
- Fee records and payment history
- Complaint records
- Visitor requests and approvals
- Notice board entries
- Gallery images

🔄 **What changes:**
- Only `room_occupancy.status` changes from 'Active' to 'Inactive'
- Rooms are no longer shown as occupied
- Students can be reallocated to new rooms later

---

## Troubleshooting

### Issue: "Can't connect to MySQL server"

**Solution:**
```bash
# Check if MySQL is running
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql

# If using MariaDB
sudo systemctl start mariadb

# Verify MySQL is listening
netstat -tlnp | grep mysql
# Should show: tcp  0  0 127.0.0.1:3306  0.0.0.0:*  LISTEN
```

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:**
```bash
# If no password set:
mysql -u root hostel_management < unallocate_students.sql

# If password is set:
mysql -u root -p hostel_management < unallocate_students.sql
# Then enter password when prompted
```

### Issue: "Database not found"

**Solution:**
```bash
# Ensure database is created
mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql

# Verify database exists
mysql -u root -e "SHOW DATABASES;" | grep hostel_management
```

---

## Recovery

If you accidentally unallocate students and want to restore allocations, you can:

1. **Restore from backup** (if available)
2. **Manually reallocate students** through the web interface:
   - Admin → Rooms → Allocate Room
   - Select each student and room
   - Set the original check-in date

3. **Use SQL to restore status:**
   ```sql
   -- If you know which students should be allocated
   UPDATE room_occupancy 
   SET status = 'Active'
   WHERE student_id IN (3, 4, 5);  -- Replace with actual student IDs
   ```

---

## Summary

| Method | Ease | Speed | Requirements |
|--------|------|-------|--------------|
| Web UI | ⭐⭐⭐⭐⭐ | Medium | Running Flask app |
| Python Script | ⭐⭐⭐⭐ | Medium | MySQL running |
| SQL File | ⭐⭐⭐ | Fast | MySQL running |
| Interactive SQL | ⭐⭐ | Slow | MySQL shell knowledge |

**Recommended:** Use the **Web UI** for ease and visual confirmation, or **Python Script** for automation.

---

## Files Included

- `unallocate_students.py` - Python script for bulk unallocation
- `unallocate_students.sql` - SQL script for direct execution
- `routes/admin_routes.py` - Updated with new unallocation route
- `templates/admin/unallocate_confirmation.html` - Web interface template
- `UNALLOCATE_GUIDE.md` - Quick reference guide
- This file - Complete documentation

---

**Created:** 2026-07-20
**Status:** Ready to use
**Version:** 1.0
