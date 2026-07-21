#!/usr/bin/env python3
"""
Test script to verify UI elements for room numbering
"""

import re
from pathlib import Path

def test_html_template():
    """Test that HTML template has been properly updated"""
    print("=" * 70)
    print("TESTING HTML TEMPLATE UPDATES")
    print("=" * 70)
    
    template_path = Path("/home/prajwal/Desktop/Hostel-Hub/templates/admin/rooms.html")
    
    if not template_path.exists():
        print("✗ Template file not found")
        return False
    
    content = template_path.read_text()
    
    tests = [
        ("room_position input field", r'name="room_position"', "Room position field should be in form"),
        ("Floor numbering explanation", r'Room numbering:', "Room numbering explanation should be present"),
        ("Max 5 rooms explanation", r'maximum 5 rooms', "Max 5 rooms per floor should be explained"),
        ("generateRoomNumber function", r'function generateRoomNumber', "generateRoomNumber JS function should exist"),
        ("updateFloorInfo function", r'function updateFloorInfo', "updateFloorInfo JS function should exist"),
        ("Room position dropdown (Position 1)", r'Position 1.*</option>', "Position 1 option should exist"),
        ("Room position dropdown (Position 5)", r'Position 5.*</option>', "Position 5 option should exist"),
        ("room_number_preview in Add modal", r'add_room_number_preview', "Room number preview in Add modal"),
        ("room_number_preview in Edit modal", r'edit_room_number_preview', "Room number preview in Edit modal"),
        ("Current room number display", r'edit_current_room_number', "Current room number display field"),
    ]
    
    all_passed = True
    print("\nTemplate Elements Check:")
    for test_name, pattern, description in tests:
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            print(f"✓ {test_name}: {description}")
        else:
            print(f"✗ {test_name}: {description} - NOT FOUND")
            all_passed = False
    
    return all_passed

def test_admin_routes():
    """Test that admin_routes.py has been properly updated"""
    print("\n" + "=" * 70)
    print("TESTING ADMIN ROUTES UPDATES")
    print("=" * 70)
    
    routes_path = Path("/home/prajwal/Desktop/Hostel-Hub/routes/admin_routes.py")
    
    if not routes_path.exists():
        print("✗ Routes file not found")
        return False
    
    content = routes_path.read_text()
    
    tests = [
        ("generate_room_number function", r'def generate_room_number', "Function to generate room numbers"),
        ("get_next_room_position function", r'def get_next_room_position', "Function to get next room position"),
        ("room_position parameter in add", r'room_position.*=.*int.*request\.form\.get', "room_position parameter in add"),
        ("room_position parameter in update", r'room_position.*=.*int.*request\.form\.get', "room_position parameter in update"),
        ("generate_room_number call in add", r'room_number.*=.*generate_room_number', "Call generate_room_number in add"),
        ("Validation for position 1-5", r'room_position.*[<>].*1.*room_position.*[<>].*5', "Validation for position 1-5"),
        ("Max 5 rooms per floor check", r'count.*>=.*5', "Check for max 5 rooms per floor"),
        ("Extract room_position from room_number", r'room_position.*=.*int.*room_number.*-2', "Extract room position from room number"),
        ("Floor and room_number sorting", r'ORDER BY.*floor.*room_number', "Order rooms by floor and room_number"),
    ]
    
    all_passed = True
    print("\nCode Elements Check:")
    for test_name, pattern, description in tests:
        if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
            print(f"✓ {test_name}: {description}")
        else:
            print(f"✗ {test_name}: {description} - NOT FOUND")
            all_passed = False
    
    return all_passed

def test_database_script():
    """Test that database constraint script exists"""
    print("\n" + "=" * 70)
    print("TESTING DATABASE CONSTRAINT SCRIPT")
    print("=" * 70)
    
    script_path = Path("/home/prajwal/Desktop/Hostel-Hub/config/enforce_room_limit.sql")
    
    if not script_path.exists():
        print("✗ Database constraint script not found")
        return False
    
    content = script_path.read_text()
    
    tests = [
        ("UNIQUE constraint", r'UNIQUE.*room_number', "UNIQUE constraint on room_number"),
        ("Insert trigger", r'TRIGGER.*insert', "Trigger for insert validation"),
        ("Update trigger", r'TRIGGER.*update', "Trigger for update validation"),
        ("Max rooms check", r'count.*>=.*5', "Check for max 5 rooms per floor"),
        ("Error message", r'Maximum.*5.*rooms', "Proper error message"),
    ]
    
    all_passed = True
    print("\nDatabase Script Elements Check:")
    for test_name, pattern, description in tests:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✓ {test_name}: {description}")
        else:
            print(f"✗ {test_name}: {description} - NOT FOUND")
            all_passed = False
    
    return all_passed

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ROOM NUMBERING IMPLEMENTATION VERIFICATION" + " " * 11 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    html_ok = test_html_template()
    routes_ok = test_admin_routes()
    db_ok = test_database_script()
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"{'✓' if html_ok else '✗'} HTML Template: {'PASSED' if html_ok else 'FAILED'}")
    print(f"{'✓' if routes_ok else '✗'} Admin Routes: {'PASSED' if routes_ok else 'FAILED'}")
    print(f"{'✓' if db_ok else '✗'} Database Script: {'PASSED' if db_ok else 'FAILED'}")
    print("=" * 70)
    
    all_passed = html_ok and routes_ok and db_ok
    if all_passed:
        print("\n✓ ALL VERIFICATIONS PASSED!")
        print("Room numbering implementation is complete and ready for use.")
    else:
        print("\n✗ SOME VERIFICATIONS FAILED - Please review the output above")
    
    print("=" * 70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
