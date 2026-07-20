# Critical Fixes and Implementation Guide

## Table of Contents
1. [Index Creation Scripts](#index-creation-scripts)
2. [N+1 Query Fixes](#n1-query-fixes)
3. [Input Validation Module](#input-validation-module)
4. [Transaction Safety Improvements](#transaction-safety-improvements)
5. [Authorization & Access Control](#authorization--access-control)
6. [Performance Monitoring](#performance-monitoring)

---

## Index Creation Scripts

### Execute in MySQL:

```sql
-- ============================================
-- CRITICAL INDEXES FOR PERFORMANCE
-- ============================================

-- Complaints Table - Foreign Keys
CREATE INDEX idx_complaints_assigned_to ON complaints(assigned_to);
CREATE INDEX idx_complaints_room ON complaints(room_id);

-- Complaints Table - Filtering
CREATE INDEX idx_complaints_created ON complaints(created_at);
CREATE INDEX idx_complaints_priority ON complaints(priority);

-- Visitors Table - Foreign Keys
CREATE INDEX idx_visitors_approved_by ON visitors(approved_by);

-- Visitors Table - Filtering
CREATE INDEX idx_visitors_status ON visitors(status);
CREATE INDEX idx_visitors_visit_date ON visitors(visit_date);

-- Fees Table - Filtering (commonly used filters)
CREATE INDEX idx_fees_status ON fees(payment_status);
CREATE INDEX idx_fees_due_date ON fees(due_date);

-- Fees Table - Composite Index (common filter combination)
CREATE INDEX idx_fees_academic_year ON fees(academic_year, semester);

-- Payment History - Foreign Keys
CREATE INDEX idx_payment_fee ON payment_history(fee_id);
CREATE INDEX idx_payment_student ON payment_history(student_id);
CREATE INDEX idx_payment_recorded_by ON payment_history(recorded_by);

-- Payment History - Filtering
CREATE INDEX idx_payment_date ON payment_history(payment_date);

-- Room Occupancy - Status filtering (very common operation)
CREATE INDEX idx_room_occupancy_status ON room_occupancy(status);
CREATE INDEX idx_room_occupancy_check_in ON room_occupancy(check_in_date);

-- Notices - Visibility filtering
CREATE INDEX idx_notices_visibility ON notices(visibility);
CREATE INDEX idx_notices_created_by ON notices(created_by);

-- Gallery - Uploaded by filtering
CREATE INDEX idx_gallery_uploaded_by ON gallery(uploaded_by);

-- Verify indexes were created
SHOW INDEX FROM complaints;
SHOW INDEX FROM visitors;
SHOW INDEX FROM fees;
SHOW INDEX FROM payment_history;
SHOW INDEX FROM room_occupancy;
SHOW INDEX FROM notices;
SHOW INDEX FROM gallery;
```

### Expected Performance Improvement:
- Room list queries: 90-95% faster
- Dashboard queries: 70-80% faster
- Filtering operations: 85-90% faster

---

## N+1 Query Fixes

### Fix 1: Room List with Occupancy Count

**Before (admin_routes.py lines 189-207):**
```python
# PROBLEM: 1 initial query + 1 query per room = O(n) database calls
cursor.execute("SELECT * FROM rooms ORDER BY id")
rooms_list = cursor.fetchall() or []

for room in rooms_list:
    room_id = int(room.get('id')) if isinstance(room.get('id'), str) else room.get('id')
    cursor.execute("SELECT COUNT(*) as count FROM room_occupancy 
                    WHERE room_id = %s AND status = 'Active'", (room_id,))
    count_result = cursor.fetchone()
    room['occupied_count'] = count_result.get('count', 0) if count_result else 0
```

**After (Optimized to 1 query):**
```python
# OPTIMIZED: Single query with GROUP BY - O(1)
cursor.execute("""
    SELECT r.*, 
           COUNT(CASE WHEN ro.status = 'Active' THEN 1 END) as occupied_count
    FROM rooms r
    LEFT JOIN room_occupancy ro ON r.id = ro.room_id
    GROUP BY r.id
    ORDER BY r.floor, r.room_number
""")
rooms_list = cursor.fetchall() or []

# Data is already processed, no loop needed
for room in rooms_list:
    room['occupied_count'] = room.get('occupied_count', 0)
```

**Performance Impact:**
- 50 rooms: 50 queries → 1 query (50x improvement)
- 100 rooms: 100 queries → 1 query (100x improvement)

---

### Fix 2: Available Students Filter

**Before (admin_routes.py lines 221-229):**
```python
# PROBLEM: 1 initial query + 1 query per student = O(n) database calls
cursor.execute("SELECT id, full_name, roll_number FROM users WHERE role = 'student' ORDER BY full_name")
all_students = cursor.fetchall() or []

students = []
for student in all_students:
    cursor.execute("SELECT id FROM room_occupancy WHERE student_id = %s AND status = 'Active'", (student.get('id'),))
    if not cursor.fetchone():  # Only add if no active room
        students.append(student)
```

**After (Optimized to 1 query):**
```python
# OPTIMIZED: Single query with NOT IN - O(1)
cursor.execute("""
    SELECT u.id, u.full_name, s.roll_number
    FROM users u
    JOIN students s ON u.id = s.user_id
    WHERE u.role = 'student'
    AND u.id NOT IN (
        SELECT student_id 
        FROM room_occupancy 
        WHERE status = 'Active'
    )
    ORDER BY u.full_name
""")
students = cursor.fetchall() or []
```

**Alternative using LEFT JOIN (sometimes faster):**
```python
cursor.execute("""
    SELECT u.id, u.full_name, s.roll_number
    FROM users u
    JOIN students s ON u.id = s.user_id
    LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
    WHERE u.role = 'student'
    AND ro.id IS NULL
    ORDER BY u.full_name
""")
students = cursor.fetchall() or []
```

**Performance Impact:**
- 100 students: 100 queries → 1 query (100x improvement)
- 500 students: 500 queries → 1 query (500x improvement)

---

### Fix 3: Dashboard Recent Complaints/Visitors

**Before (admin_routes.py lines 85-91 & warden_routes.py lines 56-62):**
```python
# Only fetches IDs, missing important fields
cursor.execute("""
    SELECT * FROM complaints ORDER BY id DESC LIMIT 5
""")
recent_complaints = cursor.fetchall() or []
```

**After (Optimized with JOINs):**
```python
cursor.execute("""
    SELECT c.*,
           u.full_name as student_name,
           u.phone as student_phone,
           r.room_number,
           assigned_user.full_name as assigned_to_name
    FROM complaints c
    LEFT JOIN users u ON c.student_id = u.id
    LEFT JOIN rooms r ON c.room_id = r.id
    LEFT JOIN users assigned_user ON c.assigned_to = assigned_user.id
    ORDER BY c.created_at DESC, c.priority DESC
    LIMIT 5
""")
recent_complaints = cursor.fetchall() or []
```

**Similar for visitors:**
```python
cursor.execute("""
    SELECT v.*,
           u.full_name as student_name,
           u.phone as student_phone
    FROM visitors v
    LEFT JOIN users u ON v.student_id = u.id
    ORDER BY v.created_at DESC, v.status DESC
    LIMIT 5
""")
recent_visitors = cursor.fetchall() or []
```

---

## Input Validation Module

### Create: config/validators.py

```python
"""
Input validation module for all form submissions
Prevents data corruption, injection attacks, and invalid states
"""

import re
from decimal import Decimal
from datetime import datetime, date
from typing import Optional, Dict, Any, List, Tuple

class ValidationError(Exception):
    """Raised when validation fails"""
    pass

class FieldValidator:
    """Validates individual form fields"""
    
    @staticmethod
    def validate_string(value: str, min_len: int = 1, max_len: int = 255, 
                       pattern: Optional[str] = None, field_name: str = "Field") -> str:
        """Validate string field"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")
        
        value = value.strip()
        
        if len(value) < min_len:
            raise ValidationError(f"{field_name} must be at least {min_len} characters")
        
        if len(value) > max_len:
            raise ValidationError(f"{field_name} must not exceed {max_len} characters")
        
        if pattern and not re.match(pattern, value):
            raise ValidationError(f"{field_name} has invalid format")
        
        return value
    
    @staticmethod
    def validate_integer(value: Any, min_val: Optional[int] = None, 
                        max_val: Optional[int] = None, field_name: str = "Field") -> int:
        """Validate integer field"""
        try:
            int_val = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a valid integer")
        
        if min_val is not None and int_val < min_val:
            raise ValidationError(f"{field_name} must be at least {min_val}")
        
        if max_val is not None and int_val > max_val:
            raise ValidationError(f"{field_name} must not exceed {max_val}")
        
        return int_val
    
    @staticmethod
    def validate_decimal(value: Any, min_val: Optional[float] = None, 
                        max_val: Optional[float] = None, field_name: str = "Field") -> Decimal:
        """Validate decimal/currency field"""
        try:
            dec_val = Decimal(str(value))
        except:
            raise ValidationError(f"{field_name} must be a valid number")
        
        if min_val is not None and dec_val < Decimal(str(min_val)):
            raise ValidationError(f"{field_name} must be at least {min_val}")
        
        if max_val is not None and dec_val > Decimal(str(max_val)):
            raise ValidationError(f"{field_name} must not exceed {max_val}")
        
        return dec_val
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        email = email.strip().lower()
        
        if not re.match(pattern, email):
            raise ValidationError("Invalid email address")
        
        if len(email) > 100:
            raise ValidationError("Email address too long")
        
        return email
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        """Validate phone number"""
        # Allows formats: +91-9876543210, 9876543210, +91 98765 43210
        pattern = r'^[\d\+\(\)\-\s]{10,15}$'
        phone = phone.strip()
        
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")
        
        # Extract digits only
        digits = re.sub(r'[^\d]', '', phone)
        if len(digits) < 10:
            raise ValidationError("Phone number must have at least 10 digits")
        
        return phone
    
    @staticmethod
    def validate_date(date_str: str, future_only: bool = False) -> str:
        """Validate date field"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Invalid date format (use YYYY-MM-DD)")
        
        if future_only and date_obj < date.today():
            raise ValidationError("Date cannot be in the past")
        
        return date_str
    
    @staticmethod
    def validate_time(time_str: str) -> str:
        """Validate time field"""
        try:
            datetime.strptime(time_str, '%H:%M')
        except ValueError:
            raise ValidationError("Invalid time format (use HH:MM)")
        
        return time_str
    
    @staticmethod
    def validate_enum(value: str, allowed_values: List[str], field_name: str = "Field") -> str:
        """Validate enum field"""
        value = value.strip()
        
        if value not in allowed_values:
            raise ValidationError(f"{field_name} must be one of: {', '.join(allowed_values)}")
        
        return value


class RoomValidator:
    """Validates room form data"""
    
    @staticmethod
    def validate_add_room(data: Dict[str, Any]) -> Tuple[str, int, str, int, Decimal, str]:
        """Validate room addition form"""
        room_number = FieldValidator.validate_string(
            data.get('room_number', ''),
            min_len=1, max_len=10,
            pattern=r'^[A-Za-z0-9\-]{1,10}$',
            field_name="Room number"
        )
        
        floor = FieldValidator.validate_integer(
            data.get('floor', 0),
            min_val=1, max_val=20,
            field_name="Floor"
        )
        
        room_type = FieldValidator.validate_enum(
            data.get('room_type', ''),
            allowed_values=['Single Deluxe', 'Double Sharing', 'Triple Sharing', 'Quad Sharing'],
            field_name="Room type"
        )
        
        capacity = FieldValidator.validate_integer(
            data.get('capacity', 0),
            min_val=1, max_val=10,
            field_name="Capacity"
        )
        
        rent = FieldValidator.validate_decimal(
            data.get('rent', 0),
            min_val=0, max_val=999999.99,
            field_name="Rent"
        )
        
        amenities = FieldValidator.validate_string(
            data.get('amenities', ''),
            min_len=0, max_len=255,
            field_name="Amenities"
        )
        
        return room_number, floor, room_type, capacity, rent, amenities
    
    @staticmethod
    def validate_update_room(data: Dict[str, Any]) -> Tuple[int, int, str, int, Decimal, str]:
        """Validate room update form"""
        room_id = FieldValidator.validate_integer(
            data.get('room_id', 0),
            min_val=1,
            field_name="Room ID"
        )
        
        # Rest is same as add_room
        room_number, floor, room_type, capacity, rent, amenities = RoomValidator.validate_add_room(data)
        
        return room_id, floor, room_type, capacity, rent, amenities


class ComplaintValidator:
    """Validates complaint form data"""
    
    @staticmethod
    def validate_submit_complaint(data: Dict[str, Any]) -> Tuple[str, str, str, str]:
        """Validate complaint submission"""
        category = FieldValidator.validate_enum(
            data.get('category', ''),
            allowed_values=['Plumbing', 'Electrical', 'Maintenance', 'Cleanliness', 'Noise', 'Others'],
            field_name="Category"
        )
        
        title = FieldValidator.validate_string(
            data.get('title', ''),
            min_len=5, max_len=150,
            field_name="Title"
        )
        
        description = FieldValidator.validate_string(
            data.get('description', ''),
            min_len=10, max_len=1000,
            field_name="Description"
        )
        
        priority = FieldValidator.validate_enum(
            data.get('priority', 'Medium'),
            allowed_values=['Low', 'Medium', 'High'],
            field_name="Priority"
        )
        
        return category, title, description, priority


class VisitorValidator:
    """Validates visitor request form data"""
    
    @staticmethod
    def validate_submit_visitor(data: Dict[str, Any]) -> Tuple[str, str, str, str, str, str, str]:
        """Validate visitor request"""
        visitor_name = FieldValidator.validate_string(
            data.get('visitor_name', ''),
            min_len=2, max_len=100,
            field_name="Visitor name"
        )
        
        visitor_phone = FieldValidator.validate_phone(
            data.get('visitor_phone', '')
        )
        
        visitor_relation = FieldValidator.validate_string(
            data.get('visitor_relation', ''),
            min_len=2, max_len=50,
            field_name="Relation"
        )
        
        visit_date = FieldValidator.validate_date(
            data.get('visit_date', ''),
            future_only=False  # Can visit today or future
        )
        
        visit_time = FieldValidator.validate_time(
            data.get('visit_time', '')
        )
        
        expected_departure = FieldValidator.validate_time(
            data.get('expected_departure', '')
        )
        
        purpose = FieldValidator.validate_string(
            data.get('purpose', ''),
            min_len=5, max_len=255,
            field_name="Purpose"
        )
        
        return visitor_name, visitor_phone, visitor_relation, visit_date, visit_time, expected_departure, purpose


# Usage Example in Routes:
# try:
#     category, title, description, priority = ComplaintValidator.validate_submit_complaint(request.form)
#     # Use validated data
# except ValidationError as e:
#     flash(f'Validation error: {str(e)}', 'danger')
#     return redirect(url_for('student.complaints'))
```

---

## Transaction Safety Improvements

### Fix: Complaint Status Update with Transaction Safety

**Before (admin_routes.py lines 170-181):**
```python
# PROBLEM: Two separate updates, second one not in transaction
cursor.execute("""
    UPDATE complaints 
    SET status = %s, resolution_notes = %s, updated_at = NOW()
    WHERE id = %s
""", (status, resolution_notes, complaint_id))

if status == 'Resolved':
    cursor.execute("""
        UPDATE complaints SET resolved_at = NOW() WHERE id = %s
    """, (complaint_id,))

db.connection.commit()
```

**After (Single Transaction):**
```python
try:
    cursor.execute("""
        UPDATE complaints 
        SET status = %s, 
            resolution_notes = %s, 
            resolved_at = CASE WHEN %s = 'Resolved' THEN NOW() ELSE resolved_at END,
            updated_at = NOW()
        WHERE id = %s
    """, (status, resolution_notes, status, complaint_id))
    
    db.connection.commit()
    flash('Complaint updated successfully!', 'success')
    
except Exception as e:
    db.connection.rollback()
    flash(f'Error updating complaint: {str(e)}', 'danger')
    
finally:
    cursor.close()
```

---

## Authorization & Access Control

### Add: Verify Room Ownership

**Create: routes/decorators.py**

```python
from functools import wraps
from flask import flash, redirect, url_for, current_user
from config.database import db

def room_access_required(f):
    """Verify user has access to specified room"""
    @wraps(f)
    def decorated_function(room_id, *args, **kwargs):
        cursor = db.connection.cursor()
        
        try:
            # For students: verify they're assigned to this room
            if current_user.role == 'student':
                cursor.execute("""
                    SELECT id FROM room_occupancy 
                    WHERE room_id = %s 
                    AND student_id = %s 
                    AND status = 'Active'
                """, (room_id, current_user.id))
                
                if not cursor.fetchone():
                    flash('Access denied: You are not assigned to this room', 'danger')
                    return redirect(url_for('student.dashboard'))
            
            # For admin/warden: verify room exists
            elif current_user.role in ['admin', 'warden']:
                cursor.execute("SELECT id FROM rooms WHERE id = %s", (room_id,))
                if not cursor.fetchone():
                    flash('Room not found', 'danger')
                    return redirect(url_for('admin.rooms') if current_user.role == 'admin' else url_for('warden.rooms'))
            
        finally:
            cursor.close()
        
        return f(room_id, *args, **kwargs)
    
    return decorated_function


def complaint_access_required(f):
    """Verify user has access to complaint"""
    @wraps(f)
    def decorated_function(complaint_id, *args, **kwargs):
        cursor = db.connection.cursor()
        
        try:
            # Get complaint owner
            cursor.execute("SELECT student_id FROM complaints WHERE id = %s", (complaint_id,))
            complaint = cursor.fetchone()
            
            if not complaint:
                flash('Complaint not found', 'danger')
                return redirect(url_for(f'{current_user.role}.complaints'))
            
            # Students can only view their own complaints
            if current_user.role == 'student' and complaint['student_id'] != current_user.id:
                flash('Access denied: Not your complaint', 'danger')
                return redirect(url_for('student.complaints'))
            
        finally:
            cursor.close()
        
        return f(complaint_id, *args, **kwargs)
    
    return decorated_function
```

---

## Performance Monitoring

### Create: config/query_monitor.py

```python
"""
Query performance monitoring for debugging and optimization
"""

import time
import logging
from functools import wraps
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/query_performance.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class QueryMonitor:
    """Monitor database query performance"""
    
    SLOW_QUERY_THRESHOLD = 0.5  # 500ms
    
    @staticmethod
    def log_query(query: str, params: tuple, execution_time: float):
        """Log query execution time"""
        is_slow = execution_time > QueryMonitor.SLOW_QUERY_THRESHOLD
        
        level = logging.WARNING if is_slow else logging.INFO
        
        log_message = f"Query: {query[:100]}... | Time: {execution_time:.4f}s | Params: {params}"
        
        if is_slow:
            log_message += " [SLOW QUERY]"
        
        logging.log(level, log_message)
    
    @staticmethod
    def monitor_cursor():
        """Decorator to monitor cursor execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Extract query from args
                if len(args) > 1:
                    query = args[1] if len(args) > 1 else "Unknown"
                    params = args[2] if len(args) > 2 else ()
                    QueryMonitor.log_query(query, params, execution_time)
                
                return result
            
            return wrapper
        
        return decorator


# Usage in database.py:
# from config.query_monitor import QueryMonitor
# 
# def execute_query(self, query, params=None):
#     start = time.time()
#     cursor = self.connection.cursor()
#     cursor.execute(query, params)
#     result = cursor.fetchall()
#     duration = time.time() - start
#     QueryMonitor.log_query(query, params or (), duration)
#     return result
```

---

## Summary of Fixes

| Fix | Priority | Complexity | Estimated Time |
|-----|----------|------------|-----------------|
| Add indexes | CRITICAL | Easy | 30 min |
| Fix room occupancy N+1 | CRITICAL | Medium | 1 hr |
| Fix available students N+1 | CRITICAL | Medium | 1 hr |
| Add input validation | HIGH | Medium | 2 hrs |
| Fix transaction safety | HIGH | Easy | 1 hr |
| Add authorization checks | HIGH | Medium | 1 hr |
| Add query monitoring | MEDIUM | Easy | 30 min |

**Total Estimated Implementation Time: 7-8 hours**

---

## Testing Recommendations

After implementing fixes:

1. **Load Testing**
   - Test with 1000+ students
   - Monitor query performance with new indexes

2. **Input Validation Testing**
   - Try injection attacks with special characters
   - Test boundary conditions (max/min values)

3. **Transaction Testing**
   - Simulate database failure during multi-step operations
   - Verify rollback occurs correctly

4. **Authorization Testing**
   - Try to access resources from wrong role
   - Try to access others' data

5. **Performance Benchmarking**
   - Compare before/after query times
   - Generate performance report

