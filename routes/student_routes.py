from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime

# Try MySQL first, fall back to mock database (same as app.py)
try:
    from config.database import db
    # Check if MySQL connection is actually available
    if db.connection is None or not db.is_connected:
        from config.database_mock import db
except:
    from config.database_mock import db

student_bp = Blueprint('student', __name__, url_prefix='/student')

# ==================== STUDENT DASHBOARD ====================
@student_bp.route('/dashboard')
@student_bp.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard"""
    try:
        cursor = db.connection.cursor()
        
        # Get student info - simplified for mock DB
        cursor.execute("SELECT * FROM students WHERE user_id = %s", (current_user.id,))
        student = cursor.fetchone()
        
        # Get room allocation - simplified
        cursor.execute("SELECT * FROM room_occupancy WHERE student_id = %s", (current_user.id,))
        occupancy = cursor.fetchone()
        
        room = None
        if occupancy:
            cursor.execute("SELECT * FROM rooms WHERE id = %s", (occupancy.get('room_id'),))
            room = cursor.fetchone()
        
        # Get complaints
        cursor.execute("SELECT * FROM complaints WHERE student_id = %s ORDER BY id DESC LIMIT 5", (current_user.id,))
        complaints = cursor.fetchall()
        
        # Get pending visitors
        cursor.execute("SELECT * FROM visitors WHERE student_id = %s", (current_user.id,))
        pending_visitors = cursor.fetchall()
        
        # Get fee status
        cursor.execute("SELECT * FROM fees WHERE student_id = %s ORDER BY id DESC LIMIT 1", (current_user.id,))
        fee = cursor.fetchone()
        
        # Get notices
        cursor.execute("SELECT * FROM notices ORDER BY id DESC LIMIT 5")
        notices = cursor.fetchall()
        
        cursor.close()
        
        return render_template('student/dashboard.html', 
                             student=student, 
                             room=room,
                             complaints=complaints or [],
                             pending_visitors=pending_visitors or [],
                             fee=fee,
                             notices=notices or [])
    except Exception as e:
        print(f"Dashboard error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        # Return dashboard with empty data
        return render_template('student/dashboard.html', 
                             student=None, 
                             room=None,
                             complaints=[],
                             pending_visitors=[],
                             fee=None,
                             notices=[])

# ==================== STUDENT PROFILE ====================
@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and update student profile"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            phone = request.form.get('phone', '').strip()
            gender = request.form.get('gender', '').strip()
            contact_person_name = request.form.get('contact_person_name', '').strip()
            contact_person_phone = request.form.get('contact_person_phone', '').strip()
            emergency_contact = request.form.get('emergency_contact_phone', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            pincode = request.form.get('pincode', '').strip()
            
            cursor.execute("""
                UPDATE students SET 
                contact_person_name = %s, contact_person_phone = %s,
                emergency_contact_phone = %s, address = %s,
                city = %s, state = %s, pincode = %s
                WHERE user_id = %s
            """, (contact_person_name, contact_person_phone, emergency_contact, 
                  address, city, state, pincode, current_user.id))
            
            cursor.execute("""
                UPDATE users SET phone = %s, gender = %s WHERE id = %s
            """, (phone, gender, current_user.id))
            
            db.connection.commit()
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            db.connection.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
        
        cursor.close()
        return redirect(url_for('student.profile'))
    
    # Get current profile
    cursor.execute("""
        SELECT s.*, u.phone, u.email 
        FROM students s 
        JOIN users u ON s.user_id = u.id 
        WHERE u.id = %s
    """, (current_user.id,))
    student = cursor.fetchone()
    cursor.close()
    
    return render_template('student/profile.html', student=student)

# ==================== COMPLAINTS ====================
@student_bp.route('/complaints', methods=['GET', 'POST'])
@login_required
def complaints():
    """View and submit complaints"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            category = request.form.get('category', '').strip()
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            priority = request.form.get('priority', 'Medium').strip()
            
            if not all([category, title, description]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('student.complaints'))
            
            # Get student's room
            cursor.execute("""
                SELECT ro.room_id FROM room_occupancy ro
                WHERE ro.student_id = %s AND ro.status = 'Active'
                LIMIT 1
            """, (current_user.id,))
            room_data = cursor.fetchone()
            room_id = room_data['room_id'] if room_data else None
            
            cursor.execute("""
                INSERT INTO complaints (student_id, room_id, category, title, description, priority, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
            """, (current_user.id, room_id, category, title, description, priority))
            db.connection.commit()
            
            flash('Complaint submitted successfully!', 'success')
            return redirect(url_for('student.complaints'))
            
        except Exception as e:
            db.connection.rollback()
            flash(f'Error submitting complaint: {str(e)}', 'danger')
    
    # Get all complaints for this student
    cursor.execute("""
        SELECT * FROM complaints 
        WHERE student_id = %s 
        ORDER BY created_at DESC
    """, (current_user.id,))
    complaints_raw = cursor.fetchall()
    
    # Convert complaints to proper format
    complaints_list = []
    for complaint in complaints_raw:
        complaint_dict = dict(complaint) if isinstance(complaint, tuple) else complaint
        
        # Convert created_at to string format if it's a datetime object
        if 'created_at' in complaint_dict:
            created_at = complaint_dict['created_at']
            if hasattr(created_at, 'strftime'):
                complaint_dict['created_at_str'] = created_at.strftime('%d %b %Y')
            else:
                complaint_dict['created_at_str'] = str(created_at)
        
        complaints_list.append(complaint_dict)
    
    cursor.close()
    
    return render_template('student/complaints.html', complaints=complaints_list)

# ==================== COMPLAINT DETAIL ====================
@student_bp.route('/complaint/<int:complaint_id>')
@login_required
def complaint_detail(complaint_id):
    """View complaint details"""
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT * FROM complaints 
        WHERE id = %s AND student_id = %s
    """, (complaint_id, current_user.id))
    complaint = cursor.fetchone()
    
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('student.complaints'))
    
    cursor.close()
    return render_template('student/complaint_detail.html', complaint=complaint)

# ==================== VISITOR REQUESTS ====================
@student_bp.route('/visitors', methods=['GET', 'POST'])
@login_required
def visitors():
    """View and request visitors"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            visitor_name = request.form.get('visitor_name', '').strip()
            visitor_phone = request.form.get('visitor_phone', '').strip()
            visitor_relation = request.form.get('visitor_relation', '').strip()
            visit_date = request.form.get('visit_date', '').strip()
            visit_time = request.form.get('visit_time', '').strip()
            expected_departure = request.form.get('expected_departure', '').strip()
            purpose = request.form.get('purpose', '').strip()
            
            if not all([visitor_name, visit_date, visit_time, purpose]):
                flash('All required fields must be filled.', 'danger')
                return redirect(url_for('student.visitors'))
            
            cursor.execute("""
                INSERT INTO visitors (student_id, visitor_name, visitor_phone, visitor_relation, 
                                    visit_date, visit_time, expected_departure, purpose, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
            """, (current_user.id, visitor_name, visitor_phone, visitor_relation, 
                  visit_date, visit_time, expected_departure, purpose))
            db.connection.commit()
            
            flash('Visitor request submitted successfully!', 'success')
            return redirect(url_for('student.visitors'))
            
        except Exception as e:
            db.connection.rollback()
            flash(f'Error submitting visitor request: {str(e)}', 'danger')
    
    # Get all visitor requests
    cursor.execute("""
        SELECT * FROM visitors 
        WHERE student_id = %s 
        ORDER BY visit_date DESC
    """, (current_user.id,))
    visitor_requests = cursor.fetchall()
    cursor.close()
    
    return render_template('student/visitors.html', visitors=visitor_requests)

# ==================== FEES ====================
@student_bp.route('/fees')
@login_required
def fees():
    """View fee details and payment history"""
    cursor = db.connection.cursor()
    
    # Get current fees
    cursor.execute("""
        SELECT * FROM fees 
        WHERE student_id = %s 
        ORDER BY academic_year DESC, semester DESC
    """, (current_user.id,))
    fees_list = cursor.fetchall()
    
    # Get payment history
    cursor.execute("""
        SELECT ph.*, f.academic_year, f.semester 
        FROM payment_history ph
        JOIN fees f ON ph.fee_id = f.id
        WHERE ph.student_id = %s 
        ORDER BY ph.payment_date DESC
    """, (current_user.id,))
    payment_history = cursor.fetchall()
    
    cursor.close()
    
    return render_template('student/fees.html', fees=fees_list, payment_history=payment_history)

# ==================== ROOM DETAILS ====================
@student_bp.route('/room')
@login_required
def room():
    """View allocated room details"""
    cursor = db.connection.cursor()
    
    try:
        cursor.execute("""
            SELECT r.id, r.room_number, r.floor, r.room_type, r.capacity, r.rent, r.amenities, r.is_available,
                   ro.check_in_date, ro.check_out_date, ro.status
            FROM room_occupancy ro
            JOIN rooms r ON ro.room_id = r.id
            WHERE ro.student_id = %s AND ro.status = 'Active'
        """, (current_user.id,))
        room_info = cursor.fetchone()
        
        if not room_info:
            flash('No room allocated yet.', 'info')
            cursor.close()
            return redirect(url_for('student.dashboard'))
        
        # Get roommates
        cursor.execute("""
            SELECT DISTINCT u.id, u.full_name, u.phone, s.roll_number
            FROM room_occupancy ro
            JOIN users u ON ro.student_id = u.id
            JOIN students s ON u.id = s.user_id
            WHERE ro.room_id = %s AND ro.status = 'Active' AND u.id != %s
        """, (room_info['id'], current_user.id))
        roommates = cursor.fetchall()
        
        cursor.close()
        
        return render_template('student/room.html', room=room_info, roommates=roommates)
    
    except Exception as e:
        cursor.close()
        print(f"Room details error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        flash(f'Error loading room details: {str(e)}', 'danger')
        return redirect(url_for('student.dashboard'))

# ==================== NOTICES ====================
@student_bp.route('/notices')
@login_required
def notices():
    """View hostel notices"""
    cursor = db.connection.cursor()
    
    cursor.execute("""
        SELECT * FROM notices 
        WHERE visibility IN ('All', 'Students')
        AND (expires_at IS NULL OR expires_at > NOW())
        ORDER BY is_pinned DESC, created_at DESC
    """)
    notices_list = cursor.fetchall()
    cursor.close()
    
    return render_template('student/notices.html', notices=notices_list)
