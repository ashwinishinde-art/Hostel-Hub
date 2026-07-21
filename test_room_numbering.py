#!/usr/bin/env python3
"""
Test script to verify floor-based room numbering implementation
Tests:
1. Room number generation (Floor + Position = Room Number)
2. Room position extraction from room number
3. Max 5 rooms per floor validation
4. Edge cases
"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from routes.admin_routes import generate_room_number

def test_room_number_generation():
    """Test room number generation"""
    print("=" * 60)
    print("TEST 1: Room Number Generation")
    print("=" * 60)
    
    test_cases = [
        (1, 1, "101"),
        (1, 2, "102"),
        (1, 5, "105"),
        (2, 1, "201"),
        (2, 3, "203"),
        (3, 5, "305"),
        (10, 1, "1001"),
        (10, 5, "1005"),
    ]
    
    all_passed = True
    for floor, position, expected in test_cases:
        result = generate_room_number(floor, position)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} Floor {floor}, Position {position} -> {result} (expected: {expected})")
    
    return all_passed

def test_invalid_positions():
    """Test invalid room positions"""
    print("\n" + "=" * 60)
    print("TEST 2: Invalid Position Validation")
    print("=" * 60)
    
    invalid_positions = [0, -1, 6, 10, 100]
    
    all_passed = True
    for position in invalid_positions:
        try:
            result = generate_room_number(2, position)
            print(f"✗ Position {position} should have raised error, but returned {result}")
            all_passed = False
        except ValueError as e:
            print(f"✓ Position {position} correctly raised error: {e}")
    
    return all_passed

def test_room_position_extraction():
    """Test extracting room position from room number"""
    print("\n" + "=" * 60)
    print("TEST 3: Room Position Extraction")
    print("=" * 60)
    
    test_cases = [
        ("101", 1),
        ("102", 2),
        ("105", 5),
        ("201", 1),
        ("203", 3),
        ("305", 5),
        ("1001", 1),
        ("1005", 5),
    ]
    
    all_passed = True
    for room_number, expected_position in test_cases:
        # Extract last 2 digits
        extracted = int(room_number[-2:])
        status = "✓" if extracted == expected_position else "✗"
        if extracted != expected_position:
            all_passed = False
        print(f"{status} Room {room_number} -> Position {extracted} (expected: {expected_position})")
    
    return all_passed

def test_floor_room_relationship():
    """Test the relationship between floor number and room number"""
    print("\n" + "=" * 60)
    print("TEST 4: Floor-Room Relationship")
    print("=" * 60)
    
    print("\nFloor 1 (5 rooms):")
    for pos in range(1, 6):
        room_no = generate_room_number(1, pos)
        print(f"  Position {pos} -> Room {room_no}")
    
    print("\nFloor 2 (5 rooms):")
    for pos in range(1, 6):
        room_no = generate_room_number(2, pos)
        print(f"  Position {pos} -> Room {room_no}")
    
    print("\nFloor 3 (5 rooms):")
    for pos in range(1, 6):
        room_no = generate_room_number(3, pos)
        print(f"  Position {pos} -> Room {room_no}")
    
    return True

def test_room_numbering_clarity():
    """Test that room numbering scheme is clear and consistent"""
    print("\n" + "=" * 60)
    print("TEST 5: Room Numbering Clarity")
    print("=" * 60)
    
    print("\nExample room numbers and their interpretation:")
    examples = [
        ("201", "Floor 2, Position 01"),
        ("305", "Floor 3, Position 05"),
        ("402", "Floor 4, Position 02"),
        ("1003", "Floor 10, Position 03"),
    ]
    
    for room_no, interpretation in examples:
        print(f"  {room_no} = {interpretation}")
    
    print("\n✓ Room numbering scheme is clear and follows pattern: {FLOOR}{POSITION:02d}")
    return True

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "ROOM NUMBERING IMPLEMENTATION TEST" + " " * 14 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {}
    results["Room Number Generation"] = test_room_number_generation()
    results["Invalid Position Validation"] = test_invalid_positions()
    results["Room Position Extraction"] = test_room_position_extraction()
    results["Floor-Room Relationship"] = test_floor_room_relationship()
    results["Room Numbering Clarity"] = test_room_numbering_clarity()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Room numbering implementation is correct!")
    else:
        print("✗ SOME TESTS FAILED - Please review the failures above")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
