-- SQL Script to Unallocate All Students from Rooms
-- This sets all active room allocations to 'Inactive' status
-- Students remain registered, only their room allocations are removed

USE hostel_management;

-- First, let's see what students are currently allocated
SELECT 'Current Student Allocations:' as info;
SELECT 
    ro.id,
    u.full_name,
    s.roll_number,
    r.room_number,
    ro.check_in_date,
    ro.status
FROM room_occupancy ro
JOIN users u ON ro.student_id = u.id
JOIN students s ON u.id = s.user_id
JOIN rooms r ON ro.room_id = r.id
WHERE ro.status = 'Active'
ORDER BY r.room_number;

-- Now update all active allocations to inactive
UPDATE room_occupancy 
SET status = 'Inactive'
WHERE status = 'Active';

-- Show the result
SELECT CONCAT('Successfully unallocated ', ROW_COUNT(), ' student(s) from rooms.') as result;

-- Verify all students are still registered
SELECT 'Registered Students (still active):' as info;
SELECT u.id, u.full_name, s.roll_number, u.role, u.is_active
FROM users u
JOIN students s ON u.id = s.user_id
WHERE u.role = 'student' AND u.is_active = TRUE
ORDER BY u.full_name;
