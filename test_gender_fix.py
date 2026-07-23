#!/usr/bin/env python
"""Test script to verify gender update and retrieval"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from config.database_mock import db

# Test 1: Check if gender is in the database
cursor = db.connection.cursor()

# Query all students and check their gender
cursor.execute("SELECT id, full_name, gender FROM users WHERE role = 'student'")
students = cursor.fetchall()

print("Current students in database:")
print("=" * 60)
for student in students:
    gender = student.get('gender') if isinstance(student, dict) else None
    full_name = student.get('full_name') if isinstance(student, dict) else None
    user_id = student.get('id') if isinstance(student, dict) else None
    print(f"ID: {user_id}, Name: {full_name}, Gender: {gender}")

print("\n" + "=" * 60)

# Test 2: Try to update gender for student ID 2
print("\nTesting gender update for student ID 2...")
cursor.execute("""
    UPDATE users SET gender = %s WHERE id = %s
""", ("Female", 2))
db.connection.commit()

# Verify the update
cursor.execute("SELECT id, full_name, gender FROM users WHERE id = %s", (2,))
result = cursor.fetchone()
if result:
    gender = result.get('gender') if isinstance(result, dict) else None
    print(f"After update - ID: {result.get('id')}, Gender: {gender}")
    print(f"✓ Update successful!" if gender == "Female" else f"✗ Update failed! Gender is still: {gender}")
else:
    print("✗ Could not find student after update")

cursor.close()
