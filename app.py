from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from functools import wraps
import bcrypt
from datetime import datetime, timedelta
from config.config import DevelopmentConfig
import secrets

# Try MySQL first, fall back to mock database
try:
    from config.database import db
    # Check if MySQL connection is actually available
    if db.connection is None or not db.is_connected:
        print("[INFO] MySQL connection failed, using mock database")
        from config.database_mock import db
    else:
        print("[INFO] Using MySQL database")
except Exception as e:
    print(f"[INFO] MySQL unavailable ({str(e)}), using mock database")
    from config.database_mock import db

# Import OTP utilities
from utils.otp_manager import generate_otp, get_otp_expiry, send_otp_email, send_password_reset_confirmation

app = Flask(__name__)
app.config['SECRET_KEY'] = DevelopmentConfig.SECRET_KEY
app.config.from_object(DevelopmentConfig)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# ==================== CUSTOM JINJA FILTERS ====================
@app.template_filter('format_date')
def format_date(value, format_str='%d %b %Y'):
    """Format date safely - handles both datetime objects and strings"""
    if not value:
        return 'N/A'
    
    try:
        # If it's already a datetime object, format it
        if hasattr(value, 'strftime'):
            return value.strftime(format_str)
        # If it's a string, try to parse it first
        elif isinstance(value, str):
            # Try to parse common date formats
            from datetime import datetime
            
            # Remove any whitespace
            date_str = value.strip()
            
            # Try different date formats
            formats_to_try = [
                '%Y-%m-%d %H:%M:%S',  # 2026-07-21 12:09:15
                '%Y-%m-%d %H:%M',     # 2026-07-21 12:09
                '%Y-%m-%d',           # 2026-07-21
                '%d %b %Y',           # 21 Jul 2026 (already formatted)
                '%d-%m-%Y',           # 21-07-2026
                '%m/%d/%Y',           # 07/21/2026
                '%Y/%m/%d',           # 2026/07/21
            ]
            
            for fmt in formats_to_try:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime(format_str)
                except ValueError:
                    continue
            
            # If no format matched, return as-is
            return date_str
        else:
            return str(value)
    except Exception as e:
        return str(value) if value else 'N/A'

# ==================== USER CLASS ====================
class User(UserMixin):
    def __init__(self, id, username, email, role, full_name):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.full_name = full_name

@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    try:
        # Flask-Login passes user_id as string, convert to int
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        if db.connection is None or not db.is_connected:
            db.connect()
        
        if db.connection is None:
            return None
            
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, username, email, role, full_name FROM users WHERE id = %s AND is_active = TRUE", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            user = User(user_data['id'], user_data['username'], user_data['email'], user_data['role'], user_data['full_name'])
            return user
        return None
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        import traceback
        traceback.print_exc()
        return None

# ==================== DECORATORS ====================
def role_required(*roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== AUTH ROUTES ====================
@app.route('/')
def index():
    """Home/Landing page"""
    try:
        # Ensure database connection
        if db.connection is None or not db.is_connected:
            db.connect()
        
        if db.connection is None:
            # Return with default values if database not available
            return render_template('index.html', 
                                 settings={},
                                 total_rooms=0,
                                 available_rooms=0,
                                 total_students=0,
                                 pending_complaints=0,
                                 gallery_images=[],
                                 recent_notices=[])
        
        cursor = db.connection.cursor()
        
        # Get hostel settings
        cursor.execute("SELECT setting_key, setting_value FROM hostel_settings WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_name', 'warden_phone')")
        settings_data = cursor.fetchall()
        settings = {s['setting_key']: s['setting_value'] for s in settings_data}
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM rooms")
        total_rooms = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM rooms WHERE is_available = TRUE")
        available_rooms = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM users WHERE role = 'student'")
        total_students = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM complaints WHERE status != 'Resolved'")
        pending_complaints = cursor.fetchone()['total']
        
        # Get featured gallery images
        cursor.execute("SELECT id, title, image_path, category FROM gallery WHERE is_featured = TRUE LIMIT 6")
        gallery_images = cursor.fetchall()
        
        # Get recent notices
        cursor.execute("SELECT id, title, content, category, created_at FROM notices ORDER BY created_at DESC LIMIT 3")
        recent_notices = cursor.fetchall()
        
        cursor.close()
        
        return render_template('index.html', 
                             settings=settings,
                             total_rooms=total_rooms,
                             available_rooms=available_rooms,
                             total_students=total_students,
                             pending_complaints=pending_complaints,
                             gallery_images=gallery_images,
                             recent_notices=recent_notices)
    except Exception as e:
        print(f"Error loading home page: {e}")
        return render_template('index.html', 
                             settings={},
                             total_rooms=0,
                             available_rooms=0,
                             total_students=0,
                             pending_complaints=0,
                             gallery_images=[],
                             recent_notices=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration"""
    if request.method == 'POST':
        try:
            # Ensure database connection is active
            try:
                if hasattr(db, 'connection') and db.connection is not None:
                    if hasattr(db.connection, 'ping'):
                        db.connection.ping(True)
                    elif not db.is_connected:
                        db.connect()
            except:
                # If MySQL fails, it's already using mock database
                pass
            
            if db.connection is None:
                flash('Database connection error. Please try again.', 'danger')
                return redirect(url_for('register'))
            
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()
            gender = request.form.get('gender', '').strip()
            roll_number = request.form.get('roll_number', '').strip().upper()
            branch = request.form.get('branch', '').strip()
            semester = request.form.get('semester', 1)
            contact_person_name = request.form.get('contact_person_name', '').strip()
            contact_person_phone = request.form.get('contact_person_phone', '').strip()
            emergency_contact = request.form.get('emergency_contact_phone', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            pincode = request.form.get('pincode', '').strip()
            
            # Validation
            if not all([username, email, password, full_name, gender, roll_number, branch]):
                flash('All required fields must be filled.', 'danger')
                return redirect(url_for('register'))
            
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('register'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return redirect(url_for('register'))
            
            try:
                cursor = db.connection.cursor()
                
                # Check if username/email exists
                cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                if cursor.fetchone():
                    flash('Username or email already exists.', 'danger')
                    cursor.close()
                    return redirect(url_for('register'))
                
                # Hash password
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Create user account
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role, full_name, phone, gender, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
                """, (username, email, password_hash, 'student', full_name, phone, gender))
                
                # Handle commit for both MySQL and mock database
                if hasattr(db.connection, 'commit'):
                    db.connection.commit()
                
                # Get the user_id - handle both MySQL and mock database
                if hasattr(cursor, 'lastrowid'):
                    user_id = cursor.lastrowid
                else:
                    # For mock database, query back to get the ID
                    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                    user_result = cursor.fetchone()
                    user_id = user_result['id'] if user_result else None
                
                if not user_id:
                    raise Exception("Failed to get user ID after registration")
                
                # Create student profile
                cursor.execute("""
                    INSERT INTO students (user_id, roll_number, branch, semester, contact_person_name, 
                                        contact_person_phone, emergency_contact_phone, address, city, state, pincode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, roll_number, branch, semester, contact_person_name, contact_person_phone, 
                      emergency_contact, address, city, state, pincode))
                
                # Handle commit for both MySQL and mock database
                if hasattr(db.connection, 'commit'):
                    db.connection.commit()
                
                cursor.close()
                
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            
            except Exception as e:
                try:
                    if hasattr(db.connection, 'rollback'):
                        db.connection.rollback()
                except:
                    pass
                print(f"[REGISTER] Error: {e}")
                import traceback
                traceback.print_exc()
                flash(f'Registration failed: {str(e)}', 'danger')
                return redirect(url_for('register'))
        
        except Exception as e:
            print(f"[REGISTER] Outer error: {e}")
            flash(f'Registration error: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        import sys
        try:
            print(f"[LOGIN] Starting login attempt", file=sys.stderr, flush=True)
            
            # Ensure database connection is active
            try:
                if hasattr(db, 'connection') and db.connection is not None:
                    if hasattr(db.connection, 'ping'):
                        db.connection.ping(True)
                    elif not db.is_connected:
                        db.connect()
            except:
                # If MySQL fails, it's already using mock database
                pass
            
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            print(f"[LOGIN] Username: {username}, Password length: {len(password)}", file=sys.stderr, flush=True)
            
            if not username or not password:
                flash('Username and password are required.', 'danger')
                return redirect(url_for('login'))
            
            try:
                cursor = db.connection.cursor()
                cursor.execute("SELECT id, username, email, role, full_name, password_hash FROM users WHERE username = %s AND is_active = TRUE", (username,))
                user_data = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print(f"[LOGIN] Database query error: {e}", file=sys.stderr, flush=True)
                flash('Database error. Please try again.', 'danger')
                return redirect(url_for('login'))
            
            print(f"[LOGIN] User found: {user_data is not None}", file=sys.stderr, flush=True)
            
            if user_data:
                stored_hash = user_data['password_hash']
                print(f"[LOGIN] Stored hash: {stored_hash[:20]}...", file=sys.stderr, flush=True)
                
                # Convert $2y$ (PHP format) to $2b$ (Python format) if needed
                if stored_hash.startswith('$2y$'):
                    stored_hash = '$2b$' + stored_hash[4:]
                    print(f"[LOGIN] Converted hash from $2y$ to $2b$", file=sys.stderr, flush=True)
                
                # Check password
                password_valid = False
                try:
                    # Ensure both password and hash are properly encoded
                    password_bytes = password.encode('utf-8')
                    hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash
                    
                    print(f"[LOGIN] Password bytes type: {type(password_bytes)}, Hash bytes type: {type(hash_bytes)}", file=sys.stderr, flush=True)
                    
                    password_valid = bcrypt.checkpw(password_bytes, hash_bytes)
                    print(f"[LOGIN] Password check result: {password_valid}", file=sys.stderr, flush=True)
                except ValueError as hash_error:
                    print(f"[LOGIN] Hash verification error: {hash_error}", file=sys.stderr, flush=True)
                    password_valid = False
                except Exception as e:
                    print(f"[LOGIN] Unexpected error during password check: {e}", file=sys.stderr, flush=True)
                    password_valid = False
                
                if password_valid:
                    user = User(user_data['id'], user_data['username'], user_data['email'], user_data['role'], user_data['full_name'])
                    print(f"[LOGIN] Password matched, logging in: {user.username}", file=sys.stderr, flush=True)
                    login_user(user, remember=True)
                    print(f"[LOGIN] Authenticated: {current_user.is_authenticated}", file=sys.stderr, flush=True)
                    flash(f'Welcome, {user.full_name}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    print(f"[LOGIN] Invalid password for user {username}", file=sys.stderr, flush=True)
                    flash('Invalid username or password.', 'danger')
            else:
                print(f"[LOGIN] User {username} not found in database", file=sys.stderr, flush=True)
                flash('Invalid username or password.', 'danger')
        except Exception as e:
            print(f"[LOGIN] Exception: {str(e)}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# ==================== PASSWORD RESET ROUTES ====================
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - User enters username/email and selects OTP method"""
    if request.method == 'POST':
        try:
            if db.connection is None or not db.is_connected:
                db.connect()
            
            if db.connection is None:
                flash('Database connection error. Please try again.', 'danger')
                return redirect(url_for('forgot_password'))
            
            username_email = request.form.get('username_email', '').strip()
            otp_method = request.form.get('otp_method', 'email')
            
            if not username_email:
                flash('Please enter username or email.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Find user by username or email
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT id, username, email, full_name, phone FROM users 
                WHERE (username = %s OR email = %s) AND is_active = TRUE
            """, (username_email, username_email))
            user_data = cursor.fetchone()
            cursor.close()
            
            if not user_data:
                flash('No account found with this username or email.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Validate that user has email or phone based on selected method
            if otp_method == 'sms' and not user_data['phone']:
                flash('No phone number on file. Please use email method instead.', 'warning')
                return redirect(url_for('forgot_password'))
            
            if otp_method == 'email' and not user_data['email']:
                flash('No email on file. Please use SMS method instead.', 'warning')
                return redirect(url_for('forgot_password'))
            
            # Generate OTP
            otp_code = generate_otp()
            otp_expiry = get_otp_expiry()
            
            # Save OTP to database
            cursor = db.connection.cursor()
            contact_info = user_data['phone'] if otp_method == 'sms' else user_data['email']
            
            cursor.execute("""
                INSERT INTO password_reset_otp (user_id, email, phone, otp_code, otp_method, expires_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_data['id'], user_data['email'], user_data['phone'], otp_code, otp_method, otp_expiry))
            db.connection.commit()
            cursor.close()
            
            # Send OTP via email or SMS
            send_success = False
            if otp_method == 'email':
                send_success = send_otp_email(user_data['email'], user_data['full_name'], otp_code)
                if send_success:
                    flash('OTP has been sent to your email. Check your inbox!', 'success')
                else:
                    flash('Failed to send email. Please try again or contact support.', 'danger')
            else:  # SMS
                # Implement SMS sending here if Twilio is configured
                from utils.otp_manager import send_otp_sms
                send_success = send_otp_sms(user_data['phone'], otp_code)
                if send_success:
                    flash('OTP has been sent to your phone!', 'success')
                else:
                    flash('SMS service not available. Please use email method.', 'warning')
                    return redirect(url_for('forgot_password'))
            
            # Store in session for verification step
            session['otp_user_id'] = user_data['id']
            session['otp_method'] = otp_method
            session['otp_email'] = user_data['email']
            session['otp_phone'] = user_data['phone']
            
            return redirect(url_for('verify_otp'))
            
        except Exception as e:
            print(f"Error in forgot_password: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """Verify OTP entered by user"""
    if request.method == 'POST':
        try:
            if db.connection is None or not db.is_connected:
                db.connect()
            
            if db.connection is None:
                flash('Database connection error. Please try again.', 'danger')
                return redirect(url_for('forgot_password'))
            
            otp_code = request.form.get('otp_code', '').strip()
            user_id = session.get('otp_user_id')
            otp_method = session.get('otp_method')
            
            if not all([otp_code, user_id, otp_method]):
                flash('Invalid request. Please start over.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Verify OTP
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT id, otp_code, expires_at, is_verified FROM password_reset_otp
                WHERE user_id = %s AND otp_method = %s AND is_used = FALSE
                ORDER BY created_at DESC LIMIT 1
            """, (user_id, otp_method))
            otp_record = cursor.fetchone()
            
            if not otp_record:
                cursor.close()
                flash('No active OTP found. Please request a new one.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Check if OTP has expired
            if datetime.now() > otp_record['expires_at']:
                cursor.close()
                flash('OTP has expired. Please request a new one.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Check if OTP matches
            if otp_record['otp_code'] != otp_code:
                cursor.close()
                flash('Invalid OTP. Please try again.', 'danger')
                return redirect(url_for('verify_otp'))
            
            # Mark OTP as verified
            cursor.execute("""
                UPDATE password_reset_otp SET is_verified = TRUE, verified_at = NOW()
                WHERE id = %s
            """, (otp_record['id'],))
            db.connection.commit()
            
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            cursor.execute("""
                INSERT INTO password_reset_tokens (user_id, token, otp_id, expires_at)
                VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 30 MINUTE))
            """, (user_id, reset_token, otp_record['id']))
            db.connection.commit()
            cursor.close()
            
            # Store reset token in session
            session['reset_token'] = reset_token
            
            flash('OTP verified successfully! Please set your new password.', 'success')
            return redirect(url_for('reset_password'))
            
        except Exception as e:
            print(f"Error in verify_otp: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('forgot_password'))
    
    # GET request - show OTP form
    user_id = session.get('otp_user_id')
    otp_method = session.get('otp_method')
    email = session.get('otp_email')
    phone = session.get('otp_phone')
    
    if not user_id:
        flash('Please start the forgot password process.', 'danger')
        return redirect(url_for('forgot_password'))
    
    # Mask email and phone for display
    masked_email = email[:2] + '*' * (len(email) - 4) + email[-2:] if email else ''
    masked_phone = '*' * (len(phone) - 4) + phone[-4:] if phone else ''
    
    # Calculate expiry time (10 minutes from now)
    expiry_time = (datetime.now() + timedelta(minutes=DevelopmentConfig.OTP_EXPIRY_MINUTES)).strftime('%H:%M')
    
    return render_template('verify_otp.html', 
                         user_id=user_id, 
                         otp_method=otp_method,
                         masked_email=masked_email,
                         masked_phone=masked_phone,
                         expiry_time=expiry_time)

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Resend OTP to user"""
    try:
        if db.connection is None or not db.is_connected:
            db.connect()
        
        user_id = session.get('otp_user_id')
        otp_method = session.get('otp_method')
        
        if not user_id:
            flash('Please start the forgot password process.', 'danger')
            return redirect(url_for('forgot_password'))
        
        # Get user info
        cursor = db.connection.cursor()
        cursor.execute("SELECT email, phone, full_name FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            cursor.close()
            flash('User not found.', 'danger')
            return redirect(url_for('forgot_password'))
        
        # Generate new OTP
        otp_code = generate_otp()
        otp_expiry = get_otp_expiry()
        
        # Save new OTP
        cursor.execute("""
            INSERT INTO password_reset_otp (user_id, email, phone, otp_code, otp_method, expires_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, user_data['email'], user_data['phone'], otp_code, otp_method, otp_expiry))
        db.connection.commit()
        cursor.close()
        
        # Send OTP
        send_success = False
        if otp_method == 'email':
            send_success = send_otp_email(user_data['email'], user_data['full_name'], otp_code)
            if send_success:
                flash('New OTP has been sent to your email!', 'success')
        else:
            from utils.otp_manager import send_otp_sms
            send_success = send_otp_sms(user_data['phone'], otp_code)
            if send_success:
                flash('New OTP has been sent to your phone!', 'success')
        
        if not send_success:
            flash('Failed to send OTP. Please try again.', 'danger')
        
        return redirect(url_for('verify_otp'))
        
    except Exception as e:
        print(f"Error in resend_otp: {e}")
        flash('Error resending OTP. Please try again.', 'danger')
        return redirect(url_for('verify_otp'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """Reset user password"""
    if request.method == 'POST':
        try:
            if db.connection is None or not db.is_connected:
                db.connect()
            
            if db.connection is None:
                flash('Database connection error. Please try again.', 'danger')
                return redirect(url_for('forgot_password'))
            
            reset_token = session.get('reset_token')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not reset_token:
                flash('Invalid reset request. Please start over.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Validation
            if len(new_password) < 8:
                flash('Password must be at least 8 characters long.', 'danger')
                return redirect(url_for('reset_password'))
            
            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('reset_password'))
            
            # Verify reset token
            cursor = db.connection.cursor()
            cursor.execute("""
                SELECT user_id, is_used, expires_at FROM password_reset_tokens
                WHERE token = %s AND is_used = FALSE
            """, (reset_token,))
            token_record = cursor.fetchone()
            
            if not token_record:
                cursor.close()
                flash('Invalid or expired reset token.', 'danger')
                return redirect(url_for('forgot_password'))
            
            if datetime.now() > token_record['expires_at']:
                cursor.close()
                flash('Reset token has expired. Please start over.', 'danger')
                return redirect(url_for('forgot_password'))
            
            user_id = token_record['user_id']
            
            # Hash new password
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Update password
            cursor.execute("""
                UPDATE users SET password_hash = %s, updated_at = NOW()
                WHERE id = %s
            """, (password_hash, user_id))
            db.connection.commit()
            
            # Mark token as used
            cursor.execute("""
                UPDATE password_reset_tokens SET is_used = TRUE, reset_at = NOW()
                WHERE token = %s
            """, (reset_token,))
            db.connection.commit()
            
            # Mark OTP as used
            cursor.execute("""
                UPDATE password_reset_otp SET is_used = TRUE
                WHERE id = (SELECT otp_id FROM password_reset_tokens WHERE token = %s)
            """, (reset_token,))
            db.connection.commit()
            
            # Get user info for confirmation email
            cursor.execute("SELECT email, full_name FROM users WHERE id = %s", (user_id,))
            user_info = cursor.fetchone()
            cursor.close()
            
            # Send confirmation email
            send_password_reset_confirmation(user_info['email'], user_info['full_name'])
            
            # Clear session
            session.pop('otp_user_id', None)
            session.pop('otp_method', None)
            session.pop('reset_token', None)
            session.pop('otp_email', None)
            session.pop('otp_phone', None)
            
            flash('Password has been reset successfully! Please log in with your new password.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            print(f"Error in reset_password: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('forgot_password'))
    
    # GET request - show reset password form
    reset_token = session.get('reset_token')
    user_id = session.get('otp_user_id')
    
    if not reset_token or not user_id:
        flash('Invalid request. Please start over.', 'danger')
        return redirect(url_for('forgot_password'))
    
    return render_template('reset_password.html', token=reset_token, user_id=user_id)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard based on role"""
    if current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role == 'warden':
        return redirect(url_for('warden.dashboard'))
    return redirect(url_for('index'))

# ==================== STATIC PAGES ====================
@app.route('/gallery')
def gallery():
    """Gallery page"""
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT * FROM gallery 
        ORDER BY display_order ASC, created_at DESC
    """)
    images = cursor.fetchall()
    cursor.close()
    return render_template('gallery.html', images=images)

@app.route('/contact')
def contact():
    """Contact page"""
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT setting_key, setting_value FROM hostel_settings 
        WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 
                             'warden_name', 'warden_phone', 'checkin_time', 'checkout_time',
                             'visitor_hours_start', 'visitor_hours_end')
    """)
    settings_data = cursor.fetchall()
    settings = {s['setting_key']: s['setting_value'] for s in settings_data}
    cursor.close()
    return render_template('contact.html', settings=settings)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

# ==================== REGISTER BLUEPRINTS ====================
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.warden_routes import warden_bp

app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(warden_bp)

# ==================== CACHE CONTROL ====================
@app.after_request
def add_cache_headers(response):
    """Add cache-control headers to prevent browser caching"""
    # Prevent caching of all pages
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['ETag'] = None  # Remove ETag to force revalidation
    return response

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Hostel Management System Starting...")
    print("="*60)
    print(f"[OK] System IP: localhost")
    print(f"[OK] Port: 5000")
    print(f"[OK] URL: http://localhost:5000")
    print("="*60)
    print("\n[NOTE] If MySQL is not running, the app will use mock data.")
    print("   To start MySQL on Windows, open Services and start MySQL.")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', debug=True, port=5000)
