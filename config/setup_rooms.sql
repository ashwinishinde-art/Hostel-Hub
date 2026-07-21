-- ============================================================================
-- HOSTEL ROOM SETUP SCRIPT
-- Delete all existing rooms and create new ones with proper numbering
-- Rooms: 101-105, 201-205, 301-305 (5 rooms per floor, 3 floors)
-- ============================================================================

USE hostel_management;

-- Step 1: Delete room occupancy records first (due to foreign key constraint)
DELETE FROM room_occupancy;
SELECT 'Deleted all room occupancy records' AS status;

-- Step 2: Delete all existing rooms
DELETE FROM rooms;
SELECT 'Deleted all existing rooms' AS status;

-- Step 3: Create new rooms with proper floor-based numbering
-- FLOOR 1: Rooms 101-105
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 2: Rooms 201-205
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 3: Rooms 301-305
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- Step 4: Verification - Display rooms per floor
SELECT 
    '=== VERIFICATION ===' AS info,
    floor,
    COUNT(*) as room_count,
    GROUP_CONCAT(room_number ORDER BY room_number) as rooms
FROM rooms
GROUP BY floor
ORDER BY floor;

-- Final summary
SELECT 
    'SUMMARY' as section,
    COUNT(*) as total_rooms,
    COUNT(DISTINCT floor) as total_floors,
    MIN(room_number) as first_room,
    MAX(room_number) as last_room
FROM rooms;

-- Display all rooms
SELECT 
    '=== ALL ROOMS ===' AS info,
    CONCAT('Room ', room_number) as room,
    CONCAT('Floor ', floor) as floor_info,
    room_type,
    CONCAT('Cap: ', capacity) as capacity,
    CONCAT('₹', FORMAT(rent, 2)) as rent_per_month
FROM rooms
ORDER BY floor, room_number;

-- ============================================================================
-- SETUP COMPLETE
-- ✓ 15 rooms created (3 floors × 5 rooms each)
-- ✓ Rooms: 101-105, 201-205, 301-305
-- ✓ All rooms available for allocation
-- ============================================================================
