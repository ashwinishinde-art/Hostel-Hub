"""
Mock Database Layer - Works without MySQL authentication
Uses in-memory data structure with persistence to JSON
"""

import json
import os
from datetime import datetime
import hashlib
import bcrypt

DB_FILE = '/home/prajwal/Programs/Hostel/data/mock_db.json'
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

# Pre-computed bcrypt hash for admin123
PASSWORD_HASH = "$2b$12$fRl39TraAQ4NkUtay2xpJ.XXS7j2LZFUZtgfZBRzWePnfaqt8.vgK"

# Default data structure
DEFAULT_DB = {
    "users": [
        {"id": 1, "username": "admin", "password_hash": PASSWORD_HASH, "role": "admin", "email": "admin@hostel.com", "full_name": "Administrator", "phone": "9876543210", "gender": "Male", "is_active": True, "created_at": "2024-01-01", "updated_at": "2024-01-01"},
        {"id": 2, "username": "prajwal", "password_hash": PASSWORD_HASH, "role": "student", "email": "prajwal@hostel.com", "full_name": "Prajwal Tandekar", "phone": "9876543211", "gender": "Male", "is_active": True, "created_at": "2024-01-01", "updated_at": "2024-01-01"},
        {"id": 3, "username": "rajdeep", "password_hash": PASSWORD_HASH, "role": "student", "email": "rajdeep@hostel.com", "full_name": "Rajdeep Singh", "phone": "9876543212", "gender": "Male", "is_active": True, "created_at": "2024-01-01", "updated_at": "2024-01-01"},
        {"id": 4, "username": "rutuja", "password_hash": PASSWORD_HASH, "role": "student", "email": "rutuja@hostel.com", "full_name": "Rutuja Sharma", "phone": "9876543213", "gender": "Female", "is_active": True, "created_at": "2024-01-01", "updated_at": "2024-01-01"},
        {"id": 5, "username": "warden", "password_hash": PASSWORD_HASH, "role": "warden", "email": "warden@hostel.com", "full_name": "Warden", "phone": "9876543214", "gender": "Male", "is_active": True, "created_at": "2024-01-01", "updated_at": "2024-01-01"},
    ],
    "students": [
        {"id": 1, "user_id": 2, "roll_number": "CSE001", "enrollment_no": "ENR001", "batch": "2024", "department": "CSE", "cgpa": 8.5, "emergency_contact": "9876543215", "emergency_relation": "Father", "guardian_name": "Tandekar Sr."},
        {"id": 2, "user_id": 3, "roll_number": "CSE002", "enrollment_no": "ENR002", "batch": "2024", "department": "CSE", "cgpa": 8.2, "emergency_contact": "9876543216", "emergency_relation": "Mother", "guardian_name": "Singh Sr."},
        {"id": 3, "user_id": 4, "roll_number": "ECE001", "enrollment_no": "ENR003", "batch": "2024", "department": "ECE", "cgpa": 8.8, "emergency_contact": "9876543217", "emergency_relation": "Father", "guardian_name": "Sharma Sr."},
    ],
    "rooms": [
        {"id": 1, "room_number": "101", "room_type": "Single Deluxe", "floor": 1, "capacity": 1, "rent": 5000, "amenities": "AC, Attached Bathroom, WiFi", "status": "occupied"},
        {"id": 2, "room_number": "102", "room_type": "Double Sharing", "floor": 1, "capacity": 2, "rent": 3500, "amenities": "AC, Shared Bathroom, WiFi", "status": "vacant"},
        {"id": 3, "room_number": "201", "room_type": "Triple Sharing", "floor": 2, "capacity": 3, "rent": 2500, "amenities": "Fan, Shared Bathroom, WiFi", "status": "occupied"},
    ],
    "room_occupancy": [
        {"id": 1, "student_id": 1, "room_id": 1, "check_in_date": "2024-01-01", "status": "Active"},
        {"id": 2, "student_id": 2, "room_id": 3, "check_in_date": "2024-01-01", "status": "Active"},
        {"id": 3, "student_id": 3, "room_id": 3, "check_in_date": "2024-01-01", "status": "Active"},
    ],
    "complaints": [
        {"id": 1, "student_id": 1, "category": "Maintenance", "description": "AC not working", "status": "pending", "priority": "high", "created_at": "2024-01-15", "resolution_notes": ""},
        {"id": 2, "student_id": 2, "category": "Cleanliness", "description": "Bathroom not clean", "status": "resolved", "priority": "medium", "created_at": "2024-01-10", "resolution_notes": "Cleaned on 2024-01-11"},
    ],
    "visitors": [
        {"id": 1, "student_id": 1, "visitor_name": "Parent", "purpose": "Visit", "date": "2024-02-01", "time": "10:00", "status": "pending", "approved_by": None},
        {"id": 2, "student_id": 2, "visitor_name": "Friend", "purpose": "Social", "date": "2024-02-02", "time": "14:00", "status": "approved", "approved_by": 5},
    ],
    "fees": [
        {"id": 1, "student_id": 1, "month": "January", "year": 2024, "room_rent": 5000, "mess_charges": 2000, "utilities": 500, "other_charges": 0, "status": "paid", "due_date": "2024-01-31", "paid_date": "2024-01-30"},
        {"id": 2, "student_id": 1, "month": "February", "year": 2024, "room_rent": 5000, "mess_charges": 2000, "utilities": 500, "other_charges": 0, "status": "pending", "due_date": "2024-02-28", "paid_date": None},
    ],
    "notices": [
        {"id": 1, "title": "Water Supply Maintenance", "content": "Water supply will be shut off on Sunday", "category": "Maintenance", "visibility": "all", "created_by": 1, "created_at": "2024-01-20", "is_pinned": 1},
        {"id": 2, "title": "Fee Reminder", "content": "Please pay your fees by month end", "category": "Fees", "visibility": "students", "created_by": 1, "created_at": "2024-01-25", "is_pinned": 0},
    ],
    "gallery": [
        {"id": 1, "title": "Common Room", "description": "Hostel common area", "image_url": "gallery/common_room.jpg", "created_at": "2024-01-01"},
        {"id": 2, "title": "Dining Hall", "description": "Hostel dining area", "image_url": "gallery/dining_hall.jpg", "created_at": "2024-01-01"},
    ],
}

class MockDatabase:
    """Mock database using JSON storage"""
    
    def __init__(self):
        self.data = self.load_data()
        self.is_connected = True
        self.connection = self  # For compatibility with app checks
    
    def load_data(self):
        """Load data from JSON file or use defaults"""
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        # Save default data
        self.save_data(DEFAULT_DB)
        return DEFAULT_DB
    
    def save_data(self, data):
        """Save data to JSON file"""
        try:
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            with open(DB_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_connection(self):
        """Mock get_connection for compatibility"""
        return self
    
    def execute_query(self, query, params=None):
        """Simulate query execution"""
        try:
            # Parse simple SQL queries
            query_lower = query.lower().strip()
            
            # Simple SELECT queries
            if query_lower.startswith("select"):
                return self.parse_select(query, params)
            
            # INSERT queries
            elif "insert into" in query_lower:
                self.parse_insert(query, params)
                return []
            
            # UPDATE queries
            elif query_lower.startswith("update"):
                self.parse_update(query, params)
                return []
            
            # DELETE queries
            elif query_lower.startswith("delete"):
                self.parse_delete(query, params)
                return []
            
            return []
        except Exception as e:
            print(f"Query error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Simulate INSERT/UPDATE/DELETE"""
        try:
            query_lower = query.lower().strip()
            
            if "insert into" in query_lower:
                return self.parse_insert(query, params)
            elif "update" in query_lower:
                return self.parse_update(query, params)
            elif "delete" in query_lower:
                return self.parse_delete(query, params)
            
            return False
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def parse_select_with_join(self, query, params=None):
        """Handle SELECT queries with JOINs"""
        import re
        
        query_lower = query.lower()
        
        # Handle room_occupancy LEFT JOIN rooms query
        if "from room_occupancy" in query_lower and "left join rooms" in query_lower and "where ro.student_id" in query_lower:
            ro_data = self.data.get("room_occupancy", [])
            rooms_data = self.data.get("rooms", [])
            
            result = []
            for ro in ro_data:
                # Check WHERE clause filters
                if params and len(params) >= 1:
                    # Check student_id filter
                    student_id = params[0]
                    if ro.get("student_id") != student_id:
                        continue
                    
                    # Check status filter if there's a second param
                    if len(params) >= 2 and "status" in query_lower:
                        status = params[1]
                        if ro.get("status") != status:
                            continue
                
                # Find corresponding room
                room = None
                for r in rooms_data:
                    if r.get("id") == ro.get("room_id"):
                        room = r
                        break
                
                # Build result row (room info can be None for LEFT JOIN)
                row = {
                    "room_number": room.get("room_number") if room else None,
                    "status": ro.get("status")
                }
                result.append(row)
            
            return result
        
        # Handle users-students JOIN query
        if "from users" in query_lower and "join students" in query_lower and "where u.role = 'student'" in query_lower:
            users_data = self.data.get("users", [])
            students_data = self.data.get("students", [])
            
            result = []
            for user in users_data:
                if user.get("role") != "student":
                    continue
                
                # Find corresponding student record
                student = None
                for s in students_data:
                    if s.get("user_id") == user.get("id"):
                        student = s
                        break
                
                if not student:
                    continue
                
                # Build result row with requested columns
                row = {
                    "id": user.get("id"),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "full_name": user.get("full_name"),
                    "phone": user.get("phone"),
                    "role": user.get("role"),
                    "roll_number": student.get("roll_number"),
                    "branch": student.get("branch", "N/A"),
                    "semester": student.get("semester", "N/A"),
                    "enrollment_no": student.get("enrollment_no", ""),
                    "department": student.get("department", "N/A"),
                    "cgpa": student.get("cgpa", 0.0)
                }
                result.append(row)
            
            # Sort by full_name if present
            if "order by u.full_name" in query_lower or "order by full_name" in query_lower:
                result.sort(key=lambda x: x.get("full_name", ""))
            
            return result
        
        # Handle the specific room_students JOIN query
        if "from room_occupancy" in query_lower and "join users" in query_lower and "join students" in query_lower:
            # Parse the specific columns requested
            select_part = query[query.lower().find("select") + 6:query.lower().find("from")].strip()
            
            # Get room_id from WHERE clause
            room_id = None
            status = None
            if params:
                # Extract room_id and status from WHERE clause
                where_match = re.search(r'where\s+ro\.room_id\s*=\s*%s\s+and\s+ro\.status\s*=\s*%s', query_lower)
                if where_match and len(params) >= 2:
                    room_id = params[0]
                    status = params[1]
                elif "where" in query_lower and len(params) >= 1:
                    room_id = params[0]
                    if len(params) >= 2:
                        status = params[1]
            
            # Get room_occupancy records
            ro_data = self.data.get("room_occupancy", [])
            users_data = self.data.get("users", [])
            students_data = self.data.get("students", [])
            
            result = []
            for ro in ro_data:
                # Filter by room_id
                if room_id is not None and ro.get("room_id") != room_id:
                    continue
                # Filter by status
                if status is not None and ro.get("status") != status:
                    continue
                
                # Find corresponding user
                user = None
                for u in users_data:
                    if u.get("id") == ro.get("student_id"):
                        user = u
                        break
                
                if not user:
                    continue
                
                # Find corresponding student
                student = None
                for s in students_data:
                    if s.get("user_id") == user.get("id"):
                        student = s
                        break
                
                if not student:
                    continue
                
                # Build result row with all requested columns
                row = {
                    "occupancy_id": ro.get("id"),
                    "student_id": user.get("id"),
                    "full_name": user.get("full_name"),
                    "roll_number": student.get("roll_number"),
                    "check_in_date": ro.get("check_in_date"),
                    "status": ro.get("status")
                }
                result.append(row)
            
            # Sort by check_in_date if present
            if "order by ro.check_in_date" in query_lower:
                result.sort(key=lambda x: x.get("check_in_date", ""))
            
            return result
        
        # Handle complaints JOIN with users and optional rooms
        if "from complaints" in query_lower and "join users" in query_lower:
            complaints_data = self.data.get("complaints", [])
            users_data = self.data.get("users", [])
            rooms_data = self.data.get("rooms", [])
            
            result = []
            for complaint in complaints_data:
                # Find corresponding user
                user = None
                for u in users_data:
                    if u.get("id") == complaint.get("student_id"):
                        user = u
                        break
                
                if not user:
                    continue
                
                # Find corresponding room if left join
                room = None
                if complaint.get("room_id"):
                    for r in rooms_data:
                        if r.get("id") == complaint.get("room_id"):
                            room = r
                            break
                
                # Build result row with all requested columns
                row = {
                    "id": complaint.get("id"),
                    "title": complaint.get("title", complaint.get("description", "")),
                    "category": complaint.get("category"),
                    "status": complaint.get("status"),
                    "priority": complaint.get("priority"),
                    "created_at": complaint.get("created_at"),
                    "full_name": user.get("full_name"),
                    "username": user.get("username"),
                    "room_number": room.get("room_number") if room else None
                }
                result.append(row)
            
            # Sort by created_at DESC if present
            if "order by c.created_at desc" in query_lower:
                # Sort in reverse by created_at
                try:
                    from datetime import datetime
                    result.sort(key=lambda x: datetime.fromisoformat(str(x.get("created_at", "")).replace("Z", "+00:00")), reverse=True)
                except:
                    # If date parsing fails, just reverse sort
                    result.reverse()
            
            # Apply LIMIT if present
            if "limit" in query_lower:
                import re
                limit_match = re.search(r'limit\s+(\d+)', query_lower)
                if limit_match:
                    limit = int(limit_match.group(1))
                    result = result[:limit]
            
            return result
        
        # Handle visitors JOIN with users
        if "from visitors" in query_lower and "join users" in query_lower:
            visitors_data = self.data.get("visitors", [])
            users_data = self.data.get("users", [])
            
            result = []
            for visitor in visitors_data:
                # Find corresponding user
                user = None
                for u in users_data:
                    if u.get("id") == visitor.get("student_id"):
                        user = u
                        break
                
                if not user:
                    continue
                
                # Build result row
                row = {
                    "id": visitor.get("id"),
                    "visitor_name": visitor.get("visitor_name"),
                    "visit_date": visitor.get("visit_date") or visitor.get("date"),
                    "status": visitor.get("status"),
                    "purpose": visitor.get("purpose"),
                    "full_name": user.get("full_name"),
                    "username": user.get("username")
                }
                result.append(row)
            
            # Apply LIMIT if present
            if "limit" in query_lower:
                import re
                limit_match = re.search(r'limit\s+(\d+)', query_lower)
                if limit_match:
                    limit = int(limit_match.group(1))
                    result = result[:limit]
            
            return result
        
        # Handle fees JOIN with users and optional students
        if "from fees" in query_lower and "join users" in query_lower:
            fees_data = self.data.get("fees", [])
            users_data = self.data.get("users", [])
            students_data = self.data.get("students", [])
            
            result = []
            for fee in fees_data:
                # Find corresponding user
                user = None
                for u in users_data:
                    if u.get("id") == fee.get("student_id"):
                        user = u
                        break
                
                if not user:
                    continue
                
                # Find corresponding student if left join
                student = None
                for s in students_data:
                    if s.get("user_id") == user.get("id"):
                        student = s
                        break
                
                # Filter by payment status if WHERE clause exists
                if "where" in query_lower and "payment_status" in query_lower:
                    # Check both payment_status and status fields
                    fee_status = fee.get("payment_status") or fee.get("status")
                    if fee_status not in ["Pending", "Overdue", "pending", "overdue"]:
                        continue
                
                # Build result row
                row = {
                    "id": fee.get("id"),
                    "total_amount": fee.get("total_amount") or (
                        (fee.get("room_rent", 0) or 0) + 
                        (fee.get("mess_charges", 0) or 0) + 
                        (fee.get("utilities", 0) or 0) + 
                        (fee.get("other_charges", 0) or 0)
                    ),
                    "paid_amount": fee.get("paid_amount", 0),
                    "pending_amount": fee.get("pending_amount") or (
                        (fee.get("room_rent", 0) or 0) + 
                        (fee.get("mess_charges", 0) or 0) + 
                        (fee.get("utilities", 0) or 0) + 
                        (fee.get("other_charges", 0) or 0) -
                        (fee.get("paid_amount", 0) or 0)
                    ),
                    "payment_status": fee.get("payment_status") or fee.get("status"),
                    "due_date": fee.get("due_date"),
                    "academic_year": fee.get("academic_year") or str(fee.get("year", "")),
                    "semester": fee.get("semester"),
                    "full_name": user.get("full_name"),
                    "username": user.get("username"),
                    "roll_number": student.get("roll_number") if student else None
                }
                result.append(row)
            
            # Apply LIMIT if present
            if "limit" in query_lower:
                import re
                limit_match = re.search(r'limit\s+(\d+)', query_lower)
                if limit_match:
                    limit = int(limit_match.group(1))
                    result = result[:limit]
            
            return result
        
        # Handle notices JOIN with users
        if "from notices" in query_lower and "join users" in query_lower:
            notices_data = self.data.get("notices", [])
            users_data = self.data.get("users", [])
            
            result = []
            for notice in notices_data:
                # Find corresponding user
                user = None
                for u in users_data:
                    if u.get("id") == notice.get("created_by"):
                        user = u
                        break
                
                if not user:
                    continue
                
                # Build result row with all notice data plus user full_name
                row = dict(notice)  # Copy all notice fields
                row["full_name"] = user.get("full_name")
                result.append(row)
            
            # Sort by is_pinned DESC, then created_at DESC
            try:
                result.sort(key=lambda x: (
                    not x.get("is_pinned", False),  # False sorts before True, so negate it
                    -(int(x.get("id", 0)))  # Sort by id descending as proxy for created_at
                ))
            except:
                pass
            
            return result
        
        # Fallback for other JOINs - return empty for now
        return []
    
    def parse_select(self, query, params=None):
        """Parse and execute SELECT"""
        query_lower = query.lower()
        
        # Check if this is a JOIN query
        if " join " in query_lower:
            return self.parse_select_with_join(query, params)
        
        # Handle COUNT(*) queries
        if "count(*)" in query_lower:
            # Extract the alias if present (COUNT(*) as alias_name)
            import re
            alias_match = re.search(r'count\(\*\)\s+as\s+(\w+)', query_lower)
            count_alias = alias_match.group(1) if alias_match else 'count'
            
            # Find table name
            if "from users" in query_lower:
                table = self.data.get("users", [])
            elif "from students" in query_lower:
                table = self.data.get("students", [])
            elif "from rooms" in query_lower:
                table = self.data.get("rooms", [])
            elif "from room_occupancy" in query_lower:
                table = self.data.get("room_occupancy", [])
            elif "from complaints" in query_lower:
                table = self.data.get("complaints", [])
            elif "from visitors" in query_lower:
                table = self.data.get("visitors", [])
            elif "from fees" in query_lower:
                table = self.data.get("fees", [])
            elif "from notices" in query_lower:
                table = self.data.get("notices", [])
            elif "from gallery" in query_lower:
                table = self.data.get("gallery", [])
            else:
                return [{count_alias: 0}]
            
            # Apply WHERE filter if present
            if "where" in query_lower and params:
                result = []
                for row in table:
                    if self.matches_where(row, query_lower, params):
                        result.append(row)
                return [{count_alias: len(result)}]
            
            return [{count_alias: len(table)}]
        
        # Find table name for regular SELECT
        if "from users" in query_lower:
            table_name = "users"
        elif "from students" in query_lower:
            table_name = "students"
        elif "from rooms" in query_lower:
            table_name = "rooms"
        elif "from room_occupancy" in query_lower:
            table_name = "room_occupancy"
        elif "from complaints" in query_lower:
            table_name = "complaints"
        elif "from visitors" in query_lower:
            table_name = "visitors"
        elif "from fees" in query_lower:
            table_name = "fees"
        elif "from notices" in query_lower:
            table_name = "notices"
        elif "from gallery" in query_lower:
            table_name = "gallery"
        else:
            return []
        
        table = self.data.get(table_name, [])
        
        # Parse WHERE clause for conditions
        if "where" in query_lower:
            # Extract WHERE condition and params
            result = []
            for row in table:
                if self.matches_where(row, query_lower, params):
                    result.append(row)
            return result
        
        return table
    
    def matches_where(self, row, query_lower, params):
        """Check if row matches WHERE clause using params"""
        if not params:
            return True
        
        # Handle tuple params (positional)
        if isinstance(params, tuple):
            # Parse WHERE clause to extract field names
            where_idx = query_lower.find("where")
            if where_idx == -1:
                return True
            
            where_part = query_lower[where_idx:]
            
            # Extract all conditions before AND
            conditions = where_part.split(" and ")
            param_idx = 0
            
            for condition in conditions:
                if "=" not in condition:
                    continue
                
                # Extract field name (before =)
                field_part = condition.split("=")[0].strip()
                field = field_part.replace("where", "").strip()
                field = field.split("(")[-1].strip()
                
                # Check if this field matches the parameter
                if param_idx < len(params):
                    if field in row:
                        if row[field] != params[param_idx]:
                            return False
                    param_idx += 1
            
            return True
        
        # Handle dict params
        if isinstance(params, dict):
            for key, val in params.items():
                if key in row and row[key] != val:
                    return False
        
        return True
    
    def parse_insert(self, query, params=None):
        """Parse and execute INSERT"""
        try:
            # Find table name
            import re
            from datetime import datetime
            
            match = re.search(r'INSERT\s+INTO\s+(\w+)', query, re.IGNORECASE)
            if not match:
                return False
            
            table = match.group(1)
            
            if table not in self.data:
                return False
            
            # Generate new ID
            new_id = max([item.get("id", 0) for item in self.data[table]], default=0) + 1
            
            # Create new row with ID
            row = {"id": new_id}
            
            # Extract field names from INSERT query - handle multiline
            fields_match = re.search(r'\((.*?)\)\s*VALUES', query, re.IGNORECASE | re.DOTALL)
            if fields_match and params:
                fields_text = fields_match.group(1)
                # Clean up whitespace and newlines
                fields_text = re.sub(r'\s+', ' ', fields_text)
                fields = [f.strip() for f in fields_text.split(',')]
                
                # Map fields to values
                for i, field in enumerate(fields):
                    if i < len(params):
                        row[field] = params[i]
            
            # Add automatic timestamps for new records
            if 'created_at' not in row:
                # Format as YYYY-MM-DD for consistency with mock DB
                row['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if 'updated_at' not in row and table in ['complaints', 'notices', 'visitors', 'fees', 'rooms']:
                row['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Add the new row to the table
            self.data[table].append(row)
            
            # Save changes
            self.save_data(self.data)
            return True
        except Exception as e:
            print(f"Insert error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def parse_update(self, query, params=None):
        """Parse and execute UPDATE"""
        try:
            import re
            # Find table name
            match = re.search(r'UPDATE\s+(\w+)', query, re.IGNORECASE)
            if not match:
                return False
            
            table = match.group(1)
            if table not in self.data:
                return False
            
            # Extract SET values and WHERE clause
            # Find SET clause
            set_match = re.search(r'SET\s+(.*?)\s+WHERE', query, re.IGNORECASE | re.DOTALL)
            if not set_match or not params:
                return False
            
            set_clause = set_match.group(1)
            # Extract field names from SET clause
            set_fields = [f.strip().split('=')[0].strip() for f in set_clause.split(',')]
            
            # Extract WHERE clause field
            where_match = re.search(r'WHERE\s+(\w+)\s*=', query, re.IGNORECASE)
            if not where_match:
                return False
            
            where_field = where_match.group(1)
            where_value = params[-1]  # Last param is WHERE value
            
            # Update matching rows
            for item in self.data[table]:
                if item.get(where_field) == where_value:
                    # Update fields (all except last which is WHERE)
                    for i, field in enumerate(set_fields):
                        if i < len(params) - 1:
                            item[field] = params[i]
            
            self.save_data(self.data)
            return True
        except Exception as e:
            print(f"Update error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def parse_delete(self, query, params=None):
        """Parse and execute DELETE"""
        try:
            import re
            # Find table name
            match = re.search(r'DELETE\s+FROM\s+(\w+)', query, re.IGNORECASE)
            if not match:
                return False
            
            table = match.group(1)
            if table not in self.data:
                return False
            
            # Find WHERE condition field name
            where_idx = query.lower().find("where")
            if where_idx == -1:
                # DELETE all if no WHERE
                self.data[table] = []
            else:
                where_part = query[where_idx:]
                # Extract field name from WHERE clause
                field_match = re.search(r'where\s+(\w+)\s*=', where_part, re.IGNORECASE)
                if field_match and params:
                    field = field_match.group(1)
                    value = params[0] if isinstance(params, tuple) else params.get(field)
                    
                    # Remove matching rows
                    self.data[table] = [
                        item for item in self.data[table]
                        if item.get(field) != value
                    ]
            
            self.save_data(self.data)
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def close(self):
        """Close connection"""
        pass
    
    def commit(self):
        """Commit changes to database"""
        self.save_data(self.data)
    
    def rollback(self):
        """Rollback changes (reload from file)"""
        self.data = self.load_data()
    
    def cursor(self):
        """Return a cursor-like object"""
        return MockCursor(self)

class MockCursor:
    """Mock cursor for compatibility"""
    
    def __init__(self, db):
        self.db = db
        self.result = None
        self.lastrowid = None
        self.rowcount = 0
    
    def execute(self, query, params=None):
        """Execute query"""
        query_lower = query.lower().strip()
        
        # SELECT query
        if query_lower.startswith("select"):
            self.result = self.db.execute_query(query, params)
            self.rowcount = len(self.result) if self.result else 0
        # INSERT query
        elif "insert into" in query_lower:
            self.db.execute_query(query, params)
            self.result = []
            self.rowcount = 1
            # Get the last inserted ID from the table
            self.lastrowid = self._get_last_id(query)
        # UPDATE/DELETE query
        else:
            self.db.execute_query(query, params)
            self.result = []
            self.rowcount = 1
        
        return self
    
    def _get_last_id(self, query):
        """Get the last inserted ID from a table"""
        import re
        match = re.search(r'INSERT\s+INTO\s+(\w+)', query, re.IGNORECASE)
        if match:
            table = match.group(1)
            if table in self.db.data:
                items = self.db.data[table]
                if items:
                    return items[-1].get('id', 0)
        return 0
    
    def fetchone(self):
        """Fetch one result"""
        if self.result and len(self.result) > 0:
            return self.result[0]
        return None
    
    def fetchall(self):
        """Fetch all results"""
        return self.result or []
    
    def close(self):
        """Close cursor"""
        pass
    
    def commit(self):
        """Commit changes"""
        self.db.save_data(self.db.data)

# Initialize
db = MockDatabase()
