# ⚡ Gender Separation Feature - Quick Setup

## What This Does ✅

Prevents boys and girls from sharing the same room:
- ✅ First student's gender determines room type (Boys/Girls)
- ✅ Can't allocate opposite gender to rooms with existing students
- ✅ Automatic enforcement with clear error messages

## Quick Setup (5 minutes)

### Step 1: Update Database

**For Fresh Installation:**
```bash
mysql -u root < config/database.sql
```

**For Existing Installation:**
```bash
mysql -u root < config/migrations/002_add_gender_restriction.sql
```

### Step 2: Restart Flask
```bash
python3 app.py
```

### Step 3: Test It
1. Login as admin: `admin` / `admin123`
2. Go to: Admin Dashboard → Rooms → Allocate Room
3. Try allocating:
   - **Male student** to empty room → Works, room becomes "Boys"
   - **Another male** to same room → Works
   - **Female student** to same room → ❌ Shows error!

## How It Works

```
Empty Room "101"
     ↓
Allocate: prajwal (Male)
     ↓
Room becomes "Boys Only"
     ↓
Allocate: rajdeep (Male) ✓ Works
     ↓
Allocate: rutuja (Female) ❌ Error!
          "Cannot allocate room! This room currently has Boys students..."
```

## Test Data

| Username | Gender | Expected Room Type |
|----------|--------|-------------------|
| prajwal | Male | Boys |
| rajdeep | Male | Boys |
| rutuja | Female | Girls |
| admin | Male | (can't be allocated) |
| warden | Male | (can't be allocated) |

## Verify Setup

```bash
# Check gender column exists
mysql -u root -e "DESCRIBE hostel_management.users;" | grep gender

# Check sample data
mysql -u root -e "SELECT username, gender FROM hostel_management.users WHERE role='student';"
```

Should show:
```
admin   | Male
prajwal | Male
rajdeep | Male
rutuja  | Female
warden  | Male
```

## What Changed

### Database
- `users` table: Added `gender` column
- `rooms` table: Added `gender_occupancy` column

### Backend
- `admin_routes.py`: Updated `allocate_room()` function
  - Validates student gender
  - Checks room's current gender
  - Prevents mixed allocations

## Error Messages

| Situation | Error |
|-----------|-------|
| Student without gender | "Student gender information is missing..." |
| Opposite gender allocation | "Cannot allocate room! This room currently has Boys students..." |
| Room at capacity | "This room is at full capacity..." |
| Student already allocated | "Student already has an active room allocation..." |

## Files Modified

1. ✅ `config/database.sql` - Added gender columns
2. ✅ `routes/admin_routes.py` - Added gender validation
3. ✅ `config/migrations/002_add_gender_restriction.sql` - Migration script
4. ✅ `GENDER_SEPARATION_GUIDE.md` - Full documentation

## Troubleshooting

**Q: Student profile doesn't show gender?**
A: Update database manually:
```bash
mysql -u root -e "UPDATE hostel_management.users SET gender='Female' WHERE username='rutuja';"
```

**Q: Old rooms show "Mixed" gender?**
A: Auto-assigns when first student added, or manually:
```bash
mysql -u root -e "UPDATE hostel_management.rooms SET gender_occupancy='Boys' WHERE room_number='101';"
```

**Q: Changes not showing?**
A: Clear browser cache and restart Flask:
```bash
python3 app.py
```

## Next Steps

1. ✅ Apply database migration
2. ✅ Restart Flask
3. ✅ Test with sample data
4. ✅ Update existing student profiles with gender
5. ✅ Configure existing rooms' gender if needed

## 🎉 Done!

The gender separation feature is now active. Boys and girls will be kept in separate rooms automatically.

**Read:** `GENDER_SEPARATION_GUIDE.md` for detailed information
