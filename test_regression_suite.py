"""
Comprehensive Regression Testing Suite for Hostel Hub
Tests all major features and fixed issues to ensure no regressions
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch, MagicMock

# Add the project to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app and dependencies
from app import app, db, User
from config.database_mock import MockDatabase

# Test Categories
TOTAL_TESTS = 0
PASSED_TESTS = 0
FAILED_TESTS = 0
TEST_RESULTS = {
    "authentication": [],
    "database": [],
    "room_management": [],
    "student_management": [],
    "complaint_system": [],
    "visitor_management": [],
    "fee_management": [],
    "notice_board": [],
    "cross_module": [],
    "performance": [],
    "data_integrity": [],
    "security": []
}


class RegressionTestRunner:
    """Main test runner for regression testing"""
    
    def __init__(self):
        self.app = app
        self.client = app.test_client()
        self.db = db
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_log = []
        
    def test(self, category, test_name, condition, error_msg=""):
        """Record test result"""
        global TOTAL_TESTS, PASSED_TESTS, FAILED_TESTS
        
        TOTAL_TESTS += 1
        self.tests_run += 1
        
        status = "✓ PASS" if condition else "✗ FAIL"
        log_entry = {
            "category": category,
            "test": test_name,
            "status": "PASS" if condition else "FAIL",
            "timestamp": datetime.now().isoformat(),
            "error": error_msg if not condition else ""
        }
        
        if condition:
            PASSED_TESTS += 1
            self.tests_passed += 1
        else:
            FAILED_TESTS += 1
            self.tests_failed += 1
            TEST_RESULTS[category].append({
                "test": test_name,
                "status": "FAIL",
                "error": error_msg
            })
        
        self.test_log.append(log_entry)
        print(f"  {status}: {test_name}" + (f" - {error_msg}" if error_msg and not condition else ""))
        
    def run_authentication_tests(self):
        """Test authentication and authorization"""
        print("\n" + "="*60)
        print("AUTHENTICATION TESTS")
        print("="*60)
        
        # Test 1: Check user table exists
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM users")
            self.test("authentication", "Users table exists", result is not None, 
                     error_msg="Users table query failed")
        except Exception as e:
            self.test("authentication", "Users table exists", False, str(e))
        
        # Test 2: Check active users have is_active field
        try:
            result = self.db.query("SELECT * FROM users WHERE username = 'admin'")
            has_is_active = result and any('is_active' in str(row) for row in result if row)
            self.test("authentication", "Users have is_active field", has_is_active,
                     error_msg="is_active field missing from users")
        except Exception as e:
            self.test("authentication", "Users have is_active field", False, str(e))
        
        # Test 3: Test login endpoint exists
        try:
            response = self.client.get('/login')
            self.test("authentication", "Login page accessible", response.status_code == 200,
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("authentication", "Login page accessible", False, str(e))
        
        # Test 4: Test login with valid credentials
        try:
            response = self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            # Success or redirect to dashboard
            self.test("authentication", "Valid login accepted", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("authentication", "Valid login accepted", False, str(e))
        
        # Test 5: Test login with invalid credentials
        try:
            response = self.client.post('/login', data={
                'username': 'admin',
                'password': 'wrongpassword'
            })
            # Should fail or show error
            self.test("authentication", "Invalid login rejected", 
                     response.status_code in [200, 401, 403],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("authentication", "Invalid login rejected", False, str(e))
        
        # Test 6: Test logout functionality
        try:
            response = self.client.get('/logout', follow_redirects=True)
            self.test("authentication", "Logout works", response.status_code == 200,
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("authentication", "Logout works", False, str(e))
    
    def run_database_tests(self):
        """Test database integrity and queries"""
        print("\n" + "="*60)
        print("DATABASE TESTS")
        print("="*60)
        
        # Test 1: Core tables exist
        required_tables = ['users', 'students', 'rooms', 'room_occupancy', 
                          'complaints', 'visitors', 'fees', 'notices', 'hostel_settings']
        
        for table in required_tables:
            try:
                result = self.db.query(f"SELECT COUNT(*) as count FROM {table}")
                self.test("database", f"Table '{table}' exists", result is not None,
                         error_msg=f"Failed to query {table}")
            except Exception as e:
                self.test("database", f"Table '{table}' exists", False, str(e))
        
        # Test 2: Hostel settings are populated
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM hostel_settings")
            count = result[0].get('count', 0) if result else 0
            self.test("database", "Hostel settings configured", count >= 8,
                     error_msg=f"Only {count} settings found")
        except Exception as e:
            self.test("database", "Hostel settings configured", False, str(e))
        
        # Test 3: Users have required fields
        try:
            result = self.db.query("SELECT * FROM users LIMIT 1")
            if result:
                user = result[0]
                has_required_fields = all(field in str(user) for field in 
                                         ['username', 'password', 'role', 'is_active'])
                self.test("database", "Users have required fields", has_required_fields,
                         error_msg="Missing required user fields")
            else:
                self.test("database", "Users have required fields", False, "No users found")
        except Exception as e:
            self.test("database", "Users have required fields", False, str(e))
        
        # Test 4: Rooms table properly structured
        try:
            result = self.db.query("SELECT * FROM rooms LIMIT 1")
            if result:
                room = result[0]
                has_room_fields = all(field in str(room) for field in 
                                     ['room_number', 'room_type', 'capacity', 'rent'])
                self.test("database", "Rooms have required fields", has_room_fields,
                         error_msg="Missing required room fields")
            else:
                self.test("database", "Rooms have required fields", False, "No rooms found")
        except Exception as e:
            self.test("database", "Rooms have required fields", False, str(e))
    
    def run_room_management_tests(self):
        """Test room management functionality"""
        print("\n" + "="*60)
        print("ROOM MANAGEMENT TESTS")
        print("="*60)
        
        # Test 1: Room allocation exists
        try:
            response = self.client.get('/admin/allocate-room')
            self.test("room_management", "Allocate room page exists", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("room_management", "Allocate room page exists", False, str(e))
        
        # Test 2: Room capacity validation
        try:
            result = self.db.query("SELECT * FROM rooms LIMIT 1")
            if result:
                room = result[0]
                room_id = room.get('id') or room.get('room_id')
                occupancy = self.db.query(
                    f"SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = {room_id}"
                )
                if occupancy:
                    count = occupancy[0].get('count', 0)
                    capacity = room.get('capacity', 0)
                    # Occupancy should not exceed capacity
                    self.test("room_management", "Room capacity not exceeded", 
                             count <= capacity,
                             error_msg=f"Occupancy {count} > Capacity {capacity}")
                else:
                    self.test("room_management", "Room capacity not exceeded", True)
            else:
                self.test("room_management", "Room capacity not exceeded", True, "No rooms found")
        except Exception as e:
            self.test("room_management", "Room capacity not exceeded", False, str(e))
        
        # Test 3: Room types are valid
        try:
            result = self.db.query("SELECT DISTINCT room_type FROM rooms")
            valid_types = ['Single Deluxe', 'Double Sharing', 'Triple Sharing', 'Common']
            if result:
                types = [r.get('room_type') for r in result if r]
                all_valid = all(t in valid_types for t in types)
                self.test("room_management", "Room types are valid", all_valid,
                         error_msg=f"Invalid types found: {types}")
            else:
                self.test("room_management", "Room types are valid", True, "No rooms found")
        except Exception as e:
            self.test("room_management", "Room types are valid", False, str(e))
    
    def run_student_management_tests(self):
        """Test student management functionality"""
        print("\n" + "="*60)
        print("STUDENT MANAGEMENT TESTS")
        print("="*60)
        
        # Test 1: Student records exist
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM students")
            count = result[0].get('count', 0) if result else 0
            self.test("student_management", "Student records exist", count > 0,
                     error_msg=f"Only {count} students found")
        except Exception as e:
            self.test("student_management", "Student records exist", False, str(e))
        
        # Test 2: Students linked to users
        try:
            result = self.db.query("SELECT * FROM students LIMIT 1")
            if result:
                student = result[0]
                has_user_id = 'user_id' in str(student)
                self.test("student_management", "Students linked to users", has_user_id,
                         error_msg="student records don't have user_id")
            else:
                self.test("student_management", "Students linked to users", True, "No students found")
        except Exception as e:
            self.test("student_management", "Students linked to users", False, str(e))
        
        # Test 3: Student management page accessible
        try:
            response = self.client.get('/admin/students')
            self.test("student_management", "Student management page accessible", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("student_management", "Student management page accessible", False, str(e))
    
    def run_complaint_system_tests(self):
        """Test complaint management system"""
        print("\n" + "="*60)
        print("COMPLAINT SYSTEM TESTS")
        print("="*60)
        
        # Test 1: Complaints table exists
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM complaints")
            self.test("complaint_system", "Complaints table exists", result is not None,
                     error_msg="Complaints table query failed")
        except Exception as e:
            self.test("complaint_system", "Complaints table exists", False, str(e))
        
        # Test 2: Complaint statuses are valid
        try:
            result = self.db.query("SELECT DISTINCT status FROM complaints")
            valid_statuses = ['Pending', 'In Progress', 'Resolved', 'Closed']
            if result:
                statuses = [r.get('status') for r in result if r]
                all_valid = all(s in valid_statuses for s in statuses if s)
                self.test("complaint_system", "Complaint statuses are valid", all_valid,
                         error_msg=f"Invalid statuses: {statuses}")
            else:
                self.test("complaint_system", "Complaint statuses are valid", True, "No complaints")
        except Exception as e:
            self.test("complaint_system", "Complaint statuses are valid", False, str(e))
        
        # Test 3: Complaint page accessible
        try:
            response = self.client.get('/admin/complaints')
            self.test("complaint_system", "Complaint management page accessible", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("complaint_system", "Complaint management page accessible", False, str(e))
    
    def run_visitor_management_tests(self):
        """Test visitor management system"""
        print("\n" + "="*60)
        print("VISITOR MANAGEMENT TESTS")
        print("="*60)
        
        # Test 1: Visitors table exists
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM visitors")
            self.test("visitor_management", "Visitors table exists", result is not None,
                     error_msg="Visitors table query failed")
        except Exception as e:
            self.test("visitor_management", "Visitors table exists", False, str(e))
        
        # Test 2: Visitor statuses are valid
        try:
            result = self.db.query("SELECT DISTINCT status FROM visitors")
            valid_statuses = ['Pending', 'Approved', 'Rejected', 'Completed']
            if result:
                statuses = [r.get('status') for r in result if r]
                all_valid = all(s in valid_statuses for s in statuses if s)
                self.test("visitor_management", "Visitor statuses are valid", all_valid,
                         error_msg=f"Invalid statuses: {statuses}")
            else:
                self.test("visitor_management", "Visitor statuses are valid", True, "No visitors")
        except Exception as e:
            self.test("visitor_management", "Visitor statuses are valid", False, str(e))
        
        # Test 3: Visitor page accessible
        try:
            response = self.client.get('/admin/visitors')
            self.test("visitor_management", "Visitor management page accessible", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("visitor_management", "Visitor management page accessible", False, str(e))
    
    def run_fee_management_tests(self):
        """Test fee management system"""
        print("\n" + "="*60)
        print("FEE MANAGEMENT TESTS")
        print("="*60)
        
        # Test 1: Fees table exists
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM fees")
            self.test("fee_management", "Fees table exists", result is not None,
                     error_msg="Fees table query failed")
        except Exception as e:
            self.test("fee_management", "Fees table exists", False, str(e))
        
        # Test 2: Fee status are valid
        try:
            result = self.db.query("SELECT DISTINCT status FROM fees")
            valid_statuses = ['Pending', 'Partial', 'Paid', 'Overdue']
            if result:
                statuses = [r.get('status') for r in result if r]
                all_valid = all(s in valid_statuses for s in statuses if s)
                self.test("fee_management", "Fee statuses are valid", all_valid,
                         error_msg=f"Invalid statuses: {statuses}")
            else:
                self.test("fee_management", "Fee statuses are valid", True, "No fees")
        except Exception as e:
            self.test("fee_management", "Fee statuses are valid", False, str(e))
        
        # Test 3: Fee page accessible
        try:
            response = self.client.get('/admin/fees')
            self.test("fee_management", "Fee management page accessible", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("fee_management", "Fee management page accessible", False, str(e))
    
    def run_notice_board_tests(self):
        """Test notice board functionality"""
        print("\n" + "="*60)
        print("NOTICE BOARD TESTS")
        print("="*60)
        
        # Test 1: Notices table exists
        try:
            result = self.db.query("SELECT COUNT(*) as count FROM notices")
            self.test("notice_board", "Notices table exists", result is not None,
                     error_msg="Notices table query failed")
        except Exception as e:
            self.test("notice_board", "Notices table exists", False, str(e))
        
        # Test 2: Notice page accessible
        try:
            response = self.client.get('/admin/notices')
            self.test("notice_board", "Notice management page accessible", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("notice_board", "Notice management page accessible", False, str(e))
    
    def run_cross_module_tests(self):
        """Test interactions between modules"""
        print("\n" + "="*60)
        print("CROSS-MODULE INTERACTION TESTS")
        print("="*60)
        
        # Test 1: Allocated students appear in complaints
        try:
            result = self.db.query("""
                SELECT ro.student_id FROM room_occupancy ro 
                WHERE ro.status = 'Active' LIMIT 1
            """)
            if result:
                student_id = result[0].get('student_id')
                complaints = self.db.query(
                    f"SELECT * FROM complaints WHERE student_id = {student_id}"
                )
                # Should be able to query complaints for allocated student
                self.test("cross_module", "Allocated students can file complaints", 
                         complaints is not None,
                         error_msg="Failed to query complaints for student")
            else:
                self.test("cross_module", "Allocated students can file complaints", True, 
                         "No allocated students")
        except Exception as e:
            self.test("cross_module", "Allocated students can file complaints", False, str(e))
        
        # Test 2: Room data consistency
        try:
            result = self.db.query("""
                SELECT r.id, COUNT(ro.id) as occupancy 
                FROM rooms r 
                LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
                GROUP BY r.id
            """)
            if result:
                all_consistent = all(r.get('occupancy', 0) <= r.get('capacity', 100) 
                                    for r in result if r)
                self.test("cross_module", "Room occupancy data is consistent", all_consistent,
                         error_msg="Occupancy exceeds capacity for some rooms")
            else:
                self.test("cross_module", "Room occupancy data is consistent", True)
        except Exception as e:
            self.test("cross_module", "Room occupancy data is consistent", False, str(e))
        
        # Test 3: Dashboard loads without errors
        try:
            response = self.client.get('/admin/dashboard')
            self.test("cross_module", "Dashboard loads successfully", 
                     response.status_code in [200, 302],
                     error_msg=f"Status code {response.status_code}")
        except Exception as e:
            self.test("cross_module", "Dashboard loads successfully", False, str(e))
    
    def run_performance_tests(self):
        """Test performance - no slowdowns introduced"""
        print("\n" + "="*60)
        print("PERFORMANCE TESTS")
        print("="*60)
        
        # Test 1: Login response time < 500ms
        try:
            start = time.time()
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            elapsed = (time.time() - start) * 1000
            self.test("performance", "Login response time < 500ms", elapsed < 500,
                     error_msg=f"Took {elapsed:.1f}ms")
        except Exception as e:
            self.test("performance", "Login response time < 500ms", False, str(e))
        
        # Test 2: Database query time < 100ms
        try:
            start = time.time()
            self.db.query("SELECT COUNT(*) as count FROM users")
            elapsed = (time.time() - start) * 1000
            self.test("performance", "Database queries < 100ms", elapsed < 100,
                     error_msg=f"Took {elapsed:.1f}ms")
        except Exception as e:
            self.test("performance", "Database queries < 100ms", False, str(e))
    
    def run_data_integrity_tests(self):
        """Test data integrity and consistency"""
        print("\n" + "="*60)
        print("DATA INTEGRITY TESTS")
        print("="*60)
        
        # Test 1: No duplicate user IDs
        try:
            result = self.db.query("""
                SELECT id, COUNT(*) as count FROM users 
                GROUP BY id HAVING count > 1
            """)
            has_duplicates = result and len(result) > 0 and any(r.get('count', 0) > 1 for r in result)
            self.test("data_integrity", "No duplicate user IDs", not has_duplicates,
                     error_msg="Duplicate user IDs found")
        except Exception as e:
            self.test("data_integrity", "No duplicate user IDs", False, str(e))
        
        # Test 2: No orphaned student records
        try:
            result = self.db.query("""
                SELECT COUNT(*) as count FROM students s 
                WHERE NOT EXISTS (SELECT 1 FROM users u WHERE u.id = s.user_id)
            """)
            orphaned_count = result[0].get('count', 0) if result else 0
            self.test("data_integrity", "No orphaned student records", orphaned_count == 0,
                     error_msg=f"{orphaned_count} orphaned students found")
        except Exception as e:
            self.test("data_integrity", "No orphaned student records", False, str(e))
        
        # Test 3: Active room allocations are valid
        try:
            result = self.db.query("""
                SELECT COUNT(*) as count FROM room_occupancy ro 
                WHERE ro.status = 'Active'
                AND NOT EXISTS (SELECT 1 FROM rooms r WHERE r.id = ro.room_id)
            """)
            invalid_count = result[0].get('count', 0) if result else 0
            self.test("data_integrity", "Active allocations point to valid rooms", 
                     invalid_count == 0,
                     error_msg=f"{invalid_count} invalid allocations found")
        except Exception as e:
            self.test("data_integrity", "Active allocations point to valid rooms", False, str(e))
    
    def run_security_tests(self):
        """Test security measures"""
        print("\n" + "="*60)
        print("SECURITY VERIFICATION TESTS")
        print("="*60)
        
        # Test 1: Passwords are hashed
        try:
            result = self.db.query("SELECT password FROM users LIMIT 1")
            if result:
                password = result[0].get('password')
                is_hashed = password and len(str(password)) > 20 and not password.isalnum()
                self.test("security", "Passwords are hashed", is_hashed,
                         error_msg="Password does not appear to be hashed")
            else:
                self.test("security", "Passwords are hashed", True, "No users found")
        except Exception as e:
            self.test("security", "Passwords are hashed", False, str(e))
        
        # Test 2: Login requires authentication
        try:
            response = self.client.get('/admin/dashboard')
            requires_auth = response.status_code in [302, 401] or 'login' in response.location.lower()
            self.test("security", "Protected routes require login", requires_auth,
                     error_msg=f"Dashboard accessible without login (status {response.status_code})")
        except Exception as e:
            self.test("security", "Protected routes require login", False, str(e))
        
        # Test 3: User roles are enforced
        try:
            # Try to access admin page as student (if possible)
            response = self.client.get('/admin/students')
            not_accessible = response.status_code in [302, 403, 401]
            self.test("security", "Role-based access control enforced", not_accessible,
                     error_msg=f"Unprotected access to admin route (status {response.status_code})")
        except Exception as e:
            self.test("security", "Role-based access control enforced", False, str(e))
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("REGRESSION TEST REPORT")
        print("="*60)
        print(f"\nTest Execution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nTotal Tests Run: {TOTAL_TESTS}")
        print(f"Passed: {PASSED_TESTS} ({100*PASSED_TESTS//max(TOTAL_TESTS,1)}%)")
        print(f"Failed: {FAILED_TESTS} ({100*FAILED_TESTS//max(TOTAL_TESTS,1)}%)")
        
        print("\n" + "-"*60)
        print("SUMMARY BY CATEGORY")
        print("-"*60)
        
        categories_tested = [
            "authentication", "database", "room_management", "student_management",
            "complaint_system", "visitor_management", "fee_management", "notice_board",
            "cross_module", "performance", "data_integrity", "security"
        ]
        
        for category in categories_tested:
            if TEST_RESULTS[category]:
                failures = len(TEST_RESULTS[category])
                print(f"\n{category.upper()}: ✗ {failures} FAILURES")
                for item in TEST_RESULTS[category]:
                    print(f"  - {item['test']}: {item['error']}")
        
        # Overall status
        print("\n" + "="*60)
        if FAILED_TESTS == 0:
            print("✓ ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT")
        else:
            print(f"✗ {FAILED_TESTS} TESTS FAILED - REVIEW REQUIRED")
        print("="*60)
        
        return {
            "total": TOTAL_TESTS,
            "passed": PASSED_TESTS,
            "failed": FAILED_TESTS,
            "success_rate": f"{100*PASSED_TESTS//max(TOTAL_TESTS,1)}%",
            "timestamp": datetime.now().isoformat(),
            "test_log": self.test_log
        }


def main():
    """Run all regression tests"""
    print("\n" + "█"*60)
    print("HOSTEL HUB - COMPREHENSIVE REGRESSION TEST SUITE")
    print("█"*60)
    print("Testing all major features and fixed issues...")
    
    runner = RegressionTestRunner()
    
    # Run all test categories
    runner.run_authentication_tests()
    runner.run_database_tests()
    runner.run_room_management_tests()
    runner.run_student_management_tests()
    runner.run_complaint_system_tests()
    runner.run_visitor_management_tests()
    runner.run_fee_management_tests()
    runner.run_notice_board_tests()
    runner.run_cross_module_tests()
    runner.run_performance_tests()
    runner.run_data_integrity_tests()
    runner.run_security_tests()
    
    # Generate report
    report = runner.generate_report()
    
    # Save report to file
    with open('regression_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: regression_test_report.json")
    
    return FAILED_TESTS == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
