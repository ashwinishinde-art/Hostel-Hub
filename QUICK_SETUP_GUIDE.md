# Quick Setup Guide - Delete & Create Rooms

## ⚡ Quick Start (2 Minutes)

### Option 1: SQL Script (Fastest)

```bash
cd /home/prajwal/Desktop/Hostel-Hub
mysql -u root -p hostel_management < config/setup_rooms.sql
```

**Done!** 15 rooms created instantly.

### Option 2: Python Script

```bash
cd /home/prajwal/Desktop/Hostel-Hub
python setup_hostel_rooms.py
# Type: YES
```

---

## 📋 What Will Be Created

### Before:
- ❌ Any existing rooms deleted
- ❌ All room allocations removed

### After:
- ✅ 15 new rooms created
- ✅ Organized as: 101-105, 201-205, 301-305
- ✅ 5 rooms per floor (3 floors total)
- ✅ All ready for student allocation

---

## 🎯 Room Breakdown

```
FLOOR 1: 101, 102, 103, 104, 105
FLOOR 2: 201, 202, 203, 204, 205
FLOOR 3: 301, 302, 303, 304, 305
```

### Room Types & Rent:
- **101, 201, 301**: Single Deluxe (₹7,000) - Capacity 1
- **102, 202, 302**: Double Sharing (₹5,000) - Capacity 2
- **103, 203, 303**: Double Sharing (₹5,000) - Capacity 2
- **104, 204, 304**: Triple Sharing (₹4,000) - Capacity 3
- **105, 205, 305**: Quad Sharing (₹3,500) - Capacity 4

---

## ✅ Verify Setup

### In Terminal:
```bash
mysql -u root -p -e "SELECT COUNT(*) FROM hostel_management.rooms;"
# Should show: 15
```

### In Admin Dashboard:
1. Login: `http://localhost:5000/login`
   - Username: `admin`
   - Password: `admin123`
2. Go to: Admin → Room Management
3. Should see all 15 rooms listed

---

## ⚠️ Important Notes

**What Gets Deleted:**
- ❌ All existing rooms
- ❌ All room allocations (students removed from rooms)

**What's NOT Affected:**
- ✅ Student accounts (remain intact)
- ✅ Student data (safe)
- ✅ Complaints
- ✅ Visitor requests
- ✅ Fees
- ✅ Notices

---

## 🚀 Next Steps

After setup:
1. **Allocate rooms to students**: Admin → Allocate Room
2. **Verify in dashboard**: See all rooms available
3. **Test with student login**: View allocated room

---

## 🆘 Troubleshooting

**MySQL not running?**
```bash
sudo systemctl start mysql
```

**Connection refused?**
```bash
mysql -u root -p
# Enter password to test connection
```

**Database doesn't exist?**
```bash
mysql -u root -p < config/database.sql
```

---

## 📁 Files Available

| File | Purpose |
|------|---------|
| `config/setup_rooms.sql` | SQL script (fastest) |
| `setup_hostel_rooms.py` | Python script (interactive) |
| `SETUP_ROOMS_INSTRUCTIONS.md` | Detailed instructions |
| `QUICK_SETUP_GUIDE.md` | This file |

---

## ✨ Summary

✅ **Simple**: One command setup
✅ **Fast**: Creates 15 rooms instantly
✅ **Clean**: Numbered as 101-105, 201-205, 301-305
✅ **Ready**: All rooms available for allocation

🎉 **Setup Complete!**
