# Hostel Room Setup Instructions

## Overview
This document explains how to delete all existing rooms and create new ones with the proper floor-based numbering system.

## Room Structure
After setup, you'll have:
- **Floor 1**: Rooms 101, 102, 103, 104, 105
- **Floor 2**: Rooms 201, 202, 203, 204, 205
- **Floor 3**: Rooms 301, 302, 303, 304, 305

**Total**: 15 rooms (5 per floor × 3 floors)

## Method 1: Using SQL Script (Recommended)

### Step 1: Start MySQL Server
```bash
# On Linux/Mac
sudo systemctl start mysql

# Or if using MariaDB
sudo systemctl start mariadb

# Or start manually
mysql -u root -p
```

### Step 2: Execute Setup Script
```bash
cd /home/prajwal/Desktop/Hostel-Hub

# Run the SQL script
mysql -u root -p hostel_management < config/setup_rooms.sql
```

### Step 3: Enter MySQL Password
When prompted, enter your MySQL password.

### Expected Output
```
Deleted all room occupancy records
Deleted all existing rooms
+----------+---------+-----------+---------------------------+
| info     | floor   | room_count | rooms                     |
+----------+---------+-----------+---------------------------+
| === VERIFICATION === | 1 | 5 | 101,102,103,104,105 |
| === VERIFICATION === | 2 | 5 | 201,202,203,204,205 |
| === VERIFICATION === | 3 | 5 | 301,302,303,304,305 |
+----------+---------+-----------+---------------------------+

✓ 15 rooms created
✓ 3 floors configured
✓ All rooms available
```

## Method 2: Using Python Script

### Step 1: Start MySQL Server
Make sure MySQL is running.

### Step 2: Run Python Script
```bash
cd /home/prajwal/Desktop/Hostel-Hub
python setup_hostel_rooms.py
```

### Step 3: Confirm Setup
When prompted with "Continue? Type 'YES' to confirm:", type:
```
YES
```

### Step 4: Verify Results
The script will show:
- ✓ Deleted rooms
- ✓ Created new rooms
- ✓ Floor breakdown
- ✓ Complete room listing

## Room Details Created

### Floor 1 Rooms

| Room | Type | Capacity | Rent | Amenities |
|------|------|----------|------|-----------|
| 101 | Single Deluxe | 1 | ₹7,000 | WiFi, AC, Private Bathroom, Study Desk |
| 102 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 103 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 104 | Triple Sharing | 3 | ₹4,000 | WiFi, Ceiling Fan, Cupboard, Study Desk |
| 105 | Quad Sharing | 4 | ₹3,500 | WiFi, Ceiling Fan, Cupboard, Study Desk |

### Floor 2 Rooms

| Room | Type | Capacity | Rent | Amenities |
|------|------|----------|------|-----------|
| 201 | Single Deluxe | 1 | ₹7,000 | WiFi, AC, Private Bathroom, Study Desk |
| 202 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 203 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 204 | Triple Sharing | 3 | ₹4,000 | WiFi, Ceiling Fan, Cupboard, Study Desk |
| 205 | Quad Sharing | 4 | ₹3,500 | WiFi, Ceiling Fan, Cupboard, Study Desk |

### Floor 3 Rooms

| Room | Type | Capacity | Rent | Amenities |
|------|------|----------|------|-----------|
| 301 | Single Deluxe | 1 | ₹7,000 | WiFi, AC, Private Bathroom, Study Desk |
| 302 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 303 | Double Sharing | 2 | ₹5,000 | WiFi, AC, Cupboard, Study Desk |
| 304 | Triple Sharing | 3 | ₹4,000 | WiFi, Ceiling Fan, Cupboard, Study Desk |
| 305 | Quad Sharing | 4 | ₹3,500 | WiFi, Ceiling Fan, Cupboard, Study Desk |

## What Gets Deleted

### ⚠️ WARNING
The setup script will **permanently delete**:

1. **All room occupancy records** - Student-room allocations
2. **All existing rooms** - Previous room database records

**Note**: This does NOT affect:
- Student accounts
- Student data
- Complaints
- Visitor requests
- Fees
- Notices

## Verification

### After Running Script

#### Check Total Rooms
```bash
mysql -u root -p -e "SELECT COUNT(*) as total_rooms FROM hostel_management.rooms;"
```
Expected: `15`

#### Check Rooms per Floor
```bash
mysql -u root -p -e "
SELECT floor, COUNT(*) as room_count 
FROM hostel_management.rooms 
GROUP BY floor 
ORDER BY floor;
"
```

Expected output:
```
+-------+------------+
| floor | room_count |
+-------+------------+
|     1 |          5 |
|     2 |          5 |
|     3 |          5 |
+-------+------------+
```

#### List All Rooms
```bash
mysql -u root -p -e "
SELECT room_number, floor, room_type, capacity, rent 
FROM hostel_management.rooms 
ORDER BY floor, room_number;
"
```

## Manual Verification in Admin Dashboard

1. **Login as Admin**
   - URL: `http://localhost:5000/login`
   - Username: `admin`
   - Password: `admin123`

2. **Go to Room Management**
   - Click "Room Management" in sidebar
   - Or navigate to `/admin/rooms`

3. **Verify Rooms Display**
   - Should see 15 rooms total
   - Organized by floor (1, 2, 3)
   - Each showing numbering (101-105, 201-205, 301-305)
   - All rooms showing as "Available" (✓ Yes)

4. **Allocate Rooms to Students** (Optional)
   - Click "Allocate Room"
   - Select student and room
   - Verify room numbering works correctly

## Troubleshooting

### Issue: "Access denied for user"
**Solution**: Check MySQL password
```bash
mysql -u root -p mysql
# Enter your password
```

### Issue: "Database 'hostel_management' doesn't exist"
**Solution**: Run the database setup first
```bash
mysql -u root -p < config/database.sql
```

### Issue: "Can't connect to MySQL server"
**Solution**: Start MySQL service
```bash
# Linux
sudo systemctl start mysql

# Or check if it's already running
sudo systemctl status mysql
```

### Issue: Script says "Database connection failed"
**Solution**: Make sure MySQL is running before running the Python script

## Rollback (If Needed)

To undo this setup and restore previous rooms:

### From Backup (If You Have One)
```bash
mysql -u root -p hostel_management < path/to/backup.sql
```

### Manual Deletion (If You Want to Reset)
```bash
mysql -u root -p -e "
DELETE FROM room_occupancy;
DELETE FROM rooms;
" hostel_management
```

Then create rooms manually through the admin dashboard.

## Next Steps

After room setup:

1. **Allocate Rooms to Students**
   - Go to Admin → Allocate Room
   - Select student and room
   - Set check-in date
   - Confirm allocation

2. **Set Fee Amounts**
   - Update fee structure if needed
   - Default rents are set (see table above)

3. **Add to Hostel Settings**
   - Verify hostel name and contact
   - Check visitor hours
   - Review other settings

4. **Test the System**
   - Login as student
   - View allocated room
   - Submit a complaint
   - Request visitor entry

## Files Used

- **SQL Script**: `config/setup_rooms.sql` (Direct SQL execution)
- **Python Script**: `setup_hostel_rooms.py` (Python wrapper)

## Support

If you encounter any issues:

1. Check MySQL is running: `sudo systemctl status mysql`
2. Verify database exists: `mysql -e "SHOW DATABASES;"`
3. Verify database has tables: `mysql -e "SHOW TABLES FROM hostel_management;"`
4. Check log files for errors

---

**Status**: Ready to execute
**Version**: 1.0
**Last Updated**: July 20, 2026
