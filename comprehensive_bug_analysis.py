#!/usr/bin/env python3
"""
Comprehensive Bug Analysis & Testing for Hostel Hub
Tests: Authentication, UI, Database, Performance, Security
"""

import json
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

# Initialize Flask app for testing
os.environ['FLASK_ENV'] = 'testing'

from app import app, db
import re
from datetime import datetime

class BugAnalyzer:
    def __init__(self):
        self.bugs = []
        self.app = app
        self.client = app.test_client()
        self.db = db
        
    def log_bug(self, category, severity, title, description, steps_to_reproduce, 
                expected_behavior, actual_behavior, root_cause, suggested_fix):
        """Log a bug finding"""
        bug = {
            'category': category,
            'severity': severity,
            'title': title,
            'description': description,
            'steps_to_reproduce': steps_to_reproduce,
            'expected_behavior': expected_behavior,
            'actual_behavior': actual_behavior,
            'root_cause': root_cause,
            'suggested_fix': suggested_fix,
            'priority_order': self._get_priority(severity)
        }
        self.bugs.append(bug)
        print(f"[{severity.upper()}] {title}")
        
    def _get_priority(self, severity):
        """Get priority number for sorting"""
        priority_map = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4
        }
        return priority_map.get(severity.lower(), 5)
    
    # ==================== AUTHENTICATION TESTS ====================
    def test_authentication_bugs(self):
        print("\n[TEST] Authentication & Authorization")
        
        # Test 1: Login page XSS vulnerability
        with app.test_request_context():
            response = self.client.post('/login', data={
                'username': '<script>alert("XSS")</script>',
                'password': 'test'
            })
            # Check if input is properly escaped
            if b'<script>' in response.data:
                self.log_bug(
                    category='Security',
                    severity='critical',
                    title='XSS Vulnerability in Login Form',
                    description='User input is not properly escaped in login form',
                    steps_to_reproduce=[
                        '1. Go to login page',
                        '2. Enter <script>alert("test")</script> in username field',
                        '3. Observe if script tags are rendered'
                    ],
                    expected_behavior='Script tags should be HTML-escaped',
                    actual_behavior='Script tags are rendered in response',
                    root_cause='User input not escaped in template rendering',
                    suggested_fix='Use Flask Jinja2 autoescaping (enabled by default) and validate template rendering'
                )
        
        # Test 2: Password reset flow without email verification
        with app.test_request_context():
            response = self.client.get('/forgot_password')
            if response.status_code == 200:
                # Check if OTP email is actually sent (currently might not be)
                if 'SMTP' not in os.environ and 'EMAIL_SEND' not in os.environ:
                    self.log_bug(
                        category='Authentication',
                        severity='high',
                        title='Password Reset May Not Send Emails',
                        description='Forgot password feature may not send OTP emails if SMTP not configured',
                        steps_to_reproduce=[
                            '1. Click "Forgot Password?"',
                            '2. Enter email address',
                            '3. Wait for OTP email'
                        ],
                        expected_behavior='OTP email should be sent immediately',
                        actual_behavior='Email may not send if SMTP not configured',
                        root_cause='SMTP configuration not verified or handled gracefully',
                        suggested_fix='Add SMTP validation or use alternative email service; fallback to admin notification'
                    )
    
    # ==================== DATABASE TESTS ====================
    def test_database_bugs(self):
        print("\n[TEST] Database & Data Integrity")
        
        # Test 1: Check if mock database has proper table structure
        try:
            cursor = db.connection.cursor()
            
            # Check if users table exists and has required fields
            cursor.execute("SELECT * FROM users LIMIT 1")
            user = cursor.fetchone()
            
            required_user_fields = ['id', 'username', 'email', 'role', 'gender', 'is_active']
            if isinstance(user, dict):
                missing_fields = [f for f in required_user_fields if f not in user]
                if missing_fields:
                    self.log_bug(
                        category='Database',
                        severity='high',
                        title='Missing User Table Fields',
                        description=f'User table missing required fields: {missing_fields}',
                        steps_to_reproduce=['1. Check mock_db.json user structure'],
                        expected_behavior='All user records should have: ' + ', '.join(required_user_fields),
                        actual_behavior=f'Missing fields: {missing_fields}',
                        root_cause='mock_db.json not properly initialized with all required fields',
                        suggested_fix='Update mock_db.json initialization to include all required fields'
                    )
            
            # Test 2: Check room occupancy cascading
            cursor.execute("SELECT * FROM room_occupancy LIMIT 1")
            occupancy = cursor.fetchone()
            if occupancy:
                # Check if student_id exists in users
                student_id = occupancy.get('student_id') if isinstance(occupancy, dict) else occupancy[1]
                cursor.execute("SELECT id FROM users WHERE id = %s", (student_id,))
                if not cursor.fetchone():
                    self.log_bug(
                        category='Database',
                        severity='high',
                        title='Orphaned Room Occupancy Records',
                        description='Room occupancy records reference non-existent students',
                        steps_to_reproduce=['1. Check room_occupancy table for orphaned records'],
                        expected_behavior='All student_id references should exist in users table',
                        actual_behavior='Found occupancy records with non-existent student IDs',
                        root_cause='No foreign key constraints or cascading delete enforcement',
                        suggested_fix='Add database constraints or cleanup script to remove orphaned records'
                    )
            
            cursor.close()
        except Exception as e:
            print(f"Database test error: {e}")
    
    # ==================== UI/UX TESTS ====================
    def test_ui_bugs(self):
        print("\n[TEST] UI & User Experience")
        
        # Test 1: Missing page titles
        pages = [
            ('/', 'index'),
            ('/login', 'login'),
            ('/register', 'register'),
            ('/gallery', 'gallery'),
            ('/contact', 'contact'),
        ]
        
        for url, page_name in pages:
            response = self.client.get(url)
            if response.status_code == 200:
                if b'<title>' not in response.data:
                    self.log_bug(
                        category='UI',
                        severity='low',
                        title=f'Missing Page Title on {page_name}',
                        description=f'Page {url} does not have a <title> tag',
                        steps_to_reproduce=[f'1. Visit {url}', '2. Check page source for <title>'],
                        expected_behavior='Every page should have a descriptive <title> tag',
                        actual_behavior='<title> tag is missing',
                        root_cause='Template missing <title> tag in <head>',
                        suggested_fix='Add <title> tags to all HTML templates'
                    )
        
        # Test 2: Check for responsive design meta tag
        response = self.client.get('/')
        if b'viewport' not in response.data.lower():
            self.log_bug(
                category='UI',
                severity='medium',
                title='Missing Responsive Design Viewport Meta Tag',
                description='Home page missing viewport meta tag for mobile responsiveness',
                steps_to_reproduce=['1. Visit home page', '2. Check source code for viewport meta tag'],
                expected_behavior='<meta name="viewport" content="width=device-width, initial-scale=1"> should be present',
                actual_behavior='Viewport meta tag is missing',
                root_cause='Template missing responsive design meta tag',
                suggested_fix='Add viewport meta tag to base.html template'
            )
    
    # ==================== SECURITY TESTS ====================
    def test_security_bugs(self):
        print("\n[TEST] Security")
        
        # Test 1: Check for CSRF protection
        response = self.client.get('/register')
        if b'csrf_token' not in response.data.lower() and b'CSRF' not in response.data:
            self.log_bug(
                category='Security',
                severity='high',
                title='Missing CSRF Protection on Forms',
                description='Registration form missing CSRF token',
                steps_to_reproduce=['1. Go to /register', '2. Check form for CSRF token'],
                expected_behavior='All forms should include a CSRF token',
                actual_behavior='No CSRF token found in form',
                root_cause='CSRF protection not implemented in Flask app',
                suggested_fix='Implement Flask-WTF for CSRF protection on all forms'
            )
        
        # Test 2: SQL Injection in search fields
        with app.test_request_context():
            response = self.client.get('/admin/students?search=" OR "1"="1')
            if b'OR' in response.data and b'1' in response.data:
                self.log_bug(
                    category='Security',
                    severity='critical',
                    title='Potential SQL Injection Vulnerability',
                    description='Student search endpoint may be vulnerable to SQL injection',
                    steps_to_reproduce=['1. Go to Admin → Students', '2. Search for: " OR "1"="1'],
                    expected_behavior='Query should be parameterized and safe',
                    actual_behavior='SQL injection pattern detected in response',
                    root_cause='User input not properly parameterized in SQL queries',
                    suggested_fix='Ensure all queries use parameterized queries with %s placeholders'
                )
    
    # ==================== PERFORMANCE TESTS ====================
    def test_performance_bugs(self):
        print("\n[TEST] Performance")
        
        # Test 1: N+1 Query Problem on dashboards
        import time
        
        # Login first
        with app.test_client() as client:
            client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            
            # Measure dashboard load time
            start = time.time()
            response = client.get('/admin/dashboard')
            load_time = time.time() - start
            
            if load_time > 0.5:  # More than 500ms is slow
                self.log_bug(
                    category='Performance',
                    severity='medium',
                    title='Slow Admin Dashboard Load Time',
                    description=f'Admin dashboard takes {load_time:.2f}s to load',
                    steps_to_reproduce=['1. Login as admin', '2. Go to Admin Dashboard', '3. Measure load time'],
                    expected_behavior='Dashboard should load in less than 200ms',
                    actual_behavior=f'Dashboard loads in {load_time:.2f}s',
                    root_cause='Possible N+1 query problem or inefficient database queries',
                    suggested_fix='Optimize queries using JOINs, add indexes, implement query caching'
                )
    
    # ==================== DATA VALIDATION TESTS ====================
    def test_data_validation_bugs(self):
        print("\n[TEST] Data Validation")
        
        # Test 1: Empty string validation on registration
        with app.test_client() as client:
            response = client.post('/register', data={
                'full_name': '',
                'email': 'test@test.com',
                'username': 'testuser',
                'password': 'test123',
                'confirm_password': 'test123',
                'roll_number': '001',
                'phone': '9999999999',
                'gender': 'Male'
            })
            
            # Should reject empty full_name
            if response.status_code == 200 and b'error' not in response.data.lower():
                self.log_bug(
                    category='Data Validation',
                    severity='medium',
                    title='Missing Full Name Validation',
                    description='Registration accepts empty full name',
                    steps_to_reproduce=['1. Go to /register', '2. Leave full_name empty', '3. Submit form'],
                    expected_behavior='Form should reject empty full name with error message',
                    actual_behavior='Form accepts empty full name',
                    root_cause='Client-side and server-side validation missing for full_name',
                    suggested_fix='Add required attribute to HTML and server-side validation in Python'
                )
    
    # ==================== ERROR HANDLING TESTS ====================
    def test_error_handling_bugs(self):
        print("\n[TEST] Error Handling")
        
        # Test 1: 404 error handling
        response = self.client.get('/nonexistent_page')
        if response.status_code == 404:
            if b'404' not in response.data:
                self.log_bug(
                    category='Error Handling',
                    severity='low',
                    title='Inadequate 404 Error Page',
                    description='404 error page does not clearly indicate page not found',
                    steps_to_reproduce=['1. Visit non-existent page', '2. Check error message'],
                    expected_behavior='Clear 404 error message with helpful navigation options',
                    actual_behavior='Generic error message or confusing error response',
                    root_cause='Custom 404 handler not properly implemented',
                    suggested_fix='Implement custom 404 error handler in app.py'
                )
    
    # ==================== DATABASE CONNECTION TESTS ====================
    def test_database_connection_bugs(self):
        print("\n[TEST] Database Connection")
        
        # Test 1: Check database fallback mechanism
        if db.connection is None:
            print("✓ Database properly falls back to mock database")
        else:
            # Check if connection is actually MySQL or mock
            try:
                cursor = db.connection.cursor()
                cursor.execute("SELECT DATABASE()")
                result = cursor.fetchone()
                if result is None:
                    self.log_bug(
                        category='Database',
                        severity='high',
                        title='Unreliable Database Connection',
                        description='Database connection exists but is not properly initialized',
                        steps_to_reproduce=['1. Check database connection status'],
                        expected_behavior='Database should be either MySQL or properly initialized mock',
                        actual_behavior='Database connection is unreliable',
                        root_cause='Database connection not properly validated',
                        suggested_fix='Add connection validation and health check in database.py'
                    )
                cursor.close()
            except Exception as e:
                print(f"Database connection test error: {e}")
    
    # ==================== ROOM ALLOCATION BUGS ====================
    def test_room_allocation_bugs(self):
        print("\n[TEST] Room Allocation Logic")
        
        # Check for gender-based allocation issues
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM rooms WHERE gender_restriction IS NOT NULL LIMIT 1")
            room = cursor.fetchone()
            
            if room:
                room_id = room.get('id') if isinstance(room, dict) else room[0]
                gender_restriction = room.get('gender_restriction') if isinstance(room, dict) else room[-1]
                
                # Check if there are students of opposite gender allocated
                cursor.execute("""
                    SELECT ro.*, u.gender 
                    FROM room_occupancy ro
                    JOIN users u ON ro.student_id = u.id
                    WHERE ro.room_id = %s
                """, (room_id,))
                occupants = cursor.fetchall()
                
                for occupant in occupants:
                    student_gender = occupant.get('gender') if isinstance(occupant, dict) else occupant[-1]
                    if student_gender and student_gender.lower() != gender_restriction.lower():
                        self.log_bug(
                            category='Data Integrity',
                            severity='critical',
                            title='Gender Restriction Violation in Room Allocation',
                            description=f'Room {room_id} has gender restriction "{gender_restriction}" but allocated student has gender "{student_gender}"',
                            steps_to_reproduce=['1. Check room allocations', '2. Find rooms with gender restriction violations'],
                            expected_behavior='All students in gender-restricted rooms should match the restriction',
                            actual_behavior='Found students violating gender restriction',
                            root_cause='Gender validation not enforced during room allocation',
                            suggested_fix='Add strict gender validation before confirming room allocation'
                        )
            cursor.close()
        except Exception as e:
            print(f"Room allocation test error: {e}")
    
    # ==================== FILE UPLOAD BUGS ====================
    def test_file_upload_bugs(self):
        print("\n[TEST] File Upload (Gallery)")
        
        # Test 1: Check if gallery endpoint validates file types
        response = self.client.get('/admin/gallery')
        if response.status_code == 200:
            if b'accept=' not in response.data and b'image' not in response.data.lower():
                self.log_bug(
                    category='Security',
                    severity='medium',
                    title='Missing File Type Validation on Gallery Upload',
                    description='Gallery upload may accept non-image files',
                    steps_to_reproduce=['1. Go to Admin → Gallery', '2. Try uploading non-image file'],
                    expected_behavior='File input should accept only image files',
                    actual_behavior='File type validation missing',
                    root_cause='HTML file input and backend validation not properly configured',
                    suggested_fix='Add accept="image/*" to file input and validate MIME type on backend'
                )
    
    # ==================== COMPLAINT WORKFLOW BUGS ====================
    def test_complaint_workflow_bugs(self):
        print("\n[TEST] Complaint Management")
        
        # Check complaint status transition logic
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM complaints LIMIT 5")
            complaints = cursor.fetchall()
            
            for complaint in complaints:
                status = complaint.get('status') if isinstance(complaint, dict) else complaint[3]
                resolution_notes = complaint.get('resolution_notes') if isinstance(complaint, dict) else None
                
                # If resolved but no resolution notes
                if status == 'Resolved' and not resolution_notes:
                    self.log_bug(
                        category='Data Integrity',
                        severity='medium',
                        title='Resolved Complaint Without Resolution Notes',
                        description='Found resolved complaint with no resolution notes provided',
                        steps_to_reproduce=['1. Check complaints list', '2. Find resolved complaints without notes'],
                        expected_behavior='All resolved complaints should have resolution notes',
                        actual_behavior='Found resolved complaint without notes',
                        root_cause='Validation not enforced when marking complaint as resolved',
                        suggested_fix='Make resolution_notes required when status changes to "Resolved"'
                    )
            cursor.close()
        except Exception as e:
            print(f"Complaint workflow test error: {e}")
    
    # ==================== FEE CALCULATION BUGS ====================
    def test_fee_calculation_bugs(self):
        print("\n[TEST] Fee Management")
        
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM fees LIMIT 1")
            fee = cursor.fetchone()
            
            if fee:
                # Check if fee amounts are valid
                amount = fee.get('amount') if isinstance(fee, dict) else fee[3]
                if amount and isinstance(amount, str):
                    try:
                        float(amount)
                    except ValueError:
                        self.log_bug(
                            category='Data Validation',
                            severity='high',
                            title='Invalid Fee Amount Data Type',
                            description='Fee amount stored as string instead of numeric',
                            steps_to_reproduce=['1. Check fees table', '2. Inspect amount field'],
                            expected_behavior='Fee amounts should be stored as DECIMAL or FLOAT',
                            actual_behavior='Fee amounts stored as strings',
                            root_cause='Database schema mismatch or improper data insertion',
                            suggested_fix='Ensure amounts are converted to numeric types before storage'
                        )
            cursor.close()
        except Exception as e:
            print(f"Fee calculation test error: {e}")
    
    # ==================== SESSION MANAGEMENT BUGS ====================
    def test_session_management_bugs(self):
        print("\n[TEST] Session Management")
        
        # Test 1: Session fixation vulnerability
        with app.test_client() as client1:
            response = client1.get('/')
            session_id_before = response.headers.get('Set-Cookie')
            
            # Login
            client1.post('/login', data={'username': 'admin', 'password': 'admin123'})
            session_id_after = response.headers.get('Set-Cookie')
            
            if session_id_before == session_id_after:
                self.log_bug(
                    category='Security',
                    severity='high',
                    title='Session Fixation Vulnerability',
                    description='Session ID does not change after login',
                    steps_to_reproduce=['1. Note session ID before login', '2. Login', '3. Check session ID after login'],
                    expected_behavior='New session ID should be generated after successful login',
                    actual_behavior='Session ID remains the same',
                    root_cause='Session regeneration not implemented in login handler',
                    suggested_fix='Call session.clear() and regenerate session ID after successful login'
                )
    
    # ==================== NOTICE MANAGEMENT BUGS ====================
    def test_notice_bugs(self):
        print("\n[TEST] Notice Board Management")
        
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM notices ORDER BY created_at DESC LIMIT 1")
            notice = cursor.fetchone()
            
            if notice:
                # Check if notice has all required fields
                required_fields = ['title', 'content', 'created_at']
                if isinstance(notice, dict):
                    missing = [f for f in required_fields if f not in notice or not notice[f]]
                    if missing:
                        self.log_bug(
                            category='Data Integrity',
                            severity='medium',
                            title='Notice Missing Required Fields',
                            description=f'Notice missing fields: {missing}',
                            steps_to_reproduce=['1. Check notices table'],
                            expected_behavior='All notices should have title, content, and created_at',
                            actual_behavior=f'Missing fields: {missing}',
                            root_cause='Notice creation not validating required fields',
                            suggested_fix='Add validation to ensure all required fields are populated'
                        )
            cursor.close()
        except Exception as e:
            print(f"Notice test error: {e}")
    
    # ==================== VISITOR REQUEST BUGS ====================
    def test_visitor_bugs(self):
        print("\n[TEST] Visitor Management")
        
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM visitors WHERE status = 'Approved' LIMIT 1")
            visitor = cursor.fetchone()
            
            if visitor:
                # Check if visit date is in future
                visit_date = visitor.get('visit_date') if isinstance(visitor, dict) else visitor[4]
                if visit_date:
                    from datetime import datetime
                    visit_datetime = datetime.strptime(visit_date, '%Y-%m-%d %H:%M:%S') if isinstance(visit_date, str) else visit_date
                    if visit_datetime < datetime.now():
                        self.log_bug(
                            category='Data Integrity',
                            severity='low',
                            title='Approved Visitor Request With Past Visit Date',
                            description='Approved visitor request has already passed visit date',
                            steps_to_reproduce=['1. Check approved visitor requests', '2. Check visit dates'],
                            expected_behavior='Approved requests should have future visit dates or be auto-archived',
                            actual_behavior='Found approved request with past visit date',
                            root_cause='No automatic archiving or cleanup of expired visitor requests',
                            suggested_fix='Implement scheduled job to archive/expire past visitor requests'
                        )
            cursor.close()
        except Exception as e:
            print(f"Visitor test error: {e}")
    
    def run_all_tests(self):
        """Run all bug tests"""
        print("="*80)
        print("HOSTEL HUB - COMPREHENSIVE BUG ANALYSIS")
        print("="*80)
        
        self.test_authentication_bugs()
        self.test_database_bugs()
        self.test_ui_bugs()
        self.test_security_bugs()
        self.test_performance_bugs()
        self.test_data_validation_bugs()
        self.test_error_handling_bugs()
        self.test_database_connection_bugs()
        self.test_room_allocation_bugs()
        self.test_file_upload_bugs()
        self.test_complaint_workflow_bugs()
        self.test_fee_calculation_bugs()
        self.test_session_management_bugs()
        self.test_notice_bugs()
        self.test_visitor_bugs()
        
        return self.bugs
    
    def generate_report(self):
        """Generate a prioritized bug report"""
        # Sort by priority
        sorted_bugs = sorted(self.bugs, key=lambda x: x['priority_order'])
        
        # Group by category
        by_category = {}
        for bug in sorted_bugs:
            cat = bug['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(bug)
        
        # Group by severity
        by_severity = {}
        for bug in sorted_bugs:
            sev = bug['severity'].upper()
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(bug)
        
        return {
            'all_bugs': sorted_bugs,
            'by_category': by_category,
            'by_severity': by_severity,
            'total_bugs': len(sorted_bugs),
            'critical_count': len(by_severity.get('CRITICAL', [])),
            'high_count': len(by_severity.get('HIGH', [])),
            'medium_count': len(by_severity.get('MEDIUM', [])),
            'low_count': len(by_severity.get('LOW', []))
        }

if __name__ == '__main__':
    analyzer = BugAnalyzer()
    bugs = analyzer.run_all_tests()
    report = analyzer.generate_report()
    
    # Print summary
    print("\n" + "="*80)
    print("BUG ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nTotal Bugs Found: {report['total_bugs']}")
    print(f"Critical: {report['critical_count']}")
    print(f"High: {report['high_count']}")
    print(f"Medium: {report['medium_count']}")
    print(f"Low: {report['low_count']}")
    
    # Save report to JSON
    with open('/home/prajwal/Desktop/Hostel-Hub/BUG_ANALYSIS_REPORT.json', 'w') as f:
        # Convert to JSON-serializable format
        json_report = {
            'summary': {
                'total_bugs': report['total_bugs'],
                'critical': report['critical_count'],
                'high': report['high_count'],
                'medium': report['medium_count'],
                'low': report['low_count']
            },
            'bugs_by_severity': {
                'CRITICAL': report['by_severity'].get('CRITICAL', []),
                'HIGH': report['by_severity'].get('HIGH', []),
                'MEDIUM': report['by_severity'].get('MEDIUM', []),
                'LOW': report['by_severity'].get('LOW', [])
            },
            'all_bugs': report['all_bugs']
        }
        json.dump(json_report, f, indent=2, default=str)
    
    print("\nReport saved to BUG_ANALYSIS_REPORT.json")
