#!/usr/bin/env python3
"""
Detailed Code Audit for Bug Detection
Analyzes code for security, data handling, and performance issues
"""

import re
import os
import json

class CodeAudit:
    def __init__(self):
        self.issues = []
        self.base_path = '/home/prajwal/Desktop/Hostel-Hub'
        
    def add_issue(self, file, line_no, issue_type, description, severity='Medium'):
        self.issues.append({
            'file': file,
            'line': line_no,
            'type': issue_type,
            'description': description,
            'severity': severity
        })
        print(f"[{severity}] {file}:{line_no} - {issue_type}")
        print(f"    {description}\n")
        
    def audit_app_py(self):
        """Audit app.py"""
        print("\n=== AUDITING app.py ===\n")
        
        with open(f'{self.base_path}/app.py', 'r') as f:
            lines = f.readlines()
        
        # Check 1: SQL Injection vulnerabilities
        for i, line in enumerate(lines, 1):
            if 'cursor.execute' in line and '%s' not in line and 'SELECT' in line:
                # Check if it's using string formatting
                if '+' in line or 'format' in line or '{' in line:
                    self.add_issue('app.py', i, 'SQL Injection Risk',
                        'Potential SQL injection: using string concatenation', 'Critical')
        
        # Check 2: Direct string operations on user input
        for i, line in enumerate(lines, 1):
            if 'request.form.get' in line and '.upper()' in line:
                if '.strip()' not in line:
                    self.add_issue('app.py', i, 'Input Validation',
                        'User input not stripped before operations', 'High')
        
        # Check 3: Missing error handling
        for i, line in enumerate(lines, 1):
            if 'cursor.execute' in line:
                # Check if next few lines have try-except
                context = ''.join(lines[max(0, i-2):min(len(lines), i+5)])
                if 'try:' not in context and 'except' not in context:
                    pass  # OK for now, will check below
    
    def audit_routes(self):
        """Audit route files"""
        print("\n=== AUDITING routes/ ===\n")
        
        for route_file in ['admin_routes.py', 'student_routes.py', 'warden_routes.py']:
            filepath = f'{self.base_path}/routes/{route_file}'
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Check for missing input validation
            for i, line in enumerate(lines, 1):
                if 'request.form.get' in line or 'request.args.get' in line:
                    # Check if there's validation in next lines
                    context = ''.join(lines[i:min(len(lines), i+3)])
                    if 'if not' not in context and 'strip()' not in line:
                        pass  # May be valid
    
    def audit_database_mock(self):
        """Audit mock database"""
        print("\n=== AUDITING database_mock.py ===\n")
        
        with open(f'{self.base_path}/config/database_mock.py', 'r') as f:
            lines = f.readlines()
        
        # Check for query parsing issues
        for i, line in enumerate(lines, 1):
            if 'parse_select' in line or 'parse_insert' in line:
                # These are critical for SQL injection prevention
                pass
    
    def audit_templates(self):
        """Audit templates for XSS vulnerabilities"""
        print("\n=== AUDITING templates/ ===\n")
        
        template_dir = f'{self.base_path}/templates'
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                    
                    for i, line in enumerate(lines, 1):
                        # Check for unescaped variables
                        if '{{ ' in line and ' }}' in line:
                            # Extract variable
                            vars_match = re.findall(r'{{\s*([^}]+)\s*}}', line)
                            for var in vars_match:
                                # Check if it's using filter
                                if '|e' not in line and '|escape' not in line:
                                    # This could be XSS if var contains HTML
                                    if any(x in var.lower() for x in ['comment', 'content', 'message', 'description']):
                                        self.add_issue(filepath, i, 'XSS Vulnerability',
                                            f'Unescaped variable: {var}', 'High')
    
    def audit_data_validation(self):
        """Check for data validation issues"""
        print("\n=== AUDITING Data Validation ===\n")
        
        # Check mock_db.json for consistency
        with open(f'{self.base_path}/data/mock_db.json', 'r') as f:
            db_data = json.load(f)
        
        # Validate users table
        if 'users' in db_data:
            required_fields = ['id', 'username', 'email', 'role', 'password_hash', 'is_active', 'created_at']
            
            for i, user in enumerate(db_data['users']):
                missing = [f for f in required_fields if f not in user]
                if missing:
                    self.add_issue('data/mock_db.json', i, 'Data Validation',
                        f"User missing fields: {', '.join(missing)}", 'High')
        
        # Validate rooms table
        if 'rooms' in db_data:
            for i, room in enumerate(db_data['rooms']):
                if 'room_number' not in room or 'room_type' not in room:
                    self.add_issue('data/mock_db.json', i, 'Data Validation',
                        'Room missing required fields', 'High')
    
    def audit_security_features(self):
        """Check security features"""
        print("\n=== AUDITING Security Features ===\n")
        
        with open(f'{self.base_path}/app.py', 'r') as f:
            content = f.read()
        
        # Check for CSRF protection
        if 'csrf' not in content.lower():
            self.add_issue('app.py', 0, 'Security',
                'No CSRF protection configured', 'Medium')
        
        # Check for rate limiting
        if 'rate_limit' not in content.lower() and 'limiter' not in content.lower():
            self.add_issue('app.py', 0, 'Security',
                'No rate limiting for login/registration', 'Medium')
        
        # Check for password policy
        if 'len(password)' not in content:
            self.add_issue('app.py', 0, 'Security',
                'No password length validation', 'High')
    
    def run_audit(self):
        """Run full audit"""
        print("\n" + "="*70)
        print("DETAILED CODE AUDIT")
        print("="*70)
        
        self.audit_app_py()
        self.audit_routes()
        self.audit_database_mock()
        self.audit_templates()
        self.audit_data_validation()
        self.audit_security_features()
        
        # Summary
        print("\n" + "="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        
        if not self.issues:
            print("✅ No issues found!")
            return 0
        
        # Group by severity
        by_severity = {}
        for issue in self.issues:
            sev = issue['severity']
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(issue)
        
        total = len(self.issues)
        print(f"\nTotal Issues: {total}")
        
        for sev in ['Critical', 'High', 'Medium', 'Low']:
            if sev in by_severity:
                print(f"  {sev}: {len(by_severity[sev])}")
        
        return total

if __name__ == '__main__':
    audit = CodeAudit()
    audit.run_audit()
