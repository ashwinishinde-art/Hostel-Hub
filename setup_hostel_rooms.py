#!/usr/bin/env python3
"""
Script to delete all existing rooms and create new ones with proper floor-based numbering.
Creates 5 rooms on each floor with numbering: 101-105, 201-205, 301-305, etc.
"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

try:
    from config.database import db
except:
    print("❌ Error: Could not connect to database. Please ensure MySQL is running.")
    sys.exit(1)

def create_hostel_rooms():
    """
    Delete all existing rooms and create new ones with proper numbering
    """
    cursor = db.connection.cursor()
    
    try:
        print("\n" + "="*80)
        print("HOSTEL ROOM SETUP - DELETE AND CREATE")
        print("="*80 + "\n")
        
        # Step 1: Get current room count
        cursor.execute("SELECT COUNT(*) as count FROM rooms")
        result = cursor.fetchone()
        current_count = result.get('count', 0) if result else 0
        
        print(f"📊 Current rooms in database: {current_count}")
        
        if current_count > 0:
            print("\n🗑️  Deleting all existing rooms...")
            
            # Delete room occupancy first (foreign key constraint)
            cursor.execute("DELETE FROM room_occupancy")
            print(f"   ✓ Deleted all room occupancy records")
            
            # Delete all rooms
            cursor.execute("DELETE FROM rooms")
            print(f"   ✓ Deleted all {current_count} rooms")
            
            db.connection.commit()
            print("   ✓ Database committed")
        
        # Step 2: Create new rooms
        print("\n➕ Creating new rooms with floor-based numbering...\n")
        
        rooms_data = [
            # Floor 1: 5 rooms
            (1, "101", 1, "Single Deluxe", 1, 7000.00, "WiFi, AC, Private Bathroom, Study Desk"),
            (1, "102", 1, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (1, "103", 1, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (1, "104", 1, "Triple Sharing", 3, 4000.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
            (1, "105", 1, "Quad Sharing", 4, 3500.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
            
            # Floor 2: 5 rooms
            (2, "201", 2, "Single Deluxe", 1, 7000.00, "WiFi, AC, Private Bathroom, Study Desk"),
            (2, "202", 2, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (2, "203", 2, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (2, "204", 2, "Triple Sharing", 3, 4000.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
            (2, "205", 2, "Quad Sharing", 4, 3500.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
            
            # Floor 3: 5 rooms
            (3, "301", 3, "Single Deluxe", 1, 7000.00, "WiFi, AC, Private Bathroom, Study Desk"),
            (3, "302", 3, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (3, "303", 3, "Double Sharing", 2, 5000.00, "WiFi, AC, Cupboard, Study Desk"),
            (3, "304", 3, "Triple Sharing", 3, 4000.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
            (3, "305", 3, "Quad Sharing", 4, 3500.00, "WiFi, Ceiling Fan, Cupboard, Study Desk"),
        ]
        
        rooms_created = 0
        for floor, room_number, position, room_type, capacity, rent, amenities in rooms_data:
            cursor.execute("""
                INSERT INTO rooms (floor, room_number, room_type, capacity, rent, amenities, is_available)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            """, (floor, room_number, room_type, capacity, rent, amenities))
            
            print(f"   ✓ Created Room {room_number} (Floor {floor}, Position {position}) - {room_type}, Capacity: {capacity}")
            rooms_created += 1
        
        db.connection.commit()
        print(f"\n✅ Successfully created {rooms_created} rooms!")
        
        # Step 3: Verify
        print("\n📋 Verification - Rooms per floor:\n")
        
        cursor.execute("""
            SELECT floor, COUNT(*) as count FROM rooms GROUP BY floor ORDER BY floor
        """)
        
        results = cursor.fetchall()
        for row in results:
            floor = row.get('floor') if isinstance(row, dict) else row[0]
            count = row.get('count', 0) if isinstance(row, dict) else row[1]
            print(f"   Floor {floor}: {count} rooms")
        
        cursor.execute("SELECT COUNT(*) as total FROM rooms")
        total_result = cursor.fetchone()
        total_rooms = total_result.get('total', 0) if total_result else 0
        
        print(f"\n   📊 Total rooms: {total_rooms}")
        
        # Step 4: Show room listing
        print("\n📍 Complete Room Listing:\n")
        
        cursor.execute("""
            SELECT room_number, floor, room_type, capacity, rent 
            FROM rooms 
            ORDER BY floor, room_number
        """)
        
        rooms_list = cursor.fetchall()
        for room in rooms_list:
            room_number = room.get('room_number') if isinstance(room, dict) else room[0]
            floor = room.get('floor') if isinstance(room, dict) else room[1]
            room_type = room.get('room_type') if isinstance(room, dict) else room[2]
            capacity = room.get('capacity') if isinstance(room, dict) else room[3]
            rent = room.get('rent') if isinstance(room, dict) else room[4]
            
            print(f"   Room {room_number} | Floor {floor} | {room_type:20} | Cap: {capacity} | Rent: ₹{rent:.2f}")
        
        print("\n" + "="*80)
        print("✅ HOSTEL ROOM SETUP COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nSummary:")
        print(f"  • Deleted previous rooms (if any)")
        print(f"  • Created {rooms_created} new rooms")
        print(f"  • Rooms: 101-105, 201-205, 301-305")
        print(f"  • Floors: 3 (with 5 rooms each)")
        print(f"  • Numbering: {room_number} = Floor {floor}, Position (last 2 digits)")
        print("\n" + "="*80 + "\n")
        
        cursor.close()
        return True
        
    except Exception as e:
        db.connection.rollback()
        print(f"\n❌ Error: {str(e)}")
        print(f"\nDetails: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        cursor.close()
        return False

def main():
    print("\n╔" + "="*78 + "╗")
    print("║" + " "*20 + "HOSTEL ROOM SETUP SCRIPT" + " "*34 + "║")
    print("║" + " "*15 + "Delete All Rooms & Create New Ones" + " "*29 + "║")
    print("╚" + "="*78 + "╝")
    
    print("\n⚠️  WARNING: This script will:")
    print("   1. DELETE all existing rooms")
    print("   2. DELETE all room occupancy records")
    print("   3. CREATE 15 new rooms (5 per floor × 3 floors)")
    print("\nRooms will be numbered:")
    print("   Floor 1: 101, 102, 103, 104, 105")
    print("   Floor 2: 201, 202, 203, 204, 205")
    print("   Floor 3: 301, 302, 303, 304, 305")
    
    confirm = input("\n❓ Continue? Type 'YES' to confirm: ").strip().upper()
    
    if confirm != "YES":
        print("\n❌ Operation cancelled.")
        return 1
    
    success = create_hostel_rooms()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
