# How to Unallocate All Students from Rooms

This guide provides multiple methods to unallocate all students from their rooms without unregistering them.

## Prerequisites

- MySQL/MariaDB service must be running
- Access to the hostel database

## Method 1: Using the Python Script (Recommended)

### Step 1: Start MySQL Service

```bash
# For Ubuntu/Debian
sudo systemctl start mysql
# OR
sudo service mysql start

# For systems with MariaDB
sudo systemctl start mariadb
# OR
sudo service mariadb start
```

### Step 2: Run the Unallocation Script

```bash
cd /home/prajwal/Programs/Hostel
python unallocate_students.py
```

The script will:
1. Show all currently allocated students
2. Ask for confirmation
3. Unallocate all students by setting their room_occupancy status to 'Inactive'
4. Keep all students registered in the system

---

## Method 2: Using SQL Directly

### Option A: Execute SQL File via MySQL

```bash
mysql -u root -p hostel_management < /home/prajwal/Programs/Hostel/unallocate_students.sql
```

Or without password (if set to empty):
```bash
mysql -u root hostel_management < /home/prajwal/Programs/Hostel/unallocate_students.sql
```

### Option B: Execute SQL in MySQL Interactive Shell

```bash
# Start MySQL
mysql -u root -p

# Then in MySQL shell:
USE hostel_management;

-- View current allocations
SELECT 
    ro.id,
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

-- Verify all students are still registered
SELECT u.full_name, s.roll_number, u.role
FROM users u
JOIN students s ON u.id = s.user_id
WHERE u.role = 'student' AND u.is_active = TRUE;
```

---

## Method 3: Using the Flask Web App (If Running)

1. Start the Flask application:
```bash
cd /home/prajwal/Programs/Hostel
python app.py
```

2. Login as Admin (username: `admin`, password: `admin123`)

3. Go to **Admin → Rooms**

4. For each room with students:
   - Click on the room
   - Click the **Remove** button for each student
   - This will set their status to 'Inactive'

---

## What Gets Unallocated?

- ✅ Room allocations are marked as 'Inactive'
- ✅ Students remain fully registered in the system
- ✅ Student profiles, documents, and history remain intact
- ✅ Fee records are not affected

## What Happens to Students?

- Their `room_occupancy.status` changes from 'Active' to 'Inactive'
- They are no longer shown as occupants in room details
- They can be reallocated to rooms later
- Their login and account remains active
- All their data (fees, complaints, visits) remains intact

---

## Verification

After unallocation, verify by running:

```sql
-- Check that all room allocations are now inactive
SELECT COUNT(*) as active_allocations FROM room_occupancy WHERE status = 'Active';
-- Should return: 0

-- Check that all students are still registered
SELECT COUNT(*) as total_students FROM users WHERE role = 'student';
-- Should return: (number of students you had before)
```

---

## Troubleshooting

### MySQL Connection Error

If you get "Can't connect to server":

1. Check if MySQL is running:
```bash
sudo systemctl status mysql
```

2. Start MySQL:
```bash
sudo systemctl start mysql
```

3. Check MySQL is listening:
```bash
sudo netstat -tlnp | grep mysql
```

### Permission Denied

If you get permission errors, ensure:
1. Your MySQL user has proper permissions
2. You're in the correct directory
3. Run with proper permissions (use `sudo` if needed)

---

## Summary

All three methods achieve the same result:
- **Python Script**: Interactive, user-friendly with confirmations
- **SQL Direct**: Fast, direct database manipulation
- **Web App**: Visual interface, one-by-one control

Choose the method that best fits your workflow!

