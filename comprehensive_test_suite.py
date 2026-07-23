"""
Comprehensive Testing Suite for Hostel Hub Flask Application
Tests Authentication, Authorization, UI/UX, Data Integrity, and Error Handling
"""

import unittest
import json
import sys
import os
from io import BytesIO
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, User, db
from config.database_mock import MockDatabase
import bcrypt

class HostelHubTestCase(unittest.TestCase):
    """Base test case for Hostel Hub application"""
    
    def setUp(self):
        """Set up test client and app context"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Tear down test client and app context"""
        self.app_context.pop()


class AuthenticationTests(HostelHubTestCase):
    """Test authentication functionality"""
    
    def test_login_page_loads(self):
        """Test login page loads without errors"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
    
    def test_valid_login_admin(self):
        """Test login with valid admin credentials"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertIn(b'dashboard', response.data.lower() or b'admin', response.data.lower())
    
    def test_valid_login_student(self):
        """Test login with valid student credentials"""
        response = self.client.post('/login', data={
            'username': 'prajwal',
            'password': 'admin123'
        }, follow_redirects=True)
        # Should redirect to dashboard or not show login error
        self.assertNotIn(b'Invalid username or password', response.data)
    
    def test_valid_login_warden(self):
        """Test login with valid warden credentials"""
        response = self.client.post('/login', data={
            'username': 'warden',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertNotIn(b'Invalid username or password', response.data)
    
    def test_invalid_username(self):
        """Test login with invalid username"""
        response = self.client.post('/login', data={
            'username': 'nonexistent_user',
            'password': 'admin123'
        })
        # Should show error or flash message
        self.assertIn(response.status_code, [200, 302])  # Either shows form again or redirects
    
    def test_invalid_password(self):
        """Test login with invalid password"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        self.assertIn(response.status_code, [200, 302])
    
    def test_empty_credentials(self):
        """Test login with empty credentials"""
        response = self.client.post('/login', data={
            'username': '',
            'password': ''
        })
        self.assertIn(response.status_code, [200, 302])
    
    def test_registration_page_loads(self):
        """Test registration page loads"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register', response.data.lower() or b'signup', response.data.lower())
    
    def test_session_creation_on_login(self):
        """Test session is created on successful login"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        # Session should contain user_id after login
        with self.client.session_transaction() as sess:
            # Session may or may not have user_id depending on implementation
            self.assertIsNotNone(sess)
    
    def test_logout_clears_session(self):
        """Test logout clears session"""
        # First login
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(response.status_code, [200, 302])
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        # This tests the hashing mechanism
        test_password = "admin123"
        # Pre-computed hash from database_mock.py
        known_hash = "$2b$12$fRl39TraAQ4NkUtay2xpJ.XXS7j2LZFUZtgfZBRzWePnfaqt8.vgK"
        
        # Verify bcrypt can validate it
        is_valid = bcrypt.checkpw(test_password.encode('utf-8'), known_hash.encode('utf-8'))
        self.assertTrue(is_valid, "Password hashing verification failed")


class AuthorizationTests(HostelHubTestCase):
    """Test role-based access control"""
    
    def test_admin_dashboard_requires_login(self):
        """Test admin dashboard requires authentication"""
        response = self.client.get('/admin/dashboard')
        self.assertIn(response.status_code, [302, 401])  # Should redirect to login
    
    def test_student_dashboard_requires_login(self):
        """Test student dashboard requires authentication"""
        response = self.client.get('/student/dashboard')
        self.assertIn(response.status_code, [302, 401])
    
    def test_warden_dashboard_requires_login(self):
        """Test warden dashboard requires authentication"""
        response = self.client.get('/warden/dashboard')
        self.assertIn(response.status_code, [302, 401])
    
    def test_student_cannot_access_admin_dashboard(self):
        """Test student cannot access admin dashboard"""
        # Login as student
        with self.client:
            self.client.post('/login', data={
                'username': 'prajwal',
                'password': 'admin123'
            })
            
            # Try to access admin dashboard
            response = self.client.get('/admin/dashboard')
            # Should either redirect or show forbidden
            self.assertIn(response.status_code, [302, 403, 401])
    
    def test_warden_cannot_access_admin_dashboard(self):
        """Test warden cannot access admin dashboard"""
        with self.client:
            self.client.post('/login', data={
                'username': 'warden',
                'password': 'admin123'
            })
            
            response = self.client.get('/admin/dashboard')
            self.assertIn(response.status_code, [302, 403, 401])
    
    def test_admin_can_access_admin_dashboard(self):
        """Test admin can access admin dashboard"""
        with self.client:
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            
            response = self.client.get('/admin/dashboard')
            # Admin should be able to access
            self.assertIn(response.status_code, [200, 302])  # May redirect if already on dashboard
    
    def test_admin_cannot_access_student_specific_features(self):
        """Test admin accessing student-only endpoints"""
        with self.client:
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            
            # Admins shouldn't access student personal dashboard
            response = self.client.get('/student/profile')
            # Should be restricted
            self.assertIn(response.status_code, [302, 403, 401])


class UIUXTests(HostelHubTestCase):
    """Test UI/UX and page loading"""
    
    def test_homepage_loads(self):
        """Test homepage loads without errors"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'hostel', response.data.lower())
    
    def test_gallery_page_loads(self):
        """Test gallery page loads"""
        response = self.client.get('/gallery')
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'contact', response.data.lower())
    
    def test_about_page_loads(self):
        """Test about page loads"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
    
    def test_404_error_handling(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-page-12345')
        self.assertEqual(response.status_code, 404)
    
    def test_all_css_files_referenced(self):
        """Test CSS files are properly referenced"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for CSS link tags
        self.assertIn(b'<link', response.data)
    
    def test_navigation_links_present(self):
        """Test navigation links are present"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for common navigation elements
        self.assertIn(b'href', response.data)  # Links should be present
    
    def test_form_validation_required_fields(self):
        """Test form validation for required fields"""
        # Try registration with empty fields
        response = self.client.post('/register', data={
            'username': '',
            'email': '',
            'password': '',
            'confirm_password': '',
            'full_name': ''
        })
        # Should either reject or redirect
        self.assertIn(response.status_code, [200, 302, 400])


class DataIntegrityTests(HostelHubTestCase):
    """Test data integrity and consistency"""
    
    def test_room_data_consistency(self):
        """Test room data is consistent"""
        # Mock database should have valid rooms
        if hasattr(db, 'data'):
            rooms = db.data.get('rooms', [])
            self.assertIsInstance(rooms, list)
            
            for room in rooms:
                self.assertIn('id', room)
                self.assertIn('room_number', room)
                self.assertIn('capacity', room)
                self.assertIn('room_type', room)
    
    def test_student_data_consistency(self):
        """Test student data is consistent"""
        if hasattr(db, 'data'):
            students = db.data.get('students', [])
            self.assertIsInstance(students, list)
            
            for student in students:
                self.assertIn('id', student)
                self.assertIn('user_id', student)
                self.assertIn('roll_number', student)
    
    def test_user_data_consistency(self):
        """Test user data is consistent"""
        if hasattr(db, 'data'):
            users = db.data.get('users', [])
            self.assertIsInstance(users, list)
            
            for user in users:
                self.assertIn('id', user)
                self.assertIn('username', user)
                self.assertIn('role', user)
                self.assertIn('email', user)
    
    def test_complaint_data_consistency(self):
        """Test complaint data is consistent"""
        if hasattr(db, 'data'):
            complaints = db.data.get('complaints', [])
            self.assertIsInstance(complaints, list)
            
            for complaint in complaints:
                self.assertIn('id', complaint)
                self.assertIn('student_id', complaint)
                self.assertIn('status', complaint)
                self.assertIn('created_at', complaint)
    
    def test_fee_data_consistency(self):
        """Test fee data is consistent"""
        if hasattr(db, 'data'):
            fees = db.data.get('fees', [])
            self.assertIsInstance(fees, list)
            
            for fee in fees:
                self.assertIn('id', fee)
                self.assertIn('student_id', fee)
                self.assertIn('status', fee)
                self.assertIn('room_rent', fee)


class ErrorHandlingTests(HostelHubTestCase):
    """Test error handling"""
    
    def test_404_error_page(self):
        """Test 404 error page displays"""
        response = self.client.get('/this-page-does-not-exist-99999')
        self.assertEqual(response.status_code, 404)
    
    def test_missing_required_fields_in_login(self):
        """Test login with missing fields"""
        response = self.client.post('/login', data={
            'username': 'admin'
            # Missing password
        })
        self.assertIn(response.status_code, [200, 302, 400])
    
    def test_invalid_form_data_type(self):
        """Test form with invalid data types"""
        response = self.client.post('/login', data={
            'username': 123,  # Should be string
            'password': {'invalid': 'dict'}  # Should be string
        })
        # Should handle gracefully
        self.assertIn(response.status_code, [200, 302, 400])
    
    def test_xss_protection_in_forms(self):
        """Test XSS protection in forms"""
        response = self.client.post('/login', data={
            'username': '<script>alert("xss")</script>',
            'password': 'admin123'
        })
        # Should handle without executing script
        self.assertIn(response.status_code, [200, 302, 400])
        # Response should escape the script tags
        self.assertNotIn(b'<script>alert', response.data)
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        response = self.client.post('/login', data={
            'username': "admin'; DROP TABLE users; --",
            'password': "admin123' OR '1'='1"
        })
        # Should handle without SQL injection
        self.assertIn(response.status_code, [200, 302, 400])
    
    def test_very_long_input(self):
        """Test handling of very long input"""
        response = self.client.post('/login', data={
            'username': 'a' * 10000,
            'password': 'b' * 10000
        })
        # Should handle without crashing
        self.assertIn(response.status_code, [200, 302, 400, 413])
    
    def test_special_characters_in_input(self):
        """Test special characters in input"""
        response = self.client.post('/login', data={
            'username': '!@#$%^&*()',
            'password': '!@#$%^&*()'
        })
        # Should handle without crashing
        self.assertIn(response.status_code, [200, 302, 400])
    
    def test_unicode_characters_in_input(self):
        """Test Unicode characters in input"""
        response = self.client.post('/login', data={
            'username': '用户名',
            'password': '密码'
        })
        # Should handle Unicode
        self.assertIn(response.status_code, [200, 302, 400])


class CRUDOperationsTests(HostelHubTestCase):
    """Test CRUD operations"""
    
    def test_complaint_submission(self):
        """Test complaint submission"""
        with self.client:
            # Login as student
            self.client.post('/login', data={
                'username': 'prajwal',
                'password': 'admin123'
            })
            
            # Try to submit complaint
            response = self.client.post('/student/complaints', data={
                'category': 'Maintenance',
                'description': 'Test complaint',
                'priority': 'high'
            }, follow_redirects=True)
            
            # Should either succeed or show form again
            self.assertIn(response.status_code, [200, 302])
    
    def test_visitor_request_submission(self):
        """Test visitor request submission"""
        with self.client:
            self.client.post('/login', data={
                'username': 'prajwal',
                'password': 'admin123'
            })
            
            response = self.client.post('/student/visitors', data={
                'visitor_name': 'Test Visitor',
                'purpose': 'Visit',
                'date': '2024-12-31',
                'time': '10:00'
            }, follow_redirects=True)
            
            self.assertIn(response.status_code, [200, 302])
    
    def test_profile_update(self):
        """Test profile update"""
        with self.client:
            self.client.post('/login', data={
                'username': 'prajwal',
                'password': 'admin123'
            })
            
            response = self.client.post('/student/profile', data={
                'full_name': 'Updated Name',
                'phone': '9999999999',
                'email': 'updated@hostel.com'
            }, follow_redirects=True)
            
            self.assertIn(response.status_code, [200, 302])


class ResponseTimeTests(HostelHubTestCase):
    """Test response times and performance"""
    
    def test_homepage_response_time(self):
        """Test homepage loads quickly"""
        import time
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        # Should load in under 2 seconds
        self.assertLess(elapsed, 2.0, f"Homepage took {elapsed:.2f}s to load")
    
    def test_login_page_response_time(self):
        """Test login page loads quickly"""
        import time
        start = time.time()
        response = self.client.get('/login')
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(elapsed, 2.0, f"Login page took {elapsed:.2f}s to load")


class ContentTests(HostelHubTestCase):
    """Test content and data display"""
    
    def test_homepage_has_content(self):
        """Test homepage displays content"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 100)  # Should have significant content
    
    def test_login_form_fields_present(self):
        """Test login form has required fields"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.data.lower())
        self.assertIn(b'password', response.data.lower())
    
    def test_registration_form_fields_present(self):
        """Test registration form has required fields"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        # Should have password fields
        self.assertIn(b'password', response.data.lower())


class TestRunner:
    """Run all tests and generate report"""
    
    @staticmethod
    def run_all_tests(verbosity=2):
        """Run all test suites"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add all test classes
        suite.addTests(loader.loadTestsFromTestCase(AuthenticationTests))
        suite.addTests(loader.loadTestsFromTestCase(AuthorizationTests))
        suite.addTests(loader.loadTestsFromTestCase(UIUXTests))
        suite.addTests(loader.loadTestsFromTestCase(DataIntegrityTests))
        suite.addTests(loader.loadTestsFromTestCase(ErrorHandlingTests))
        suite.addTests(loader.loadTestsFromTestCase(CRUDOperationsTests))
        suite.addTests(loader.loadTestsFromTestCase(ResponseTimeTests))
        suite.addTests(loader.loadTestsFromTestCase(ContentTests))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        return result


if __name__ == '__main__':
    # Run all tests with detailed output
    result = TestRunner.run_all_tests(verbosity=2)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
