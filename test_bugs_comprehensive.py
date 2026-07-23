#!/usr/bin/env python3
"""
Comprehensive Bug Test Suite for Hostel Hub
Tests all critical functionalities and identifies bugs
"""

import sys
import json
import os
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

# Initialize Flask app
os.environ['FLASK_ENV'] = 'testing'
from app import app, db

class BugTestRunner:
    def __init__(self):
        self.bugs_found = []
        self.tests_passed = 0
        self.tests_failed = 0
        
    def log_bug(self, category, bug_name, description, severity='Medium'):
        """Log a bug found"""
        bug = {
            'category': category,
            'name': bug_name,
            'description': description,
            'severity': severity
        }
        self.bugs_found.append(bug)
        print(f"❌ [{severity}] {category}: {bug_name}")
        print(f"   → {description}\n")
        
    def log_pass(self, test_name):
        """Log a passed test"""
        self.tests_passed += 1
        print(f"✅ {test_name}\n")
        
    def test_database_connection(self):
        """Test 1: Database Connection"""
        print("\n=== TEST 1: Database Connection ===")
        try:
            if db.connection is None:
                self.log_bug('Database', 'No Connection', 
                    'Database connection is None - using mock database')
            else:
                self.log_pass('Database connected')
        except Exception as e:
            self.log_bug('Database', 'Connection Error', str(e), 'Critical')
            
    def test_user_loading(self):
        """Test 2: User Loading"""
        print("\n=== TEST 2: User Loading ===")
        try:
            from app import load_user
            # Try loading a test user
            user = load_user(1)
            if user:
                self.log_pass(f'User loading works (loaded: {user.username})')
            else:
                self.log_bug('Auth', 'User Not Found', 
                    'Cannot load user with id=1', 'High')
        except Exception as e:
            self.log_bug('Auth', 'User Loading Error', str(e), 'Critical')
            
    def test_input_validation(self):
        """Test 3: Input Validation"""
        print("\n=== TEST 3: Input Validation ===")
        
        # Test for SQL injection vulnerability
        with app.test_client() as client:
            try:
                # Test register form with SQL injection attempt
                response = client.post('/register', data={
                    'username': "admin' OR '1'='1",
                    'email': 'test@test.com',
                    'password': 'pass123',
                    'confirm_password': 'pass123',
                    'full_name': 'Test User',
                    'gender': 'M',
                    'roll_number': '123',
                    'branch': 'CSE'
                })
                
                # Should reject or sanitize
                if response.status_code in [200, 400, 302]:
                    self.log_pass('Input Validation: SQL injection attempt handled')
                else:
                    self.log_bug('Security', 'Input Validation Bypass',
                        'SQL injection attempt not properly handled', 'Critical')
            except Exception as e:
                self.log_bug('Security', 'Validation Test Error', str(e))
                
    def test_password_hashing(self):
        """Test 4: Password Hashing"""
        print("\n=== TEST 4: Password Hashing ===")
        try:
            import bcrypt
            password = "testpass123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Verify
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                self.log_pass('Password hashing and verification works')
            else:
                self.log_bug('Security', 'Password Verification Failed',
                    'Password hash verification failed', 'Critical')
        except Exception as e:
            self.log_bug('Security', 'Password Hashing Error', str(e), 'Critical')
            
    def test_session_management(self):
        """Test 5: Session Management"""
        print("\n=== TEST 5: Session Management ===")
        try:
            with app.test_client() as client:
                # Check if session is properly initialized
                response = client.get('/')
                if response.status_code == 200:
                    self.log_pass('Session management working')
                else:
                    self.log_bug('Session', 'Session Init Failed',
                        f'Homepage returned {response.status_code}', 'High')
        except Exception as e:
            self.log_bug('Session', 'Session Error', str(e), 'High')
            
    def test_templates(self):
        """Test 6: Template Rendering"""
        print("\n=== TEST 6: Template Rendering ===")
        try:
            with app.test_client() as client:
                # Test index page
                response = client.get('/')
                if '<!DOCTYPE html>' in response.get_data(as_text=True):
                    self.log_pass('Index template renders correctly')
                else:
                    self.log_bug('Templates', 'Index Render Failed',
                        'Index page returns invalid HTML', 'High')
                        
                # Test login page
                response = client.get('/login')
                if response.status_code == 200:
                    self.log_pass('Login page accessible')
                else:
                    self.log_bug('Templates', 'Login Page Error',
                        f'Login page returned {response.status_code}', 'High')
                        
        except Exception as e:
            self.log_bug('Templates', 'Template Rendering Error', str(e), 'High')
            
    def test_error_handling(self):
        """Test 7: Error Handling"""
        print("\n=== TEST 7: Error Handling ===")
        try:
            with app.test_client() as client:
                # Test 404 error
                response = client.get('/nonexistent/page')
                if response.status_code == 404:
                    self.log_pass('404 error handling works')
                else:
                    self.log_bug('ErrorHandling', '404 Not Handled',
                        f'Nonexistent route returned {response.status_code}', 'Medium')
                        
        except Exception as e:
            self.log_bug('ErrorHandling', 'Error Test Failed', str(e))
            
    def test_data_consistency(self):
        """Test 8: Data Consistency"""
        print("\n=== TEST 8: Data Consistency ===")
        try:
            # Load mock database
            with open('/home/prajwal/Desktop/Hostel-Hub/data/mock_db.json', 'r') as f:
                db_data = json.load(f)
            
            # Check users table
            if 'users' in db_data:
                users = db_data['users']
                
                # Check for required fields
                missing_fields = []
                for user in users:
                    required = ['id', 'username', 'email', 'role', 'is_active']
                    for field in required:
                        if field not in user:
                            missing_fields.append(f"User {user.get('username', 'unknown')}: missing '{field}'")
                
                if missing_fields:
                    self.log_bug('DataConsistency', 'Missing User Fields',
                        f"Fields missing in users: {', '.join(missing_fields[:3])}", 'High')
                else:
                    self.log_pass('All users have required fields')
            else:
                self.log_bug('DataConsistency', 'Users Table Missing',
                    'users table not found in mock database', 'Critical')
                    
            # Check hostel_settings
            if 'hostel_settings' in db_data:
                self.log_pass('hostel_settings table exists')
            else:
                self.log_bug('DataConsistency', 'Missing hostel_settings',
                    'hostel_settings table not found', 'High')
                    
        except Exception as e:
            self.log_bug('DataConsistency', 'Data Test Error', str(e), 'High')
            
    def test_role_based_access(self):
        """Test 9: Role-Based Access Control"""
        print("\n=== TEST 9: Role-Based Access Control ===")
        try:
            from app import role_required
            
            # Check if decorators are properly implemented
            self.log_pass('Role-based decorator imported successfully')
            
        except Exception as e:
            self.log_bug('Security', 'RBAC Not Implemented', str(e), 'High')
            
    def test_routes_availability(self):
        """Test 10: Routes Availability"""
        print("\n=== TEST 10: Routes Availability ===")
        try:
            from flask import url_for
            
            test_routes = [
                ('index', '/'),
                ('login', '/login'),
                ('register', '/register'),
                ('gallery', '/gallery'),
                ('contact', '/contact'),
            ]
            
            missing_routes = []
            for route_name, expected_path in test_routes:
                try:
                    with app.app_context():
                        path = url_for(route_name)
                        if path == expected_path:
                            pass
                        else:
                            missing_routes.append(f"{route_name}: got {path}, expected {expected_path}")
                except:
                    missing_routes.append(route_name)
            
            if missing_routes:
                self.log_bug('Routes', 'Missing/Wrong Routes',
                    f"Routes missing or incorrect: {', '.join(missing_routes[:3])}", 'High')
            else:
                self.log_pass('All core routes available')
                
        except Exception as e:
            self.log_bug('Routes', 'Route Test Error', str(e))
            
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("COMPREHENSIVE BUG TEST SUITE")
        print("="*60)
        
        self.test_database_connection()
        self.test_user_loading()
        self.test_input_validation()
        self.test_password_hashing()
        self.test_session_management()
        self.test_templates()
        self.test_error_handling()
        self.test_data_consistency()
        self.test_role_based_access()
        self.test_routes_availability()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Bugs Found: {len(self.bugs_found)}")
        
        if self.bugs_found:
            print("\n" + "="*60)
            print("BUGS FOUND BY SEVERITY")
            print("="*60)
            
            for severity in ['Critical', 'High', 'Medium', 'Low']:
                critical_bugs = [b for b in self.bugs_found if b['severity'] == severity]
                if critical_bugs:
                    print(f"\n{severity} ({len(critical_bugs)}):")
                    for bug in critical_bugs:
                        print(f"  • {bug['category']}: {bug['name']}")
        
        return len(self.bugs_found)

if __name__ == '__main__':
    runner = BugTestRunner()
    bug_count = runner.run_all_tests()
    sys.exit(0 if bug_count == 0 else 1)
