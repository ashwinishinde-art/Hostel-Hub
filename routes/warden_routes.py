from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

# Try MySQL first, fall back to mock database
try:
    from config.database import db
except:
    from config.database_mock import db

warden_bp = Blueprint('warden', __name__, url_prefix='/warden')

def warden_required(f):
    """Decorator to require warden role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'warden':
            flash('Warden access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== WARDEN DASHBOARD ====================
@warden_bp.route('/dashboard')
@login_required
@warden_required
def dashboard():
    """Warden dashboard"""
    cursor = db.connection.cursor()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) as count FROM complaints")
    total_complaints_result = cursor.fetchone()
    total_complaints = total_complaints_result.get('count', 0) if total_complaints_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'Pending'")
    pending_complaints_result = cursor.fetchone()
    pending_complaints = pending_complaints_result.get('count', 0) if pending_complaints_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'In Progress'")
    in_progress_result = cursor.fetchone()
    in_progress = in_progress_result.get('count', 0) if in_progress_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM visitors WHERE status = 'Pending'")
    pending_visitors_result = cursor.fetchone()
    pending_visitors = pending_visitors_result.get('count', 0) if pending_visitors_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'student'")
    total_students_result = cursor.fetchone()
    total_students = total_students_result.get('count', 0) if total_students_result else 0
    
    # Get recent complaints (simplified for mock DB - no JOINs)
    cursor.execute("""
        SELECT * FROM complaints ORDER BY id DESC LIMIT 5
    """)
    recent_complaints = cursor.fetchall() or []
    
    # Get recent visitors (simplified for mock DB - no JOINs)
    cursor.execute("""
        SELECT * FROM visitors ORDER BY id DESC LIMIT 5
    """)
    recent_visitors = cursor.fetchall() or []
    
    cursor.close()
    
    return render_template('warden/dashboard.html',
                         total_complaints=total_complaints,
                         pending_complaints=pending_complaints,
                         in_progress=in_progress,
                         pending_visitors=pending_visitors,
                         total_students=total_students,
                         recent_complaints=recent_complaints,
                         recent_visitors=recent_visitors)

# ==================== WARDEN COMPLAINTS ====================
@warden_bp.route('/complaints')
@login_required
@warden_required
def complaints():
    """View and manage complaints"""
    cursor = db.connection.cursor()
    
    status_filter = request.args.get('status', 'all')
    
    if status_filter == 'all':
        cursor.execute("""
            SELECT c.*, u.full_name, r.room_number
            FROM complaints c
            JOIN users u ON c.student_id = u.id
            LEFT JOIN rooms r ON c.room_id = r.id
            ORDER BY c.priority DESC, c.created_at DESC
        """)
    else:
        cursor.execute("""
            SELECT c.*, u.full_name, r.room_number
            FROM complaints c
            JOIN users u ON c.student_id = u.id
            LEFT JOIN rooms r ON c.room_id = r.id
            WHERE c.status = %s
            ORDER BY c.priority DESC, c.created_at DESC
        """, (status_filter,))
    
    complaints_list = cursor.fetchall()
    cursor.close()
    
    return render_template('warden/complaints.html', complaints=complaints_list, status_filter=status_filter)

# ==================== WARDEN VISITORS ====================
@warden_bp.route('/visitors', methods=['GET', 'POST'])
@login_required
@warden_required
def visitors():
    """Approve/reject visitor requests"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        visitor_id = request.form.get('visitor_id', 0)
        
        if action == 'approve':
            try:
                cursor.execute("""
                    UPDATE visitors 
                    SET status = 'Approved', approved_by = %s, updated_at = NOW()
                    WHERE id = %s
                """, (current_user.id, visitor_id))
                db.connection.commit()
                flash('Visitor request approved!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error: {str(e)}', 'danger')
        
        elif action == 'reject':
            try:
                rejection_reason = request.form.get('rejection_reason', '').strip()
                cursor.execute("""
                    UPDATE visitors 
                    SET status = 'Rejected', rejection_reason = %s, approved_by = %s, updated_at = NOW()
                    WHERE id = %s
                """, (rejection_reason, current_user.id, visitor_id))
                db.connection.commit()
                flash('Visitor request rejected!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('warden.visitors'))
    
    cursor.execute("""
        SELECT v.*, u.full_name, u.phone
        FROM visitors v
        JOIN users u ON v.student_id = u.id
        ORDER BY v.status DESC, v.visit_date DESC
    """)
    visitors_list = cursor.fetchall()
    cursor.close()
    
    return render_template('warden/visitors.html', visitors=visitors_list)

# ==================== WARDEN NOTICES ====================
@warden_bp.route('/notices', methods=['GET', 'POST'])
@login_required
@warden_required
def notices():
    """View notices"""
    cursor = db.connection.cursor()
    
    cursor.execute("""
        SELECT n.*, u.full_name 
        FROM notices n
        JOIN users u ON n.created_by = u.id
        ORDER BY n.is_pinned DESC, n.created_at DESC
    """)
    notices_list = cursor.fetchall()
    cursor.close()
    
    return render_template('warden/notices.html', notices=notices_list)

# ==================== WARDEN ROOMS ====================
@warden_bp.route('/rooms')
@login_required
@warden_required
def rooms():
    """View room allocation and availability"""
    cursor = db.connection.cursor()
    
    cursor.execute("""
        SELECT r.*, COUNT(ro.id) as occupied_count
        FROM rooms r
        LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
        GROUP BY r.id
        ORDER BY r.floor, r.room_number
    """)
    rooms_list = cursor.fetchall()
    cursor.close()
    
    return render_template('warden/rooms.html', rooms=rooms_list)

# ==================== WARDEN STUDENTS ====================
@warden_bp.route('/students')
@login_required
@warden_required
def students():
    """View student list"""
    cursor = db.connection.cursor()
    
    cursor.execute("""
        SELECT u.*, s.roll_number, s.branch, s.semester,
               r.room_number
        FROM users u
        JOIN students s ON u.id = s.user_id
        LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
        LEFT JOIN rooms r ON ro.room_id = r.id
        WHERE u.role = 'student'
        ORDER BY u.full_name
    """)
    students_list = cursor.fetchall()
    cursor.close()
    
    return render_template('warden/students.html', students=students_list)
