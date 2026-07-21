-- Fix Room Numbers to Follow Floor-Based Numbering Pattern
-- Ensures rooms are numbered: 101-105, 201-205, 301-305, etc.
-- Where first digit(s) = floor, last 2 digits = room position (01-05)

USE hostel_management;

-- Step 1: Delete existing room allocations and rooms
DELETE FROM room_occupancy;
DELETE FROM rooms;

-- Step 2: Create rooms with CORRECT floor-based numbering
-- FLOOR 1: Rooms 101, 102, 103, 104, 105
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 2: Rooms 201, 202, 203, 204, 205
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 3: Rooms 301, 302, 303, 304, 305
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- Step 3: Verification Query
SELECT 
    CONCAT('✅ Rooms Created Successfully!') AS status,
    COUNT(*) AS total_rooms,
    COUNT(DISTINCT floor) AS total_floors
FROM rooms;

-- Show breakdown by floor
SELECT 
    CONCAT('Floor ', floor) AS floor_info,
    COUNT(*) AS room_count,
    GROUP_CONCAT(room_number ORDER BY room_number) AS rooms
FROM rooms
GROUP BY floor
ORDER BY floor;

-- Show all rooms with details
SELECT 
    room_number,
    CONCAT('Floor ', floor) AS floor_info,
    room_type,
    capacity,
    CONCAT('₹', FORMAT(rent, 2)) AS rent
FROM rooms
ORDER BY floor, room_number;
