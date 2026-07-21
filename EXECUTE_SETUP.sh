#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║              HOSTEL ROOM SETUP - DELETE & CREATE ROOMS                     ║"
echo "║                   Rooms: 101-105, 201-205, 301-305                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Ensure we're in the right directory
cd /home/prajwal/Desktop/Hostel-Hub

echo "⚙️  Step 1: Verifying MySQL is running..."
systemctl status mysql > /dev/null 2>&1 || (echo "Starting MySQL..."; systemctl start mysql 2>&1)

sleep 2

echo "✓ MySQL is running"
echo ""

echo "📋 Step 2: Running setup script..."
echo ""

# Create temporary SQL file
cat > /tmp/hostel_setup.sql << 'SQLEOF'
USE hostel_management;

DELETE FROM room_occupancy;
DELETE FROM rooms;

INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES
(1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk', TRUE),
(3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk', TRUE),
(3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE),
(3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk', TRUE);

SELECT CONCAT('✅ Setup Complete - ', COUNT(*), ' rooms created') FROM rooms;
SELECT CONCAT('Floor ', floor, ': ', COUNT(*), ' rooms') FROM rooms GROUP BY floor ORDER BY floor;
SQLEOF

# Execute with sudo
echo ""
sudo mysql hostel_management < /tmp/hostel_setup.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║  ✅ SUCCESS! All 15 rooms have been created"                              ║"
    echo "║  • Floor 1: Rooms 101-105"                                                 ║"
    echo "║  • Floor 2: Rooms 201-205"                                                 ║"
    echo "║  • Floor 3: Rooms 301-305"                                                 ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
else
    echo ""
    echo "❌ Setup failed. Please check MySQL access."
fi

# Cleanup
rm -f /tmp/hostel_setup.sql

