#!/usr/bin/env python3
"""
Fix room numbering to follow floor-based pattern
Rooms: 101-105, 201-205, 301-305
"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from flask import Flask
from config.database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

with app.app_context():
    try:
        conn = db.connect()
        if not conn:
            raise Exception("Could not connect to database")
        
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("FIXING ROOM NUMBERING - FLOOR-BASED PATTERN")
        print("="*80 + "\n")
        
        # Delete existing rooms
        print("Deleting existing rooms and allocations...")
        cursor.execute("DELETE FROM room_occupancy")
        cursor.execute("DELETE FROM rooms")
        conn.commit()
        print("✓ Database cleaned\n")
        
        # Create correct rooms
        print("Creating rooms with correct floor-based numbering:\n")
        
        rooms = [
            # Floor 1: 101-105
            (1, '101', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
            (1, '102', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (1, '103', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (1, '104', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
            (1, '105', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
            # Floor 2: 201-205
            (2, '201', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
            (2, '202', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (2, '203', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (2, '204', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
            (2, '205', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
            # Floor 3: 301-305
            (3, '301', 'Single Deluxe', 1, 7000.00, 'WiFi, AC, Private Bathroom, Study Desk'),
            (3, '302', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (3, '303', 'Double Sharing', 2, 5000.00, 'WiFi, AC, Cupboard, Study Desk'),
            (3, '304', 'Triple Sharing', 3, 4000.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
            (3, '305', 'Quad Sharing', 4, 3500.00, 'WiFi, Ceiling Fan, Cupboard, Study Desk'),
        ]
        
        for floor, room_num, room_type, capacity, rent, amenities in rooms:
            cursor.execute("""
                INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            """, (floor, room_num, room_type, capacity, rent, amenities))
            print(f"  ✓ Room {room_num} | Floor {floor} | {room_type} | Cap: {capacity}")
        
        conn.commit()
        
        # Verify
        print("\n" + "="*80)
        print("VERIFICATION")
        print("="*80 + "\n")
        
        cursor.execute("SELECT floor, COUNT(*) as count FROM rooms GROUP BY floor ORDER BY floor")
        results = cursor.fetchall()
        
        print("Rooms per floor:")
        for row in results:
            floor = row[0] if isinstance(row, tuple) else row.get('floor')
            count = row[1] if isinstance(row, tuple) else row.get('count')
            print(f"  Floor {floor}: {count} rooms")
        
        cursor.execute("SELECT COUNT(*) FROM rooms")
        total = cursor.fetchone()
        total_count = total[0] if isinstance(total, tuple) else total.get('COUNT(*)')
        
        print(f"\n  📊 Total: {total_count} rooms\n")
        
        # List all rooms
        print("="*80)
        print("COMPLETE ROOM LISTING")
        print("="*80 + "\n")
        
        cursor.execute("""
            SELECT room_number, floor, room_type, capacity, rent 
            FROM rooms 
            ORDER BY floor, room_number
        """)
        
        all_rooms = cursor.fetchall()
        print(f"{'Room':<6} | {'Floor':<6} | {'Type':<20} | {'Cap':<3} | {'Rent':<10}")
        print("-" * 80)
        
        for room in all_rooms:
            if isinstance(room, tuple):
                room_num, floor, rtype, cap, rent = room
            else:
                room_num = room.get('room_number')
                floor = room.get('floor')
                rtype = room.get('room_type')
                cap = room.get('capacity')
                rent = room.get('rent')
            
            print(f"{room_num:<6} | {floor:<6} | {rtype:<20} | {cap:<3} | ₹{rent:>7,.0f}")
        
        print("\n" + "="*80)
        print("✅ ROOM NUMBERING FIXED!")
        print("="*80)
        print("\nFloor-based numbering applied:")
        print("  ✅ Floor 1: Rooms 101, 102, 103, 104, 105")
        print("  ✅ Floor 2: Rooms 201, 202, 203, 204, 205")
        print("  ✅ Floor 3: Rooms 301, 302, 303, 304, 305")
        print("\nRoom numbering pattern:")
        print("  • First digit(s) = Floor number")
        print("  • Last 2 digits = Room position (01-05)")
        print("  • Example: 201 = Floor 2, Position 01")
        print("\n" + "="*80 + "\n")
        
        cursor.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
