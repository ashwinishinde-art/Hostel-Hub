#!/usr/bin/env python3
"""
Direct setup script - use the app's database config
Run this from Flask context or standalone with proper DB setup
"""

import sys
import os

sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')
os.chdir('/home/prajwal/Desktop/Hostel-Hub')

from flask import Flask
from config.database import db

# Create minimal Flask app for context
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'

with app.app_context():
    try:
        conn = db.connect()
        if not conn:
            raise Exception("Could not establish database connection")
        
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("HOSTEL ROOM SETUP - DELETE ALL & CREATE NEW")
        print("="*80 + "\n")
        
        # Delete
        print("🗑️  Deleting existing rooms and allocations...")
        cursor.execute("DELETE FROM room_occupancy")
        cursor.execute("DELETE FROM rooms")
        conn.commit()
        print("   ✓ Cleaned up database\n")
        
        # Create rooms
        print("➕ Creating 15 new rooms (5 per floor)...\n")
        
        rooms = [
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
        
        for floor, room_num, room_type, capacity, rent, amenities in rooms:
            cursor.execute(
                "INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available) VALUES (%s, %s, %s, %s, %s, %s, TRUE)",
                (floor, room_num, room_type, capacity, rent, amenities)
            )
            print(f"   ✓ Room {room_num} (Floor {floor})")
        
        conn.commit()
        
        # Verify
        print("\n" + "="*80)
        print("✅ VERIFICATION")
        print("="*80 + "\n")
        
        cursor.execute("SELECT floor, COUNT(*) as count FROM rooms GROUP BY floor ORDER BY floor")
        results = cursor.fetchall()
        
        print("Rooms by floor:")
        for row in results:
            if isinstance(row, dict):
                print(f"  Floor {row['floor']}: {row['count']} rooms")
            else:
                print(f"  Floor {row[0]}: {row[1]} rooms")
        
        cursor.execute("SELECT COUNT(*) FROM rooms")
        total = cursor.fetchone()
        total_count = total[0] if isinstance(total, tuple) else total.get('COUNT(*)')
        
        print(f"\n  📊 Total: {total_count} rooms\n")
        
        # Show all
        print("="*80)
        print("COMPLETE ROOM LISTING")
        print("="*80 + "\n")
        
        cursor.execute("SELECT room_number, floor, room_type, capacity, rent FROM rooms ORDER BY floor, room_number")
        all_rooms = cursor.fetchall()
        
        for room in all_rooms:
            if isinstance(room, dict):
                print(f"Room {room['room_number']:>3} | Floor {room['floor']} | {room['room_type']:20} | Cap: {room['capacity']} | ₹{room['rent']:>7,.2f}")
            else:
                print(f"Room {room[0]:>3} | Floor {room[1]} | {room[2]:20} | Cap: {room[3]} | ₹{room[4]:>7,.2f}")
        
        print("\n" + "="*80)
        print("✅ SUCCESS!")
        print("   • 15 rooms created")
        print("   • Rooms: 101-105, 201-205, 301-305")
        print("   • All ready for allocation")
        print("="*80 + "\n")
        
        cursor.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
