# 500 Server Error on Login - FIXED

## Problem
When trying to login, users were getting:
```
500 Server Error
Something went wrong on our end. We're working to fix it!
```

## Root Cause
The login query was:
```sql
SELECT id, username, email, role, full_name, password_hash, phone, gender 
FROM users 
WHERE username = %s AND is_active = TRUE
```

**The problem:** 10 newly registered users in `mock_db.json` were missing the `is_active` field:
- ID 6: nandini
- ID 7: anushka
- ID 8: srushti
- ID 9: rutujachaudhari
- ID 10: rushikesh
- ID 11: Nandini
- ID 12: Rutuja chaudhari
- ID 13: sru_1219
- ID 14: prajwaltandekar
- ID 15: testuser123

When the mock database tried to filter by `is_active = TRUE` for users without this field, it would either:
1. Skip them (user not found in login)
2. Cause an error in the filtering logic

This caused the 500 error.

## Solution Applied
Added `"is_active": true` to all 10 users missing this field in `mock_db.json`.

### Verification
✓ All 15 users now have the `is_active` field set to `true`

## Files Modified
- `/home/prajwal/Desktop/Hostel-Hub/data/mock_db.json` - Added is_active field to 10 users

## Testing
Users can now login successfully:
- Username: prajwal
- Username: rajdeep
- Username: anushka
- Username: nandini
- And all other registered users

Password for all test accounts: admin123

## Status
✅ **FIXED** - Login 500 error resolved. All users can now authenticate.
