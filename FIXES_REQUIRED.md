# Detailed Fixes Required - Hostel Management System

## CRITICAL FIX #1: Room Allocation - Undefined Variable

**File:** `routes/admin_routes.py`  
**Lines:** 371-390  
**Severity:** CRITICAL  
**Category:** Logic Error (NameError)

### Current Code (BROKEN):
```python
# Get available rooms with occupancy info
cursor.execute("""
    SELECT r.id, r.room_number, r.room_type, r.capacity,
           COUNT(ro.id) as occupied_count
    FROM rooms r
    LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
    GROUP BY r.id
    HAVING occupied_count < r.capacity
    ORDER BY r.room_number
""")
available_rooms = cursor.fetchall() or []

# BUG: 'all_rooms' is undefined - this code never ran above!
available_rooms = []
for room in all_rooms:  # ← NameError: name 'all_rooms' is not defined
    room_id = int(room.get('id')) if isinstance(room.get('id'), str) else room.get('id')
    cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = %s AND status = 'Active'", (room_id,))
    count_result = cursor.fetchone()
    occupied = count_result.get('count', 0) if count_result else 0
    capacity = room.get('capacity', 0)
    
    if occupied < capacity:
        room['occupied_count'] = occupied
        available_rooms.append(room)
```

### Fixed Code:
```python
# Get all rooms first
cursor.execute("SELECT * FROM rooms ORDER BY room_number")
all_rooms = cursor.fetchall() or []

# Filter available rooms with occupancy info
available_rooms = []
for room in all_rooms:
    room_id = int(room.get('id')) if isinstance(room.get('id'), str) else room.get('id')
    cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = %s AND status = 'Active'", (room_id,))
    count_result = cursor.fetchone()
    occupied = count_result.get('count', 0) if count_result else 0
    capacity = int(room.get('capacity', 0)) if room.get('capacity') else 0
    
    if capacity > 0 and occupied < capacity:  # Added capacity > 0 validation
        room['occupied_count'] = occupied
        room['capacity'] = capacity
        available_rooms.append(room)
```

---

## CRITICAL FIX #2: Hardcoded Database Credentials

**File:** `config/database.py`  
**Lines:** 10-20  
**Severity:** CRITICAL  
**Category:** Security (Information Disclosure)

### Current Code (INSECURE):
```python
def connect(self):
    """Connect to MySQL with error handling"""
    try:
        # Direct connection to localhost
        self.connection = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',  # ← HARDCODED EMPTY PASSWORD
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=cursors.DictCursor,
            autocommit=True,
            port=3306
        )
```

### Fixed Code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

def connect(self):
    """Connect to MySQL with error handling"""
    try:
        # Get credentials from environment variables
        self.connection = MySQLdb.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'hostel_management'),
            charset='utf8mb4',
            cursorclass=cursors.DictCursor,
            autocommit=False,  # Changed: better transaction control
            port=int(os.getenv('MYSQL_PORT', 3306))
        )
        self.is_connected = True
        return self.connection
        
    except MySQLdb.Error as e:
        print(f"✗ Database connection failed: {e}")
        self.is_connected = False
        self.connection = None
        return None
```

### Required .env file:
```
FLASK_ENV=development
SECRET_KEY=change_this_to_random_key_production
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DB=hostel_management
MYSQL_PORT=3306
```

---

## CRITICAL FIX #3: Missing Access Control Decorator

**File:** `routes/admin_routes.py`  
**Lines:** 277-278  
**Severity:** CRITICAL  
**Category:** Authorization Bypass

### Current Code (VULNERABLE):
```python
@admin_bp.route('/remove-student/<int:occupancy_id>', methods=['POST'])
@login_required  # ← Only checks if logged in
@admin_required  # ← THIS DECORATOR IS PRESENT but code still wrong
def remove_student(occupancy_id):
```

**WAIT - Actually this HAS the decorator. The issue is elsewhere. Check `shift_student` route:**

```python
@admin_bp.route('/shift-student/<int:occupancy_id>/<int:current_room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def shift_student(occupancy_id, current_room_id):
```

Actually both are correct. **This needs verification - skip this fix.**

---

## CRITICAL FIX #4: Duplicate Route Decorator

**File:** `routes/student_routes.py`  
**Lines:** 11-13  
**Severity:** CRITICAL  
**Category:** Code Error

### Current Code (WRONG):
```python
@student_bp.route('/dashboard')
@student_bp.route('/dashboard')  # ← DUPLICATE
@login_required
def dashboard():
```

### Fixed Code:
```python
@student_bp.route('/dashboard')
@login_required
def dashboard():
```

---

## CRITICAL FIX #5: Unsafe Password Hash Comparison

**File:** `app.py`  
**Lines:** 169-177  
**Severity:** CRITICAL  
**Category:** Authentication Bypass

### Current Code (UNRELIABLE):
```python
if user_data:
    stored_hash = user_data['password_hash']
    # Convert $2y$ (PHP format) to $2b$ (Python format) if needed
    if stored_hash.startswith('$2y$'):
        stored_hash = '$2b$' + stored_hash[4:]  # ← DANGEROUS conversion
    
    # Check password
    try:
        password_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    except ValueError as hash_error:
        print(f"[LOGIN] Hash verification error: {hash_error}", file=sys.stderr, flush=True)
        password_valid = False
    
    if password_valid:
        # Login success
```

### Fixed Code:
```python
if user_data:
    stored_hash = user_data['password_hash']
    
    try:
        # Don't convert PHP format - regenerate password
        # Python bcrypt can handle both $2b$ and $2y$ in recent versions
        password_valid = bcrypt.checkpw(
            password.encode('utf-8'), 
            stored_hash.encode('utf-8')
        )
        
        if password_valid:
            user = User(user_data['id'], user_data['username'], 
                       user_data['email'], user_data['role'], user_data['full_name'])
            login_user(user, remember=True)
            flash(f'Welcome, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Log failed attempt
            print(f"[LOGIN] Invalid password for user: {username}", file=sys.stderr, flush=True)
            flash('Invalid username or password.', 'danger')
            
    except (ValueError, TypeError) as hash_error:
        print(f"[LOGIN] Hash verification error for {username}: {hash_error}", file=sys.stderr, flush=True)
        flash('Authentication error. Please try again.', 'danger')
else:
    flash('Invalid username or password.', 'danger')
```

---

## CRITICAL FIX #6: Incomplete SQL Database File

**File:** `config/database.sql`  
**Lines:** 236+ (End of file)  
**Severity:** CRITICAL  
**Category:** Syntax Error

### Current Code (INCOMPLETE):
```sql
INSERT INTO users (username, email, password_hash, role, full_name, phone, is_active) VALUES
('admin', 'admin@hostel.com', '$2b$12$...', 'admin', 'Admin User', '9000000001', TRUE),
('warden', 'warden@hostel.com', '$2b$12$...', 'warden', 'Hostel Warden', '9000000002', TRUE),
('prajwal', 'prajwal@student.com', '$2b$12$...', 'student', 'Prajwal Tandekar', '9876543210', TRUE),
-- STOPS HERE - NO COMMA, NO MORE STUDENTS
```

### Fixed Code:
```sql
INSERT INTO users (username, email, password_hash, role, full_name, phone, is_active) VALUES
('admin', 'admin@hostel.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'admin', 'Admin User', '9000000001', TRUE),
('warden', 'warden@hostel.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'warden', 'Hostel Warden', '9000000002', TRUE),
('prajwal', 'prajwal@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Prajwal Tandekar', '9876543210', TRUE),
('rajdeep', 'rajdeep@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rajdeep Patil', '9123456789', TRUE),
('rutuja', 'rutuja@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rutuja Patil', '9876123450', TRUE);
```

---

## CRITICAL FIX #7: Missing Connection Validation - Gallery Route

**File:** `app.py`  
**Lines:** 274-284  
**Severity:** CRITICAL  
**Category:** Runtime Error (AttributeError)

### Current Code (WILL CRASH):
```python
@app.route('/gallery')
def gallery():
    cursor = db.connection.cursor()  # ← db.connection can be None!
    cursor.execute("""
        SELECT * FROM gallery 
        ORDER BY display_order ASC, created_at DESC
    """)
    images = cursor.fetchall()
    cursor.close()
    return render_template('gallery.html', images=images)
```

### Fixed Code:
```python
@app.route('/gallery')
def gallery():
    try:
        # Ensure database connection
        if db.connection is None or not db.is_connected:
            db.connect()
        
        if db.connection is None:
            flash('Database unavailable. Please try again later.', 'warning')
            return render_template('gallery.html', images=[])
        
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT * FROM gallery 
            ORDER BY display_order ASC, created_at DESC
        """)
        images = cursor.fetchall()
        cursor.close()
        return render_template('gallery.html', images=images or [])
        
    except Exception as e:
        print(f"Gallery error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        flash('Error loading gallery. Please try again later.', 'warning')
        return render_template('gallery.html', images=[])
```

---

## CRITICAL FIX #8: Catch-All Exception Handler

**File:** `app.py`  
**Lines:** 12-16  
**Severity:** CRITICAL  
**Category:** Exception Handling

### Current Code (HIDES ALL ERRORS):
```python
try:
    from config.database import db
    print("✓ Using MySQL database")
except:  # ← Catches EVERYTHING
    print("✗ MySQL unavailable, using mock database")
    from config.database_mock import db
```

### Fixed Code:
```python
import sys

try:
    from config.database import db
    print("✓ Using MySQL database")
except ImportError as e:
    print(f"✗ MySQL module not available: {e}")
    sys.exit(1)
except FileNotFoundError as e:
    print(f"✗ Database configuration file not found: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error loading database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# If we reach here, db is successfully imported
if db is None:
    print("✗ Database initialization failed")
    sys.exit(1)
```

---

## CRITICAL FIX #9: Missing Input Validation - Numeric Conversion

**File:** `routes/admin_routes.py`  
**Lines:** 347-358  
**Severity:** CRITICAL  
**Category:** Data Validation

### Current Code (UNSAFE):
```python
try:
    student_id = int(request.form.get('student_id', 0))
    room_id = int(request.form.get('room_id', 0))
    
    # No validation that IDs are > 0
    if student_id == 0 or room_id == 0:
        # This won't be caught!
        pass
    
    # ...later...
    room_capacity = room.get('capacity', 0) if isinstance(room, dict) else room[2] if isinstance(room, tuple) else 0
    
    if current_count >= room_capacity:  # ← Can be 0!
        flash(f'This room is at full capacity ({current_count}/{room_capacity} occupied).')
```

### Fixed Code:
```python
try:
    student_id = int(request.form.get('student_id', 0))
    room_id = int(request.form.get('room_id', 0))
    check_in_date = request.form.get('check_in_date', '').strip()
    
    # Validate IDs
    if not student_id or not room_id:
        flash('Please select both a student and a room.', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    if check_in_date:
        # Validate date format
        try:
            datetime.strptime(check_in_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('admin.allocate_room'))
    else:
        check_in_date = datetime.now().strftime('%Y-%m-%d')
    
    # Get room info with validation
    cursor.execute("SELECT capacity FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        flash('Room not found.', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    room_capacity = int(room.get('capacity', 0))
    
    if room_capacity <= 0:
        flash('Invalid room configuration.', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    # Count active occupants
    cursor.execute("""
        SELECT COUNT(*) as count FROM room_occupancy 
        WHERE room_id = %s AND status = 'Active'
    """, (room_id,))
    count_result = cursor.fetchone()
    current_count = count_result.get('count', 0) if count_result else 0
    
    if current_count >= room_capacity:
        flash(f'This room is at full capacity ({current_count}/{room_capacity} occupied).', 'danger')
        return redirect(url_for('admin.allocate_room'))
```

---

## HIGH FIX #1: CSRF Protection Implementation

**File:** All routes with POST methods  
**Severity:** HIGH  
**Category:** Security (CSRF)

### Step 1: Update requirements.txt
```
Flask-WTF==1.1.1
```

### Step 2: Update app.py
```python
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = DevelopmentConfig.SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = True  # Enable CSRF
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for tokens

csrf = CSRFProtect(app)
```

### Step 3: Update all HTML forms
```html
<!-- Before -->
<form method="POST" action="/admin/rooms">
    ...
</form>

<!-- After -->
<form method="POST" action="/admin/rooms">
    {{ csrf_token() }}  <!-- Add this -->
    ...
</form>
```

### Step 4: Add CSRF token to base template
```html
<!-- In templates/base.html -->
<meta name="csrf-token" content="{{ csrf_token() }}">
```

---

## HIGH FIX #2: Input Validation - Visitor Request Form

**File:** `routes/student_routes.py`  
**Lines:** 96-120  
**Severity:** HIGH  
**Category:** Data Validation

### Current Code (NO VALIDATION):
```python
visitor_name = request.form.get('visitor_name', '').strip()
visitor_phone = request.form.get('visitor_phone', '').strip()
visitor_relation = request.form.get('visitor_relation', '').strip()
visit_date = request.form.get('visit_date', '').strip()
visit_time = request.form.get('visit_time', '').strip()
expected_departure = request.form.get('expected_departure', '').strip()
purpose = request.form.get('purpose', '').strip()

if not all([visitor_name, visit_date, visit_time, purpose]):
    # Only checks if empty
    flash('All required fields must be filled.', 'danger')
```

### Fixed Code:
```python
import re
from datetime import datetime

visitor_name = request.form.get('visitor_name', '').strip()
visitor_phone = request.form.get('visitor_phone', '').strip()
visitor_relation = request.form.get('visitor_relation', '').strip()
visit_date = request.form.get('visit_date', '').strip()
visit_time = request.form.get('visit_time', '').strip()
expected_departure = request.form.get('expected_departure', '').strip()
purpose = request.form.get('purpose', '').strip()

# Validation
if not all([visitor_name, visit_date, visit_time, purpose]):
    flash('All required fields must be filled.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate visitor name (max 100 chars, no special chars)
if len(visitor_name) > 100 or not re.match(r"^[a-zA-Z\s'-]+$", visitor_name):
    flash('Invalid visitor name. Use letters, spaces, hyphens, or apostrophes.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate phone (10 digits)
if visitor_phone and not re.match(r'^\d{10}$', visitor_phone.replace('-', '').replace(' ', '')):
    flash('Invalid phone number. Use 10 digits.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate relation
valid_relations = ['Father', 'Mother', 'Brother', 'Sister', 'Relative', 'Friend', 'Guardian', 'Other']
if visitor_relation and visitor_relation not in valid_relations:
    flash('Invalid visitor relation.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate dates
try:
    visit_date_obj = datetime.strptime(visit_date, '%Y-%m-%d').date()
    if visit_date_obj < datetime.now().date():
        flash('Visit date cannot be in the past.', 'danger')
        return redirect(url_for('student.visitors'))
except ValueError:
    flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate times
try:
    visit_time_obj = datetime.strptime(visit_time, '%H:%M').time()
    if expected_departure:
        expected_departure_obj = datetime.strptime(expected_departure, '%H:%M').time()
        if expected_departure_obj <= visit_time_obj:
            flash('Departure time must be after visit time.', 'danger')
            return redirect(url_for('student.visitors'))
except ValueError:
    flash('Invalid time format. Use HH:MM.', 'danger')
    return redirect(url_for('student.visitors'))

# Validate purpose (max 255 chars)
if len(purpose) > 255 or not purpose.strip():
    flash('Invalid purpose. Maximum 255 characters.', 'danger')
    return redirect(url_for('student.visitors'))

# All validation passed - proceed with insert
```

---

## HIGH FIX #3: Payment Calculation Precision

**File:** `routes/admin_routes.py`  
**Lines:** 475-495  
**Severity:** HIGH  
**Category:** Financial Data

### Current Code (FLOATING POINT):
```python
new_pending = fee_info['pending_amount'] - float(amount_paid)
if new_pending <= 0:
    status = 'Paid'
elif new_pending < fee_info['pending_amount']:
    status = 'Partial'
else:
    status = 'Pending'
```

### Fixed Code:
```python
from decimal import Decimal, ROUND_HALF_UP

# Ensure all values are Decimal
pending_amount = Decimal(str(fee_info['pending_amount']))
amount_paid = Decimal(str(request.form.get('amount_paid', 0)))

# Validate payment amount
if amount_paid <= 0:
    flash('Payment amount must be greater than zero.', 'danger')
    return redirect(url_for('admin.fees'))

if amount_paid > pending_amount:
    flash(f'Payment amount cannot exceed pending amount (₹{pending_amount}).', 'danger')
    return redirect(url_for('admin.fees'))

# Calculate new pending with proper rounding
new_pending = (pending_amount - amount_paid).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Determine status
if new_pending <= 0:
    status = 'Paid'
    new_pending = Decimal('0.00')
elif new_pending < pending_amount:
    status = 'Partial'
else:
    status = 'Pending'

# Update database with Decimal values
cursor.execute("""
    UPDATE fees 
    SET paid_amount = paid_amount + %s,
        pending_amount = %s,
        payment_status = %s,
        last_payment_date = NOW()
    WHERE id = %s
""", (str(amount_paid), str(new_pending), status, fee_id))
```

---

## IMPLEMENTATION ORDER

**Day 1 - CRITICAL (4 hours):**
1. Fix duplicate route (CRITICAL FIX #4)
2. Fix undefined variable in room allocation (CRITICAL FIX #1)
3. Complete SQL file (CRITICAL FIX #6)
4. Test basic functionality

**Day 2 - SECURITY (4 hours):**
1. Remove hardcoded credentials (CRITICAL FIX #2)
2. Add connection validation (CRITICAL FIX #7)
3. Fix exception handler (CRITICAL FIX #8)
4. Fix password hash comparison (CRITICAL FIX #5)

**Day 3 - VALIDATION (4 hours):**
1. Add input validation (CRITICAL FIX #9)
2. Add CSRF protection (HIGH FIX #1)
3. Add visitor validation (HIGH FIX #2)
4. Fix payment calculations (HIGH FIX #3)

**Day 4 - TESTING:**
1. Full regression testing
2. Security testing
3. Load testing

---

**Total Estimated Fix Time:** 12-16 hours
