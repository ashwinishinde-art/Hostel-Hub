# Quick Fix Reference - Hostel Management System

## 🚨 CRITICAL - FIX TODAY (45 minutes total)

### 1. Duplicate Route Decorator
**File:** `routes/student_routes.py:12`  
**Time:** 1 minute  
**Action:** Remove line 12 (duplicate `@student_bp.route('/dashboard')`)

```python
# DELETE this line:
@student_bp.route('/dashboard')
```

---

### 2. Undefined Variable NameError
**File:** `routes/admin_routes.py:390`  
**Time:** 5 minutes  
**Action:** Add missing query before loop

```python
# ADD before line 373:
cursor.execute("SELECT * FROM rooms ORDER BY room_number")
all_rooms = cursor.fetchall() or []

# Keep the loop but validate room_capacity > 0
```

---

### 3. Incomplete SQL File
**File:** `config/database.sql:236`  
**Time:** 2 minutes  
**Action:** Add missing students to INSERT

```sql
('rajdeep', 'rajdeep@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rajdeep Patil', '9123456789', TRUE),
('rutuja', 'rutuja@student.com', '$2b$12$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK', 'student', 'Rutuja Patil', '9876123450', TRUE);
```

---

### 4. Connection Check - Gallery Route
**File:** `app.py:274-284`  
**Time:** 5 minutes  
**Action:** Wrap in try-except with connection check

```python
@app.route('/gallery')
def gallery():
    try:
        if db.connection is None or not db.is_connected:
            db.connect()
        if db.connection is None:
            return render_template('gallery.html', images=[])
        # ... rest of code
    except Exception as e:
        print(f"Gallery error: {e}")
        return render_template('gallery.html', images=[])
```

---

### 5. Connection Check - Contact Route
**File:** `app.py:280-288`  
**Time:** 5 minutes  
**Action:** Same pattern as gallery route

```python
@app.route('/contact')
def contact():
    try:
        if db.connection is None or not db.is_connected:
            db.connect()
        if db.connection is None:
            return render_template('contact.html', settings={})
        # ... rest of code
    except Exception as e:
        print(f"Contact error: {e}")
        return render_template('contact.html', settings={})
```

---

### 6. Bare Except Clause
**File:** `app.py:12-16`  
**Time:** 3 minutes  
**Action:** Replace with specific exception handling

```python
try:
    from config.database import db
    print("✓ Using MySQL database")
except (ImportError, FileNotFoundError) as e:
    print(f"✗ Database error: {e}")
    import sys
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import sys
    sys.exit(1)
```

---

### 7. Remove Hardcoded Credentials
**File:** `config/database.py:10-20`  
**Time:** 10 minutes  
**Action:** Replace hardcoded values with environment variables

```python
# ADD at top:
import os
from dotenv import load_dotenv
load_dotenv()

# REPLACE in connect():
self.connection = MySQLdb.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    database=os.getenv('MYSQL_DB', 'hostel_management'),
    # ... rest
)

# CREATE .env file:
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=hostel_management
```

---

### 8. Fix Password Hash Comparison
**File:** `app.py:169-177`  
**Time:** 5 minutes  
**Action:** Remove PHP format conversion, improve error handling

```python
if user_data:
    stored_hash = user_data['password_hash']
    try:
        password_valid = bcrypt.checkpw(
            password.encode('utf-8'), 
            stored_hash.encode('utf-8')
        )
        if password_valid:
            # login success
        else:
            flash('Invalid username or password.', 'danger')
    except (ValueError, TypeError) as e:
        print(f"[LOGIN] Auth error: {e}")
        flash('Authentication error. Please try again.', 'danger')
```

---

## ⚠️ HIGH - FIX THIS WEEK (2 hours total)

### 9. Add CSRF Protection
**File:** All POST forms  
**Time:** 20 minutes  

Step 1: `requirements.txt` - Add:
```
Flask-WTF==1.1.1
```

Step 2: `app.py` - Add after imports:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

Step 3: All HTML forms - Add:
```html
<form method="POST">
    {{ csrf_token() }}
    <!-- rest of form -->
</form>
```

---

### 10. Input Validation - Visitor Form
**File:** `routes/student_routes.py:96-120`  
**Time:** 20 minutes  

```python
import re
from datetime import datetime

# Validate name (letters, spaces, hyphens only)
if not re.match(r"^[a-zA-Z\s'-]+$", visitor_name):
    flash('Invalid name format', 'danger')

# Validate phone (10 digits)
if visitor_phone:
    if not re.match(r'^\d{10}$', visitor_phone.replace('-', '')):
        flash('Phone must be 10 digits', 'danger')

# Validate date (not in past)
try:
    visit_date_obj = datetime.strptime(visit_date, '%Y-%m-%d').date()
    if visit_date_obj < datetime.now().date():
        flash('Date cannot be in past', 'danger')
except ValueError:
    flash('Invalid date format', 'danger')

# Validate length
if len(visitor_name) > 100:
    flash('Name too long', 'danger')
if len(purpose) > 255:
    flash('Purpose too long', 'danger')
```

---

### 11. Use Decimal for Payments
**File:** `routes/admin_routes.py:475-495`  
**Time:** 15 minutes  

```python
from decimal import Decimal, ROUND_HALF_UP

# Replace float math:
pending = Decimal(str(fee_info['pending_amount']))
paid = Decimal(str(request.form.get('amount_paid')))

new_pending = (pending - paid).quantize(
    Decimal('0.01'), 
    rounding=ROUND_HALF_UP
)

# Validate
if paid <= 0:
    flash('Amount must be > 0', 'danger')
if paid > pending:
    flash('Amount exceeds pending', 'danger')

# Update with string conversion
cursor.execute("""
    UPDATE fees SET pending_amount = %s WHERE id = %s
""", (str(new_pending), fee_id))
```

---

### 12. Numeric Conversion Validation
**File:** `routes/admin_routes.py:347-358`  
**Time:** 10 minutes  

```python
try:
    student_id = int(request.form.get('student_id', 0))
    room_id = int(request.form.get('room_id', 0))
    
    # Validate IDs
    if not student_id or not room_id:
        flash('Please select both student and room', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    # Get room and validate capacity
    cursor.execute("SELECT capacity FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        flash('Room not found', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    capacity = int(room.get('capacity', 0))
    if capacity <= 0:
        flash('Invalid room configuration', 'danger')
        return redirect(url_for('admin.allocate_room'))
    
    # Proceed...
except (ValueError, TypeError) as e:
    flash(f'Invalid input: {e}', 'danger')
```

---

### 13. Rate Limiting on Login
**File:** `app.py:153`  
**Time:** 15 minutes  

```python
# Add to requirements.txt:
# Flask-Limiter==3.3.1

# In app.py:
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# On login route:
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    # existing code
```

---

## 📋 MEDIUM - FIX WHEN TIME ALLOWS

### 14. Add Database Indexes
**File:** `config/database.sql`  
**Time:** 10 minutes  

```sql
-- Add these indexes:
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_complaints_created ON complaints(created_at);
CREATE INDEX idx_fees_status ON fees(payment_status);
```

---

### 15. Replace Print with Logging
**File:** Throughout codebase  
**Time:** 30 minutes  

```python
# At top of files:
import logging
logger = logging.getLogger(__name__)

# Replace:
print(f"Error: {e}")
# With:
logger.error(f"Error: {e}")

# In app.py:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

### 16. Improve Exception Handling
**File:** All routes  
**Time:** 20 minutes  

```python
# BEFORE:
except Exception as e:
    try:
        db.connection.rollback()
    except:
        pass

# AFTER:
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    try:
        if db.connection:
            db.connection.rollback()
    except Exception as rollback_error:
        logger.error(f"Rollback failed: {rollback_error}")
    flash('Operation failed. Please try again.', 'danger')
```

---

## ✅ VERIFICATION CHECKLIST

After making fixes, verify:

- [ ] All routes load without 500 errors
- [ ] Login works correctly
- [ ] Room allocation doesn't create duplicates
- [ ] Payments calculate correctly to cent
- [ ] CSRF tokens present on forms
- [ ] Input validation blocking bad data
- [ ] No undefined variable errors in logs
- [ ] Database connections working
- [ ] Access control enforced (students can't access admin)
- [ ] Forms display without errors

---

## 🔧 Testing Commands

```bash
# Test database connection
python -c "from config.database import db; print('✓ DB Connected' if db.connection else '✗ DB Failed')"

# Test imports
python -c "import app; print('✓ App imports OK')"

# Run basic tests
python -m pytest tests/ -v

# Check for syntax errors
python -m py_compile routes/*.py

# Run Flask tests
FLASK_APP=app.py python -m flask shell
```

---

## 📞 Need Help?

Each fix has a reference number (1-16). Check `CODE_ANALYSIS_REPORT.md` for detailed information.

For more context, see `FIXES_REQUIRED.md` with full code examples.

---

**Estimated Total Fix Time:** 3-4 hours  
**Priority:** CRITICAL + HIGH fixes = 2-3 hours minimum
