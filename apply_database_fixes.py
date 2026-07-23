"""
Database Schema Fixes for Hostel Hub
Addresses missing fields in complaints and students tables
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database_mock import db, DB_FILE

def fix_complaint_schema():
    """
    Fix Issue #1: Add missing status field to complaints table
    """
    print("\n" + "="*70)
    print("FIX #1: Adding status field to complaints table")
    print("="*70)
    
    data = db.data
    complaints = data.get('complaints', [])
    
    fixes_needed = 0
    for complaint in complaints:
        # Check for missing fields
        if 'status' not in complaint:
            complaint['status'] = 'pending'
            fixes_needed += 1
        
        if 'created_at' not in complaint:
            complaint['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if 'resolution_notes' not in complaint:
            complaint['resolution_notes'] = ''
    
    data['complaints'] = complaints
    db.data = data
    
    print(f"✓ Fixed {fixes_needed} complaints with missing status")
    print(f"✓ Added created_at and resolution_notes fields")
    
    # Display fixed structure
    if complaints:
        print(f"\nSample complaint after fix:")
        print(json.dumps(complaints[0], indent=2))
    
    return True

def fix_student_schema():
    """
    Fix Issue #2: Add missing roll_number field to students table
    """
    print("\n" + "="*70)
    print("FIX #2: Adding roll_number field to students table")
    print("="*70)
    
    data = db.data
    students = data.get('students', [])
    
    fixes_needed = 0
    departments = {'CSE': 'Computer Science', 'ECE': 'Electronics', 'MECH': 'Mechanical', 'CIVIL': 'Civil'}
    
    for idx, student in enumerate(students):
        if 'roll_number' not in student:
            # Generate roll number based on department and batch
            dept = student.get('department', 'CSE')
            batch = student.get('batch', '2024')
            student_num = str(idx + 1).zfill(3)
            student['roll_number'] = f"{dept}{batch[2:]}{student_num}"
            fixes_needed += 1
    
    data['students'] = students
    db.data = data
    
    print(f"✓ Fixed {fixes_needed} students with missing roll_number")
    print(f"✓ Generated roll numbers based on department and batch")
    
    # Display fixed structure
    if students:
        print(f"\nSample student after fix:")
        print(json.dumps(students[0], indent=2))
    
    return True

def document_authorization_issue():
    """
    Document Issue #3: Admin access to student profile
    """
    print("\n" + "="*70)
    print("ISSUE #3: Admin Access to Student Profile")
    print("="*70)
    print("\nCurrent Behavior:")
    print("  - Admin users can access /student/profile endpoint (returns 200)")
    print("  - This may be intentional for administrative oversight")
    print("\nRecommended Actions:")
    print("  1. If NO admin access needed:")
    print("     - Add @student_required decorator to /student/profile route")
    print("     - Location: routes/student_routes.py, around line 50")
    print("\n  2. If YES admin access needed:")
    print("     - Document this as intentional admin capability")
    print("     - Add audit logging for admin profile access")
    print("     - Add data access controls if needed")
    print("\nDecision Required: Please review business requirements")
    print("="*70 + "\n")

def save_fixes():
    """
    Save all fixes to database
    """
    print("\nSaving fixes to database...")
    success = db.save_data(db.data)
    
    if success:
        print("✓ All fixes saved successfully to mock_db.json")
        return True
    else:
        print("❌ Error saving fixes")
        return False

def main():
    """
    Apply all database schema fixes
    """
    print("\n" + "="*70)
    print("HOSTEL HUB DATABASE SCHEMA FIXES")
    print("="*70)
    print(f"\nDatabase File: {DB_FILE}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Apply fixes
        fix_complaint_schema()
        fix_student_schema()
        document_authorization_issue()
        
        # Save to database
        if save_fixes():
            print("\n" + "="*70)
            print("✓ ALL FIXES APPLIED SUCCESSFULLY")
            print("="*70)
            print("\nNext Steps:")
            print("1. Review Issue #3 (Admin access) and implement as needed")
            print("2. Run comprehensive_test_suite.py to verify fixes")
            print("3. Check COMPREHENSIVE_TEST_REPORT.md for details")
            print("="*70 + "\n")
            return 0
        else:
            print("\n❌ Error saving fixes")
            return 1
    
    except Exception as e:
        print(f"\n❌ Error applying fixes: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
