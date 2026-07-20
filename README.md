# Hostel Management System

A comprehensive web-based hostel management system built with Flask and MySQL. This system provides role-based access for students, admins, and wardens with complete features for hostel operations.

## Features

### 🔐 Authentication & Authorization
- Role-based access control (Student, Admin, Warden)
- Secure password hashing with bcrypt
- Session management
- Login/Logout functionality

### 📊 Student Dashboard
- View allocated room details
- Submit and track complaints
- Request visitor entry
- Check fee status and payment history
- View hostel notices
- View roommate information
- Update personal profile

### 👨‍💼 Admin Dashboard
- System statistics and overview
- Room management (add, update, delete, allocate)
- Student management
- Complaint management and resolution
- Visitor request approval/rejection
- Fee management and payment tracking
- Notice publishing and management
- Hostel settings configuration

### 🏢 Warden Dashboard
- Monitor hostel activities
- Review and manage complaints
- Approve/reject visitor requests
- View room allocation
- Access student information
- Manage notices

### 🌐 Public Features
- Attractive landing page with hostel information
- Statistics section
- Hostel facilities showcase
- Gallery with hostel images
- Testimonials from students
- Contact information
- Notices display

### 📋 Core Features
1. **Room Management** - Add, update, delete, allocate rooms
2. **Complaint System** - Submit, track, and resolve complaints
3. **Visitor Management** - Request and approve visitor entry
4. **Fee Management** - Track fees, payments, and pending amounts
5. **Notice Board** - Publish and manage hostel notices
6. **Gallery** - Display hostel images and facilities
7. **Contact** - Hostel contact information and map

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Authentication**: Flask-Login, bcrypt
- **ORM**: MySQLdb for database operations

## System Requirements

- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

## Installation & Setup

### 1. Clone the Repository
```bash
cd /home/prajwal/Programs/Hostel
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database

**Option A: Using MySQL Command Line**
```bash
mysql -u root -p < config/database.sql
```

**Option B: Manual Setup**
- Start MySQL server
- Open MySQL command line or MySQL Workbench
- Execute the SQL script: `config/database.sql`

### 4. Configure Environment Variables
Edit `.env` file with your MySQL credentials:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=hostel_management
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Default Login Credentials

### Demo Accounts

**Admin:**
- Username: `admin`
- Password: `admin123`

**Warden:**
- Username: `warden`
- Password: `admin123`

**Student Accounts:**
- Username: `prajwal` | Password: `admin123`
- Username: `rajdeep` | Password: `admin123`
- Username: `rutuja` | Password: `admin123`

## Project Structure

```
Hostel/
├── app.py                          # Main Flask application
├── config/
│   ├── config.py                   # Configuration settings
│   ├── database.py                 # Database connection handler
│   └── database.sql                # MySQL schema
├── routes/
│   ├── admin_routes.py             # Admin functionality
│   ├── student_routes.py           # Student functionality
│   └── warden_routes.py            # Warden functionality
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── gallery.html                # Gallery page
│   ├── contact.html                # Contact page
│   ├── admin/
│   │   ├── dashboard.html          # Admin dashboard
│   │   ├── rooms.html              # Room management
│   │   ├── complaints.html         # Complaint management
│   │   ├── visitors.html           # Visitor management
│   │   ├── notices.html            # Notice management
│   │   ├── fees.html               # Fee management
│   │   └── students.html           # Student list
│   ├── student/
│   │   ├── dashboard.html          # Student dashboard
│   │   ├── profile.html            # Student profile
│   │   ├── room.html               # Room details
│   │   ├── complaints.html         # Complaints list
│   │   ├── complaint_detail.html    # Complaint details
│   │   ├── visitors.html           # Visitor requests
│   │   ├── fees.html               # Fee details
│   │   └── notices.html            # Notices list
│   └── warden/
│       ├── dashboard.html          # Warden dashboard
│       ├── complaints.html         # Complaints
│       ├── visitors.html           # Visitor management
│       ├── rooms.html              # Room information
│       ├── students.html           # Student list
│       └── notices.html            # Notices
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── README.md                       # This file
```

## Database Schema

### Main Tables
- **users** - User accounts with roles
- **students** - Student-specific information
- **rooms** - Room inventory
- **room_occupancy** - Student-room allocation
- **complaints** - Complaint management
- **visitors** - Visitor requests
- **fees** - Fee management
- **notices** - Hostel notices
- **gallery** - Image gallery
- **payment_history** - Payment records
- **hostel_settings** - Configuration settings

## Features in Detail

### Student Features
- Register with personal and academic information
- Secure login with password encryption
- View personalized dashboard
- Access allocated room information
- View roommate details
- Submit complaints with categories
- Track complaint status (Pending, In Progress, Resolved)
- Request visitor entry
- View pending visitor requests
- Check fee status and payment history
- View hostel notices
- Update profile information

### Admin Features
- Monitor all hostel activities from dashboard
- Manage room inventory (add, edit, delete)
- Allocate rooms to students
- View room availability and occupancy
- Manage student records
- Review and resolve complaints
- Assign complaint priorities
- Approve/reject visitor requests
- Record fee payments
- Track fee status (Pending, Partial, Paid, Overdue)
- Publish, edit, and delete notices
- Pin important notices
- Manage hostel settings
- View system statistics and charts

### Warden Features
- Monitor hostel operations
- View complaint list with priorities
- Approve/reject visitor requests
- Review room allocations
- Access student information
- Manage notices
- Generate hostel activity reports

## Key Functionalities

### 1. Authentication System
- Bcrypt password hashing
- Session-based authentication
- Role-based access control
- Secure logout

### 2. Room Management
- Add rooms with types (Single Deluxe, Double Sharing, etc.)
- Track occupancy and availability
- Display amenities
- Set rental rates per room

### 3. Complaint System
- Submit complaints with category and priority
- Track complaint status
- Admin can assign and update status
- Resolution notes for closure
- Complaint history

### 4. Visitor Management
- Submit visitor requests with date/time
- Track approval status
- View visitor history
- Admin/Warden approval workflow

### 5. Fee Management
- Display fee structure (room rent, mess, utilities, other)
- Track payment status
- Record multiple payments
- Display payment history with methods

### 6. Notice Board
- Publish notices with categories
- Pin important notices
- Set notice visibility (All, Students, Admin, Warden)
- Pin priority notices

## API Endpoints

### Authentication Routes
- `GET/POST /login` - User login
- `GET/POST /register` - Student registration
- `GET /logout` - User logout
- `GET /dashboard` - Redirect to role dashboard

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET/POST /student/profile` - View/edit profile
- `GET/POST /student/complaints` - Complaints management
- `GET /student/complaint/<id>` - Complaint details
- `GET/POST /student/visitors` - Visitor requests
- `GET /student/fees` - Fee information
- `GET /student/room` - Room details
- `GET /student/notices` - Hostel notices

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET/POST /admin/rooms` - Room management
- `GET/POST /admin/allocate-room` - Allocate rooms
- `GET/POST /admin/complaints` - Complaint management
- `GET/POST /admin/visitors` - Visitor management
- `GET/POST /admin/notices` - Notice management
- `GET/POST /admin/fees` - Fee management
- `GET /admin/students` - Student list

### Warden Routes
- `GET /warden/dashboard` - Warden dashboard
- `GET /warden/complaints` - Complaints
- `GET/POST /warden/visitors` - Visitor approval
- `GET /warden/rooms` - Room information
- `GET /warden/students` - Student list
- `GET /warden/notices` - Notices

### Public Routes
- `GET /` - Home page
- `GET /gallery` - Gallery
- `GET /contact` - Contact information
- `GET /about` - About page

## Security Features

1. **Password Security**
   - Bcrypt hashing with salt
   - Minimum 6 character requirement
   - Password confirmation on registration

2. **Access Control**
   - Role-based access decorators
   - Login required checks
   - Unauthorized access prevention

3. **Data Protection**
   - SQL injection prevention with parameterized queries
   - XSS protection through template escaping
   - CSRF protection in forms

4. **Session Management**
   - Secure session handling
   - User-specific data isolation
   - Logout functionality

## Future Enhancements

- Email notifications for complaints and visitor approvals
- SMS alerts for fee reminders
- File upload for complaint images
- Advanced reporting and analytics
- Mobile app for students
- Attendance tracking
- Mess billing integration
- Maintenance schedule management
- Online payment integration
- Student disciplinary records

## Troubleshooting

### MySQL Connection Error
- Check if MySQL server is running
- Verify credentials in `.env` file
- Ensure database is created: `mysql -u root -p < config/database.sql`

### Import Errors
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+)

### Port Already in Use
- Change port in app.py: `app.run(debug=True, port=5001)`

### Database Not Found
- Execute database.sql script
- Check MYSQL_DB name in .env file

## Support & Contact

For issues or questions:
- Check the documentation above
- Review database schema in `config/database.sql`
- Verify all dependencies are installed

## License

This project is open-source and available for educational and commercial use.

## Contributors

- Prajwal Tandekar
- Development Team

---

**Last Updated**: July 2024
**Version**: 1.0.0
