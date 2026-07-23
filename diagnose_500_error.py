#!/usr/bin/env python3
"""Complete diagnosis of 500 error"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from app import app, db
from routes import student_routes, admin_routes, warden_routes

print("=" * 70)
print("COMPREHENSIVE 500 ERROR DIAGNOSIS")
print("=" * 70)

# Test with test client
with app.test_client() as client:
    print("\n1️⃣  Testing Login...")
    try:
        response = client.post('/login', data={
            'username': 'prajwal',
            'password': 'admin123'
        })
        print(f"   ✓ Login status: {response.status_code}")
        if response.status_code != 302:
            print(f"   Warning: Expected 302, got {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n2️⃣  Testing Student Dashboard...")
    try:
        response = client.get('/student/dashboard')
        print(f"   ✓ Dashboard status: {response.status_code}")
        if response.status_code == 500:
            print("   ✗ 500 ERROR FOUND ON /student/dashboard")
            print(f"   Response: {response.data.decode()[:500]}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n3️⃣  Testing Admin Dashboard...")
    try:
        # Login as admin
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        response = client.get('/admin/dashboard')
        print(f"   ✓ Admin dashboard status: {response.status_code}")
        if response.status_code == 500:
            print("   ✗ 500 ERROR FOUND ON /admin/dashboard")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    print("\n4️⃣  Testing Database Queries...")
    try:
        cursor = db.connection.cursor()
        
        # Test student queries
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'student'")
        student_count = cursor.fetchone()
        print(f"   ✓ Student count query: {student_count}")
        
        # Test room queries
        cursor.execute("SELECT COUNT(*) as count FROM rooms")
        room_count = cursor.fetchone()
        print(f"   ✓ Room count query: {room_count}")
        
        # Test complaint queries
        cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'pending'")
        complaint_count = cursor.fetchone()
        print(f"   ✓ Complaint count query: {complaint_count}")
        
        cursor.close()
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n5️⃣  Testing Student Profile Load...")
    try:
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT s.*, u.phone, u.gender, u.email 
            FROM students s 
            JOIN users u ON s.user_id = u.id 
            WHERE u.id = %s
        """, (2,))
        profile = cursor.fetchone()
        if profile:
            print(f"   ✓ Student profile loaded: {profile.get('user_id')}")
        else:
            print(f"   ✗ No student profile found")
        cursor.close()
    except Exception as e:
        print(f"   ✗ Profile error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("✅ DIAGNOSIS COMPLETE")
print("=" * 70)
print("\nNext steps:")
print("1. If all tests passed, the issue is browser/network related")
print("2. Try clearing browser cache and cookies")
print("3. Try in a private/incognito window")
print("4. Check browser console for errors (F12)")
print("=" * 70 + "\n")
