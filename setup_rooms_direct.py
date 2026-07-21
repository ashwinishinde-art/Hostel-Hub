#!/usr/bin/env python3
"""
Direct room setup - connects with MySQL socket auth
"""

import MySQLdb
import sys

print("\n" + "="*80)
print("HOSTEL ROOM SETUP - DELETE ALL & CREATE NEW")
print("="*80 + "\n")

try:
    # Connect using Unix socket (auth_socket method)
    conn = MySQLdb.connect(
        unix_socket='/var/run/mysqld/mysqld.sock',
        user='root',
        db='hostel_management'
    )
    
    cursor = conn.cursor()
    print("✓ Connected to MySQL database\n")
    
    # Delete existing
    print("🗑️  Deleting existing rooms and allocations...")
    cursor.execute("DELETE FROM room_occupancy")
    print("   ✓ Deleted room occupancy records")
    
    cursor.execute("DELETE FROM rooms")
    print("   ✓ Deleted existing rooms")
    
    conn.commit()
    
    # Create new rooms
    print("\n➕ Creating 15 new rooms (5 per floor)...\n")
    
    rooms_data = [
        # Floor 1
        (1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        # Floor 2
        (2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        # Floor 3
        (3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
        (3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
        (3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        (3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
    ]
    
    for floor, room_num, room_type, capacity, rent, amenities in rooms_data:
        cursor.execute("""
            INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
        """, (floor, room_num, room_type, capacity, rent, amenities))
        print(f"   ✓ Room {room_num} (Floor {floor}) - {room_type}, Cap: {capacity}")
    
    conn.commit()
    
    # Verify
    print("\n" + "="*80)
    print("✅ VERIFICATION - SETUP COMPLETE")
    print("="*80 + "\n")
    
    cursor.execute("SELECT floor, COUNT(*) as count FROM rooms GROUP BY floor ORDER BY floor")
    results = cursor.fetchall()
    
    print("Rooms per floor:")
    for floor, count in results:
        print(f"  Floor {floor}: {count} rooms")
    
    cursor.execute("SELECT COUNT(*) as total FROM rooms")
    total_count = cursor.fetchone()[0]
    
    print(f"\n  📊 Total: {total_count} rooms ✓")
    
    # Show all rooms
    print("\n" + "="*80)
    print("COMPLETE ROOM LISTING")
    print("="*80 + "\n")
    
    cursor.execute("""
        SELECT room_number, floor, room_type, capacity, rent 
        FROM rooms 
        ORDER BY floor, room_number
    """)
    
    rooms_list = cursor.fetchall()
    for room_num, floor, rtype, cap, rent in rooms_list:
        print(f"Room {room_num:>3} | Floor {floor} | {rtype:20} | Cap: {cap} | ₹{rent:>7,.2f}")
    
    print("\n" + "="*80)
    print("✅ SUCCESS!")
    print("   • 15 rooms created")
    print("   • Rooms: 101-105, 201-205, 301-305")
    print("   • All rooms available for allocation")
    print("="*80 + "\n")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
