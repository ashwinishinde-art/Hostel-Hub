-- ============================================================
-- FIX ADMIN/WARDEN ROLES - Remove from Student List
-- ============================================================
-- This script corrects the roles for admin and warden users
-- so they don't appear in the Student List

USE hostel_management;

-- Step 1: Show current state
SELECT '-- BEFORE FIX --' as Status;
SELECT id, username, full_name, role FROM users ORDER BY username;

-- Step 2: Fix admin and warden roles
UPDATE users SET role = 'admin' WHERE username = 'admin';
UPDATE users SET role = 'warden' WHERE username = 'warden';

-- Step 3: Remove student records for admin/warden (they shouldn't have student records)
DELETE FROM students 
WHERE user_id IN (SELECT id FROM users WHERE role IN ('admin', 'warden'));

-- Step 4: Show final state
SELECT '-- AFTER FIX --' as Status;
SELECT id, username, full_name, role FROM users ORDER BY username;

-- Step 5: Show what student list will display
SELECT '-- STUDENT LIST (Admin Dashboard) --' as Status;
SELECT u.full_name, u.username, s.roll_number, s.branch, s.semester, r.room_number
FROM users u
JOIN students s ON u.id = s.user_id
LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
LEFT JOIN rooms r ON ro.room_id = r.id
WHERE u.role = 'student'
ORDER BY u.full_name;

-- Step 6: Verify results
SELECT 'VERIFICATION RESULTS:' as Status;
SELECT CONCAT('Total Admin/Warden: ', COUNT(*)) as Count 
FROM users WHERE role IN ('admin', 'warden');

SELECT CONCAT('Total Students: ', COUNT(*)) as Count 
FROM users WHERE role = 'student';

SELECT 'Fix Complete! Hard refresh browser (Ctrl+Shift+R) to see changes.' as Message;
