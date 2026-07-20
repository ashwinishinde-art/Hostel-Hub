from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime

# Try MySQL first, fall back to mock database
try:
    from config.database import db
except:
    from config.database_mock import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ADMIN DASHBOARD ====================
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    cursor = db.connection.cursor()
    
    # Calculate statistics
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'student'")
    total_students = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM rooms")
    total_rooms_result = cursor.fetchone()
    total_rooms = total_rooms_result.get('count', 0) if total_rooms_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM rooms WHERE is_available = TRUE")
    available_result = cursor.fetchone()
    available_rooms = available_result.get('count', 0) if available_result else 0
    
    occupied_rooms = total_rooms - available_rooms
    
    cursor.execute("SELECT COUNT(*) as count FROM complaints WHERE status = 'Pending'")
    pending_complaints_result = cursor.fetchone()
    pending_complaints = pending_complaints_result.get('count', 0) if pending_complaints_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM visitors WHERE status = 'Pending'")
    pending_visitors_result = cursor.fetchone()
    pending_visitors = pending_visitors_result.get('count', 0) if pending_visitors_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM notices")
    notices_result = cursor.fetchone()
    total_notices = notices_result.get('count', 0) if notices_result else 0
    
    cursor.execute("SELECT COUNT(*) as count FROM fees WHERE payment_status IN ('Pending', 'Overdue')")
    pending_fees_result = cursor.fetchone()
    pending_fees = pending_fees_result.get('count', 0) if pending_fees_result else 0
    
    cursor.execute("""
        SELECT SUM(pending_amount) as total_pending FROM fees
    """)
    fee_result = cursor.fetchone()
    total_pending_fees = 0
    if fee_result:
        total_pending_fees = fee_result.get('total_pending') or 0
    
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
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_rooms=total_rooms,
                         available_rooms=available_rooms,
                         occupied_rooms=occupied_rooms,
                         pending_complaints=pending_complaints,
                         pending_visitors=pending_visitors,
                         total_notices=total_notices,
                         pending_fees=pending_fees,
                         total_pending_fees=total_pending_fees,
                         recent_complaints=recent_complaints,
                         recent_visitors=recent_visitors)

# ==================== ROOM MANAGEMENT ====================
@admin_bp.route('/rooms', methods=['GET', 'POST'])
@login_required
@admin_required
def rooms():
    """Room management"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        
        if action == 'add':
            try:
                room_number = request.form.get('room_number', '').strip()
                floor = int(request.form.get('floor', 0))
                room_type = request.form.get('room_type', '')
                capacity = int(request.form.get('capacity', 0))
                rent = float(request.form.get('rent', 0))
                amenities = request.form.get('amenities', '').strip()
                
                cursor.execute("""
                    INSERT INTO rooms (room_number, floor, room_type, capacity, rent, amenities, is_available)
                    VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                """, (room_number, floor, room_type, capacity, rent, amenities))
                db.connection.commit()
                flash('Room added successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error adding room: {str(e)}', 'danger')
        
        elif action == 'update':
            try:
                room_id = int(request.form.get('room_id', 0))
                floor = int(request.form.get('floor', 0))
                room_type = request.form.get('room_type', '')
                capacity = int(request.form.get('capacity', 0))
                rent = float(request.form.get('rent', 0))
                amenities = request.form.get('amenities', '').strip()
                
                cursor.execute("""
                    UPDATE rooms 
                    SET floor = %s, room_type = %s, capacity = %s, rent = %s, amenities = %s
                    WHERE id = %s
                """, (floor, room_type, capacity, rent, amenities, room_id))
                db.connection.commit()
                flash('Room updated successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error updating room: {str(e)}', 'danger')
        
        elif action == 'delete':
            try:
                room_id = int(request.form.get('room_id', 0))
                cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
                db.connection.commit()
                flash('Room deleted successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error deleting room: {str(e)}', 'danger')
        
        elif action == 'remove_student':
            try:
                occupancy_id = int(request.form.get('occupancy_id', 0))
                cursor.execute("""
                    SELECT student_id FROM room_occupancy WHERE id = %s
                """, (occupancy_id,))
                occupancy = cursor.fetchone()
                
                if occupancy:
                    cursor.execute("""
                        UPDATE room_occupancy SET status = 'Inactive' WHERE id = %s
                    """, (occupancy_id,))
                    db.connection.commit()
                    
                    cursor.execute("SELECT full_name FROM users WHERE id = %s", (occupancy['student_id'],))
                    student = cursor.fetchone()
                    flash(f"Student {student['full_name']} removed from room.", 'success')
                else:
                    flash('Occupancy record not found.', 'danger')
                    
            except Exception as e:
                db.connection.rollback()
                flash(f'Error removing student: {str(e)}', 'danger')
        
        return redirect(url_for('admin.rooms'))
    
    # Get all rooms
    cursor.execute("SELECT * FROM rooms ORDER BY id")
    rooms_list = cursor.fetchall() or []
    
    # Add occupied_count to each room and convert numeric fields
    for room in rooms_list:
        # Convert numeric fields to proper types
        room['floor'] = int(room.get('floor', 0)) if room.get('floor') else 0
        room['capacity'] = int(room.get('capacity', 0)) if room.get('capacity') else 0
        room['rent'] = float(room.get('rent', 0)) if room.get('rent') else 0.0
        
        # Count ACTIVE occupants for this room (using status field, not is_active)
        room_id = int(room.get('id')) if isinstance(room.get('id'), str) else room.get('id')
        cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = %s AND status = 'Active'", (room_id,))
        count_result = cursor.fetchone()
        room['occupied_count'] = count_result.get('count', 0) if count_result else 0
    
    cursor.close()
    
    return render_template('admin/rooms.html', rooms=rooms_list)

# ==================== ALLOCATE ROOMS ====================
@admin_bp.route('/allocate-room', methods=['GET', 'POST'])
@login_required
@admin_required
def allocate_room():
    """Allocate room to student - with gender restriction"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id', 0))
            room_id = int(request.form.get('room_id', 0))
            check_in_date = request.form.get('check_in_date', '').strip()
            
            if not check_in_date:
                check_in_date = datetime.now().strftime('%Y-%m-%d')
            
            # Get student gender
            cursor.execute("SELECT gender FROM users WHERE id = %s", (student_id,))
            student_result = cursor.fetchone()
            if not student_result:
                flash('Student not found.', 'danger')
                return redirect(url_for('admin.allocate_room'))
            
            student_gender = student_result.get('gender') if isinstance(student_result, dict) else student_result[0]
            
            if not student_gender:
                flash('Student gender information is missing. Please update student profile first.', 'warning')
                return redirect(url_for('admin.allocate_room'))
            
            # Get room information including gender occupancy
            cursor.execute("SELECT capacity, gender_occupancy FROM rooms WHERE id = %s", (room_id,))
            room_result = cursor.fetchone()
            
            if not room_result:
                flash('Room not found.', 'danger')
                return redirect(url_for('admin.allocate_room'))
            
            room_capacity = room_result.get('capacity') if isinstance(room_result, dict) else room_result[0]
            room_gender_occupancy = room_result.get('gender_occupancy') if isinstance(room_result, dict) else room_result[1]
            
            # Check room availability - count ACTIVE occupants only
            cursor.execute("""
                SELECT COUNT(*) as count FROM room_occupancy 
                WHERE room_id = %s AND status = 'Active'
            """, (room_id,))
            count_result = cursor.fetchone()
            current_count = count_result.get('count', 0) if count_result else 0
            
            # Check if room is at capacity
            if current_count >= room_capacity:
                flash(f'This room is at full capacity ({current_count}/{room_capacity} occupied). Cannot add more students.', 'danger')
                return redirect(url_for('admin.allocate_room'))
            
            # GENDER RESTRICTION: Check if room already has opposite gender students
            if current_count > 0:
                # Get gender of students already in the room
                cursor.execute("""
                    SELECT DISTINCT u.gender FROM users u
                    INNER JOIN room_occupancy ro ON u.id = ro.student_id
                    WHERE ro.room_id = %s AND ro.status = 'Active'
                """, (room_id,))
                existing_genders = cursor.fetchall()
                
                if existing_genders:
                    existing_gender_list = [g.get('gender') if isinstance(g, dict) else g[0] for g in existing_genders]
                    
                    # If room has students and new student is opposite gender, reject
                    if student_gender not in existing_gender_list:
                        existing_gender = existing_gender_list[0]
                        flash(f'Cannot allocate room! This room currently has {existing_gender} students. Rooms cannot be mixed with {student_gender} students.', 'danger')
                        return redirect(url_for('admin.allocate_room'))
            
            # Check if student already has active allocation
            cursor.execute("""
                SELECT id FROM room_occupancy 
                WHERE student_id = %s AND status = 'Active'
            """, (student_id,))
            
            if cursor.fetchone():
                flash('Student already has an active room allocation.', 'danger')
                return redirect(url_for('admin.allocate_room'))
            
            # Update room gender occupancy if this is the first student
            if current_count == 0:
                room_gender = 'Boys' if student_gender == 'Male' else 'Girls'
                cursor.execute("""
                    UPDATE rooms SET gender_occupancy = %s WHERE id = %s
                """, (room_gender, room_id))
                db.connection.commit()
            
            # Allocate room
            cursor.execute("""
                INSERT INTO room_occupancy (room_id, student_id, check_in_date, status)
                VALUES (%s, %s, %s, 'Active')
            """, (room_id, student_id, check_in_date))
            db.connection.commit()
            
            flash(f'Room allocated successfully! ({current_count + 1}/{room_capacity} occupied)', 'success')
            return redirect(url_for('admin.rooms'))
            
        except Exception as e:
            try:
                db.connection.rollback()
            except:
                pass
            flash(f'Error allocating room: {str(e)}', 'danger')
            import traceback
            traceback.print_exc()
            return redirect(url_for('admin.allocate_room'))
    
    # Get students without active rooms
    cursor.execute("SELECT id, full_name, roll_number, gender FROM users WHERE role = 'student' ORDER BY full_name")
    all_students = cursor.fetchall() or []
    
    # Filter students without active room allocations
    students = []
    for student in all_students:
        cursor.execute("SELECT id FROM room_occupancy WHERE student_id = %s AND status = 'Active'", (student.get('id') if isinstance(student, dict) else student[0],))
        if not cursor.fetchone():
            students.append(student)
    
    # Get available rooms with occupancy info
    cursor.execute("""
        SELECT r.id, r.room_number, r.room_type, r.capacity, r.gender_occupancy,
               COUNT(ro.id) as occupied_count
        FROM rooms r
        LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
        GROUP BY r.id
        ORDER BY r.room_number
    """)
    all_rooms = cursor.fetchall() or []
    
    available_rooms = []
    for room in all_rooms:
        room_id = int(room.get('id')) if isinstance(room.get('id'), str) else room.get('id')
        cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE room_id = %s AND status = 'Active'", (room_id,))
        count_result = cursor.fetchone()
        occupied = count_result.get('count', 0) if count_result else 0
        capacity = room.get('capacity', 0) if isinstance(room, dict) else room[3]
        gender_occupancy = room.get('gender_occupancy', 'Mixed') if isinstance(room, dict) else (room[4] if len(room) > 4 else 'Mixed')
        
        if occupied < capacity:
            room_dict = {
                'id': room_id,
                'room_number': room.get('room_number') if isinstance(room, dict) else room[1],
                'room_type': room.get('room_type') if isinstance(room, dict) else room[2],
                'capacity': capacity,
                'gender_occupancy': gender_occupancy,
                'occupied_count': occupied
            }
            available_rooms.append(room_dict)
    
    cursor.close()
    
    return render_template('admin/allocate_room.html', students=students, available_rooms=available_rooms)


# ==================== COMPLAINTS MANAGEMENT ====================
@admin_bp.route('/complaints', methods=['GET', 'POST'])
@login_required
@admin_required
def complaints():
    """Manage complaints"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        complaint_id = request.form.get('complaint_id', 0)
        
        if action == 'update_status':
            try:
                status = request.form.get('status', '')
                resolution_notes = request.form.get('resolution_notes', '').strip()
                
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
                flash('Complaint updated successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error updating complaint: {str(e)}', 'danger')
        
        return redirect(url_for('admin.complaints'))
    
    # Filter complaints
    status_filter = request.args.get('status', 'all')
    if status_filter == 'all':
        cursor.execute("""
            SELECT c.*, u.full_name, r.room_number
            FROM complaints c
            JOIN users u ON c.student_id = u.id
            LEFT JOIN rooms r ON c.room_id = r.id
            ORDER BY c.created_at DESC
        """)
    else:
        cursor.execute("""
            SELECT c.*, u.full_name, r.room_number
            FROM complaints c
            JOIN users u ON c.student_id = u.id
            LEFT JOIN rooms r ON c.room_id = r.id
            WHERE c.status = %s
            ORDER BY c.created_at DESC
        """, (status_filter,))
    
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
    
    return render_template('admin/complaints.html', complaints=complaints_list, status_filter=status_filter)

# ==================== VIEW COMPLAINT DETAILS ====================
@admin_bp.route('/complaint/<int:complaint_id>')
@login_required
@admin_required
def view_complaint(complaint_id):
    """View complaint details"""
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT c.*, u.full_name, u.phone, u.email, r.room_number
        FROM complaints c
        JOIN users u ON c.student_id = u.id
        LEFT JOIN rooms r ON c.room_id = r.id
        WHERE c.id = %s
    """, (complaint_id,))
    complaint = cursor.fetchone()
    cursor.close()
    
    if not complaint:
        return '<div class="alert alert-danger">Complaint not found</div>', 404
    
    # Convert to dict
    complaint_dict = dict(complaint) if isinstance(complaint, tuple) else complaint
    
    # Format dates
    if 'created_at' in complaint_dict:
        created_at = complaint_dict['created_at']
        if hasattr(created_at, 'strftime'):
            complaint_dict['created_at_str'] = created_at.strftime('%d %b %Y at %H:%M')
        else:
            complaint_dict['created_at_str'] = str(created_at)
    
    # Return modal content
    html = f"""
    <div class="complaint-details">
        <div class="detail-item">
            <label><i class="fas fa-user"></i> Student Name</label>
            <p>{complaint_dict.get('full_name', 'N/A')}</p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-door-open"></i> Room Number</label>
            <p>{complaint_dict.get('room_number', 'N/A')}</p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-phone"></i> Contact</label>
            <p>{complaint_dict.get('phone', 'N/A')} | {complaint_dict.get('email', 'N/A')}</p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-tag"></i> Category</label>
            <p>{complaint_dict.get('category', 'N/A')}</p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-exclamation"></i> Priority</label>
            <p>
                <span class="badge bg-{{'danger' if complaint_dict.get('priority') == 'High' else 'warning' if complaint_dict.get('priority') == 'Medium' else 'info'}}">
                    {complaint_dict.get('priority', 'N/A')}
                </span>
            </p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-check-circle"></i> Status</label>
            <p>
                <span class="badge bg-{{'success' if complaint_dict.get('status') == 'Resolved' else 'warning' if complaint_dict.get('status') == 'In Progress' else 'danger'}}">
                    {complaint_dict.get('status', 'N/A')}
                </span>
            </p>
        </div>
        <div class="detail-item">
            <label><i class="fas fa-calendar"></i> Submitted</label>
            <p>{complaint_dict.get('created_at_str', 'N/A')}</p>
        </div>
    </div>

    <div class="description-box">
        <label><i class="fas fa-heading"></i> Title</label>
        <p>{complaint_dict.get('title', 'N/A')}</p>
    </div>

    <div class="description-box">
        <label><i class="fas fa-file-alt"></i> Description</label>
        <p>{complaint_dict.get('description', 'N/A')}</p>
    </div>

    <form method="POST" action="/admin/complaints">
        <input type="hidden" name="action" value="update">
        <input type="hidden" name="complaint_id" value="{complaint_id}">
        
        <div class="row">
            <div class="col-md-6">
                <label class="form-label fw-bold">Update Status</label>
                <select name="status" class="form-select" style="border-radius: 8px; border: 2px solid #e0e0e0;">
                    <option value="Pending" {{'selected' if complaint_dict.get('status') == 'Pending' else ''}}>Pending</option>
                    <option value="In Progress" {{'selected' if complaint_dict.get('status') == 'In Progress' else ''}}>In Progress</option>
                    <option value="Resolved" {{'selected' if complaint_dict.get('status') == 'Resolved' else ''}}>Resolved</option>
                    <option value="Closed" {{'selected' if complaint_dict.get('status') == 'Closed' else ''}}>Closed</option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label fw-bold">Priority</label>
                <select name="priority" class="form-select" style="border-radius: 8px; border: 2px solid #e0e0e0;">
                    <option value="Low" {{'selected' if complaint_dict.get('priority') == 'Low' else ''}}>Low</option>
                    <option value="Medium" {{'selected' if complaint_dict.get('priority') == 'Medium' else ''}}>Medium</option>
                    <option value="High" {{'selected' if complaint_dict.get('priority') == 'High' else ''}}>High</option>
                </select>
            </div>
        </div>

        <div style="margin-top: 20px;">
            <label class="form-label fw-bold">Resolution Notes</label>
            <textarea name="resolution_notes" class="form-control" rows="4" style="border-radius: 8px; border: 2px solid #e0e0e0;" placeholder="Add notes about the resolution...">{complaint_dict.get('resolution_notes', '')}</textarea>
        </div>

        <div style="margin-top: 20px; display: flex; gap: 10px;">
            <button type="submit" class="btn btn-success" style="font-weight: 700; border-radius: 8px;">
                <i class="fas fa-save"></i> Save Changes
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" style="font-weight: 700; border-radius: 8px;">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
    </form>
    """
    
    return html

# ==================== VISITORS MANAGEMENT ====================
@admin_bp.route('/visitors', methods=['GET', 'POST'])
@login_required
@admin_required
def visitors():
    """Manage visitor requests"""
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
                flash(f'Error approving request: {str(e)}', 'danger')
        
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
                flash(f'Error rejecting request: {str(e)}', 'danger')
        
        return redirect(url_for('admin.visitors'))
    
    # Get all visitor requests
    cursor.execute("""
        SELECT v.*, u.full_name, u.phone
        FROM visitors v
        JOIN users u ON v.student_id = u.id
        ORDER BY v.status DESC, v.created_at DESC
    """)
    visitors_list = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/visitors.html', visitors=visitors_list)

# ==================== NOTICES MANAGEMENT ====================
@admin_bp.route('/notices', methods=['GET', 'POST'])
@login_required
@admin_required
def notices():
    """Manage notices"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        
        if action == 'add':
            try:
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                category = request.form.get('category', 'General')
                priority = request.form.get('priority', 'Medium')
                is_pinned = request.form.get('is_pinned') == 'on'
                visibility = request.form.get('visibility', 'All')
                
                cursor.execute("""
                    INSERT INTO notices (title, content, category, created_by, priority, is_pinned, visibility)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (title, content, category, current_user.id, priority, is_pinned, visibility))
                db.connection.commit()
                flash('Notice published successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error publishing notice: {str(e)}', 'danger')
        
        elif action == 'update':
            try:
                notice_id = request.form.get('notice_id', 0)
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                category = request.form.get('category', 'General')
                priority = request.form.get('priority', 'Medium')
                is_pinned = request.form.get('is_pinned') == 'on'
                
                cursor.execute("""
                    UPDATE notices 
                    SET title = %s, content = %s, category = %s, priority = %s, is_pinned = %s, updated_at = NOW()
                    WHERE id = %s
                """, (title, content, category, priority, is_pinned, notice_id))
                db.connection.commit()
                flash('Notice updated successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error updating notice: {str(e)}', 'danger')
        
        elif action == 'delete':
            try:
                notice_id = request.form.get('notice_id', 0)
                cursor.execute("DELETE FROM notices WHERE id = %s", (notice_id,))
                db.connection.commit()
                flash('Notice deleted successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error deleting notice: {str(e)}', 'danger')
        
        return redirect(url_for('admin.notices'))
    
    cursor.execute("""
        SELECT n.*, u.full_name 
        FROM notices n
        JOIN users u ON n.created_by = u.id
        ORDER BY n.is_pinned DESC, n.created_at DESC
    """)
    notices_list = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/notices.html', notices=notices_list)

# ==================== FEE MANAGEMENT ====================
@admin_bp.route('/fees', methods=['GET', 'POST'])
@login_required
@admin_required
def fees():
    """Manage fees"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        
        if action == 'record_payment':
            try:
                fee_id = request.form.get('fee_id', 0)
                amount_paid = request.form.get('amount_paid', 0)
                payment_method = request.form.get('payment_method', 'Cash')
                transaction_id = request.form.get('transaction_id', '').strip()
                notes = request.form.get('notes', '').strip()
                
                # Get fee info
                cursor.execute("""
                    SELECT student_id, pending_amount FROM fees WHERE id = %s
                """, (fee_id,))
                fee_info = cursor.fetchone()
                
                if not fee_info:
                    flash('Fee record not found.', 'danger')
                    return redirect(url_for('admin.fees'))
                
                # Record payment
                cursor.execute("""
                    INSERT INTO payment_history (fee_id, student_id, amount_paid, payment_method, 
                                               transaction_id, payment_date, recorded_by, notes)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s)
                """, (fee_id, fee_info['student_id'], amount_paid, payment_method, 
                     transaction_id, current_user.id, notes))
                
                # Update fee status
                new_pending = fee_info['pending_amount'] - float(amount_paid)
                if new_pending <= 0:
                    status = 'Paid'
                elif new_pending < fee_info['pending_amount']:
                    status = 'Partial'
                else:
                    status = 'Pending'
                
                cursor.execute("""
                    UPDATE fees 
                    SET paid_amount = paid_amount + %s,
                        pending_amount = %s,
                        payment_status = %s,
                        last_payment_date = NOW()
                    WHERE id = %s
                """, (amount_paid, max(0, new_pending), status, fee_id))
                
                db.connection.commit()
                flash('Payment recorded successfully!', 'success')
                
            except Exception as e:
                db.connection.rollback()
                flash(f'Error recording payment: {str(e)}', 'danger')
        
        return redirect(url_for('admin.fees'))
    
    cursor.execute("""
        SELECT f.*, u.full_name, s.roll_number
        FROM fees f
        JOIN users u ON f.student_id = u.id
        JOIN students s ON u.id = s.user_id
        ORDER BY f.academic_year DESC, f.semester DESC
    """)
    fees_list = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/fees.html', fees=fees_list)

# ==================== STUDENTS MANAGEMENT ====================
@admin_bp.route('/students')
@login_required
@admin_required
def students():
    """View all students"""
    cursor = db.connection.cursor()
    
    cursor.execute("""
        SELECT u.id, u.username, u.email, u.full_name, u.phone, u.role,
               s.roll_number, s.branch, s.semester,
               r.room_number,
               ro.status as room_status
        FROM users u
        JOIN students s ON u.id = s.user_id
        LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
        LEFT JOIN rooms r ON ro.room_id = r.id
        WHERE u.role = 'student'
        ORDER BY u.full_name
    """)
    students_list = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/students.html', students=students_list)


# ==================== ROOM STUDENT MANAGEMENT ====================
@admin_bp.route('/room-students/<int:room_id>')
@login_required
@admin_required
def room_students(room_id):
    """Get students in a room (AJAX endpoint)"""
    cursor = db.connection.cursor()
    
    # Get room details
    cursor.execute("SELECT room_number, capacity FROM rooms WHERE id = %s", (room_id,))
    room = cursor.fetchone()
    
    if not room:
        return '<p style="color: #e74c3c;">Room not found</p>', 404
    
    # Get students in this room
    cursor.execute("""
        SELECT ro.id as occupancy_id, u.id as student_id, u.full_name, s.roll_number,
               ro.check_in_date, ro.status
        FROM room_occupancy ro
        JOIN users u ON ro.student_id = u.id
        JOIN students s ON u.id = s.user_id
        WHERE ro.room_id = %s AND ro.status = 'Active'
        ORDER BY ro.check_in_date
    """, (room_id,))
    students = cursor.fetchall()
    
    cursor.close()
    
    # Build HTML response
    html = f'''
    <div style="padding: 15px;">
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h6 style="margin: 0 0 10px 0; font-weight: 700;">Room {room['room_number']}</h6>
            <p style="margin: 0; font-weight: 500;">
                <i class="fas fa-users"></i> {len(students)}/{room['capacity']} students
            </p>
        </div>
    '''
    
    if students:
        html += '''
        <div style="border-radius: 8px; overflow: hidden;">
            <table style="width: 100%; border-collapse: collapse;">
                <thead style="background: rgba(52, 152, 219, 0.1);">
                    <tr>
                        <th style="padding: 12px; text-align: left; font-weight: 700; border-bottom: 2px solid var(--border-current);">Student</th>
                        <th style="padding: 12px; text-align: left; font-weight: 700; border-bottom: 2px solid var(--border-current);">Roll No</th>
                        <th style="padding: 12px; text-align: left; font-weight: 700; border-bottom: 2px solid var(--border-current);">Check-in</th>
                        <th style="padding: 12px; text-align: center; font-weight: 700; border-bottom: 2px solid var(--border-current);">Actions</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for student in students:
            check_in_date = student['check_in_date'].strftime('%d %b %Y') if hasattr(student['check_in_date'], 'strftime') else student['check_in_date']
            html += f'''
                    <tr style="border-bottom: 1px solid var(--border-current);">
                        <td style="padding: 12px; color: var(--text-current); font-weight: 600;">{student['full_name']}</td>
                        <td style="padding: 12px; color: var(--text-current); font-weight: 500;">{student['roll_number']}</td>
                        <td style="padding: 12px; color: var(--text-current); font-weight: 500;">{check_in_date}</td>
                        <td style="padding: 12px; text-align: center;">
                            <button class="btn btn-sm btn-warning" onclick="shiftStudent({student['occupancy_id']}, {room_id})" title="Shift to another room" style="font-weight: 600; margin-right: 5px;">
                                <i class="fas fa-exchange-alt"></i> Shift
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="removeStudentFromRoom({student['occupancy_id']}, {room_id})" title="Remove from room" style="font-weight: 600;">
                                <i class="fas fa-trash"></i> Remove
                            </button>
                        </td>
                    </tr>
            '''
        
        html += '''
                </tbody>
            </table>
        </div>
        '''
    else:
        html += '''
        <div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 8px;">
            <i class="fas fa-inbox" style="font-size: 2rem; opacity: 0.3; margin-bottom: 10px; display: block;"></i>
            <p style="font-weight: 500; margin: 10px 0 0 0;">No students in this room</p>
        </div>
        '''
    
    html += '</div>'
    return html


@admin_bp.route('/remove-student/<int:occupancy_id>', methods=['POST'])
@login_required
@admin_required
def remove_student(occupancy_id):
    """Remove student from room"""
    cursor = db.connection.cursor()
    
    try:
        # Get occupancy details
        cursor.execute("""
            SELECT student_id, room_id FROM room_occupancy WHERE id = %s
        """, (occupancy_id,))
        occupancy = cursor.fetchone()
        
        if not occupancy:
            flash('Occupancy record not found.', 'danger')
            return redirect(url_for('admin.rooms'))
        
        # Mark as inactive instead of deleting
        cursor.execute("""
            UPDATE room_occupancy SET status = 'Inactive' WHERE id = %s
        """, (occupancy_id,))
        db.connection.commit()
        
        # Get student name for message
        cursor.execute("SELECT full_name FROM users WHERE id = %s", (occupancy['student_id'],))
        student = cursor.fetchone()
        
        flash(f"Student {student['full_name']} removed from room.", 'success')
        
    except Exception as e:
        db.connection.rollback()
        flash(f'Error removing student: {str(e)}', 'danger')
    
    cursor.close()
    return redirect(url_for('admin.rooms'))


@admin_bp.route('/shift-student/<int:occupancy_id>/<int:current_room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def shift_student(occupancy_id, current_room_id):
    """Shift student to another room"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            new_room_id = int(request.form.get('new_room_id', 0))
            
            # Get current occupancy
            cursor.execute("""
                SELECT student_id FROM room_occupancy WHERE id = %s
            """, (occupancy_id,))
            occupancy = cursor.fetchone()
            
            if not occupancy:
                flash('Occupancy record not found.', 'danger')
                return redirect(url_for('admin.rooms'))
            
            # Check new room capacity
            cursor.execute("""
                SELECT capacity FROM rooms WHERE id = %s
            """, (new_room_id,))
            new_room = cursor.fetchone()
            
            if not new_room:
                flash('New room not found.', 'danger')
                return redirect(url_for('admin.rooms'))
            
            # Count active occupants in new room
            cursor.execute("""
                SELECT COUNT(*) as count FROM room_occupancy 
                WHERE room_id = %s AND status = 'Active'
            """, (new_room_id,))
            count_result = cursor.fetchone()
            occupants = count_result.get('count', 0) if count_result else 0
            
            if occupants >= new_room['capacity']:
                flash(f'New room is at full capacity ({occupants}/{new_room["capacity"]}).', 'danger')
                return redirect(url_for('admin.rooms'))
            
            # Update occupancy
            cursor.execute("""
                UPDATE room_occupancy 
                SET room_id = %s
                WHERE id = %s
            """, (new_room_id, occupancy_id))
            db.connection.commit()
            
            cursor.execute("SELECT full_name FROM users WHERE id = %s", (occupancy['student_id'],))
            student = cursor.fetchone()
            
            cursor.execute("SELECT room_number FROM rooms WHERE id = %s", (new_room_id,))
            new_room_num = cursor.fetchone()
            
            flash(f"Student {student['full_name']} shifted to room {new_room_num['room_number']}.", 'success')
            
        except Exception as e:
            db.connection.rollback()
            flash(f'Error shifting student: {str(e)}', 'danger')
        
        cursor.close()
        return redirect(url_for('admin.rooms'))
    
    # GET request - show shift form
    cursor.execute("""
        SELECT student_id FROM room_occupancy WHERE id = %s
    """, (occupancy_id,))
    occupancy = cursor.fetchone()
    
    cursor.execute("""
        SELECT id, room_number, capacity,
               COUNT(ro.id) as occupants
        FROM rooms r
        LEFT JOIN room_occupancy ro ON r.id = ro.room_id AND ro.status = 'Active'
        WHERE r.id != %s
        GROUP BY r.id
        HAVING occupants < r.capacity
        ORDER BY r.room_number
    """, (current_room_id,))
    available_rooms = cursor.fetchall()
    
    cursor.execute("SELECT full_name FROM users WHERE id = %s", (occupancy['student_id'],))
    student = cursor.fetchone()
    
    cursor.close()
    
    html = f'''
    <div class="modal" id="shiftStudentModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <form method="POST">
                    <div class="modal-header" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); color: white;">
                        <h5 class="modal-title" style="font-weight: 700;"><i class="fas fa-exchange-alt"></i> Shift Student to Another Room</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p style="margin-bottom: 20px; font-weight: 500;">
                            <strong>Student:</strong> {student['full_name']}
                        </p>
                        <div class="mb-3">
                            <label class="form-label" style="font-weight: 700;">Select New Room *</label>
                            <select class="form-select" name="new_room_id" required style="border-width: 2px; font-weight: 500;">
                                <option value="">-- Choose Available Room --</option>
    '''
    
    for room in available_rooms:
        capacity_text = f"{room['occupants']}/{room['capacity']}"
        html += f'<option value="{room["id"]}">Room {room["room_number"]} ({capacity_text} occupied)</option>'
    
    html += '''
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary" style="font-weight: 700;"><i class="fas fa-exchange-alt"></i> Shift Student</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    '''
    
    return html


# ==================== HOSTEL SETTINGS ====================
@admin_bp.route('/update-hostel-info', methods=['POST'])
@login_required
@admin_required
def update_hostel_info():
    """Update hostel information in database"""
    try:
        cursor = db.connection.cursor()
        
        # Updates to apply
        updates = {
            'hostel_address': 'Zeal Chowk, Narhe, Pune',
            'hostel_phone': '7030710886',
            'hostel_email': 'hostelhub@work.com',
            'hostel_name': 'HostelHub',
            'warden_phone': '7030710886'
        }
        
        # Apply updates
        for setting_key, setting_value in updates.items():
            # Try to update
            cursor.execute(
                "UPDATE hostel_settings SET setting_value = %s WHERE setting_key = %s",
                (setting_value, setting_key)
            )
            
            # If no rows affected, insert
            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO hostel_settings (setting_key, setting_value) VALUES (%s, %s)",
                    (setting_key, setting_value)
                )
        
        db.connection.commit()
        
        flash('✅ Hostel information updated successfully!', 'success')
        return jsonify({'status': 'success', 'message': 'Hostel information updated'}), 200
        
    except Exception as e:
        db.connection.rollback()
        flash(f'❌ Error updating hostel information: {str(e)}', 'danger')
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        cursor.close()


# ==================== BULK UNALLOCATION ====================
@admin_bp.route('/unallocate-all-students', methods=['GET', 'POST'])
@login_required
@admin_required
def unallocate_all_students():
    """Unallocate all students from rooms"""
    cursor = db.connection.cursor()
    
    if request.method == 'POST':
        try:
            confirmation = request.form.get('confirmation', '').strip()
            
            if confirmation != 'yes':
                flash('Operation cancelled.', 'warning')
                return redirect(url_for('admin.rooms'))
            
            # Get count before unallocation
            cursor.execute("SELECT COUNT(*) as count FROM room_occupancy WHERE status = 'Active'")
            result = cursor.fetchone()
            count = result['count'] if result else 0
            
            if count == 0:
                flash('No students currently allocated to rooms.', 'info')
                return redirect(url_for('admin.rooms'))
            
            # Unallocate all students
            cursor.execute("""
                UPDATE room_occupancy 
                SET status = 'Inactive'
                WHERE status = 'Active'
            """)
            db.connection.commit()
            
            flash(f'✅ Successfully unallocated {count} student(s) from rooms! All students remain registered.', 'success')
            return redirect(url_for('admin.rooms'))
            
        except Exception as e:
            db.connection.rollback()
            flash(f'Error unallocating students: {str(e)}', 'danger')
            return redirect(url_for('admin.rooms'))
    
    # GET request - show confirmation page
    # Get list of currently allocated students
    cursor.execute("""
        SELECT 
            ro.id,
            u.full_name,
            s.roll_number,
            r.room_number,
            ro.check_in_date
        FROM room_occupancy ro
        JOIN users u ON ro.student_id = u.id
        JOIN students s ON u.id = s.user_id
        JOIN rooms r ON ro.room_id = r.id
        WHERE ro.status = 'Active'
        ORDER BY r.room_number
    """)
    
    allocated_students = cursor.fetchall() or []
    cursor.close()
    
    return render_template('admin/unallocate_confirmation.html', 
                         students=allocated_students,
                         total_count=len(allocated_students))
