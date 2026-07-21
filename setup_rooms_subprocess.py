#!/usr/bin/env python3
"""
Setup rooms by directly executing MySQL commands via subprocess
"""

import subprocess
import sys

print("\n" + "="*80)
print("HOSTEL ROOM SETUP - DELETE ALL & CREATE NEW ROOMS")
print("="*80 + "\n")

# SQL to execute
sql_commands = """
-- Delete existing rooms and allocations
DELETE FROM room_occupancy;
DELETE FROM rooms;

-- FLOOR 1: Create 5 rooms
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 2: Create 5 rooms
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- FLOOR 3: Create 5 rooms
INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

-- Verification
SELECT 'Rooms Created Successfully!' AS status;
SELECT floor, COUNT(*) as room_count FROM rooms GROUP BY floor ORDER BY floor;
SELECT CONCAT('Total: ', COUNT(*), ' rooms') as total_count FROM rooms;
"""

try:
    print("Executing setup commands...\n")
    
    # Use sudo to run mysql
    process = subprocess.Popen(
        ['sudo', 'mysql', 'hostel_management'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=sql_commands)
    
    if process.returncode != 0:
        # Try without sudo
        print("Trying without sudo...")
        process = subprocess.Popen(
            ['mysql', 'hostel_management', '-u', 'root'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=sql_commands)
        
        if process.returncode != 0:
            print(f"stderr: {stderr}")
            raise Exception("Failed to execute MySQL commands")
    
    print("Output from MySQL:")
    print(stdout)
    
    if stderr and "error" in stderr.lower():
        print(f"\nWarnings/Errors:\n{stderr}")
    
    print("\n" + "="*80)
    print("✅ SUCCESS! Room setup completed")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
