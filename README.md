# 🏨 Hostel Management System

A complete web-based hostel management system with a beautiful UI, featuring separate admin and student portals. Built with HTML/CSS/JavaScript frontend and Python Flask backend with SQLite database.

![Login Page](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Admin Portal
- 📊 **Dashboard**: View real-time statistics (total rooms, occupancy, revenue, active bookings)
- 🏠 **Room Management**: Add, edit, delete rooms with different types and pricing
- 👥 **Student Management**: Manage student records with contact information and login credentials
- 📅 **Booking Management**: Handle check-ins, check-outs, and payment tracking
- 💬 **Feedback Management**: View and reply to student queries and feedback
- 🔐 **Secure Authentication**: Admin login system

### Student Portal
- 🏠 **Personal Dashboard**: View assigned room details and booking information
- 💬 **Feedback System**: Submit queries and feedback to admin
- 📝 **View Responses**: Check admin replies to submitted feedback
- 📊 **Booking Details**: Track check-in/check-out dates and payment status

## 🎨 Screenshots

- **Beautiful Login Page**: Modern glassmorphism design with animated background
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Intuitive Interface**: Easy-to-use admin and student dashboards

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite
- **API**: RESTful API architecture

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hostel-management-system.git
cd hostel-management-system
```

### Step 2: Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 3: Initialize Database

```bash
python backend/database.py
```

### Step 4: Run Backend Server

```bash
python backend/app.py
```

The backend will run on `http://localhost:5000`

### Step 5: Run Frontend Server

Open a new terminal and run:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser

## 🔑 Default Login Credentials

### Admin Login
- **Username**: `admin`
- **Password**: `admin123`

### Student Login
- Students need to be registered by admin first
- Default password for new students: `123456`
- Login with registered email and password

## 📁 Project Structure

```
hostel-management-system/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── database.py               # Database initialization
│   ├── requirements.txt          # Python dependencies
│   └── hostel.db                # SQLite database (auto-generated)
├── frontend/
│   ├── index.html               # Login page
│   ├── dashboard.html           # Admin dashboard
│   ├── rooms.html               # Room management
│   ├── students.html            # Student management
│   ├── bookings.html            # Booking management
│   ├── feedback.html            # Admin feedback management
│   ├── student-dashboard.html   # Student dashboard
│   ├── student-feedback.html    # Student feedback view
│   ├── css/
│   │   └── style.css           # Styles
│   └── js/
│       └── main.js             # JavaScript utilities
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/login` - Admin/Student login

### Dashboard
- `GET /api/stats` - Dashboard statistics
- `GET /api/student/dashboard/<student_id>` - Student dashboard data

### Room Management
- `GET /api/rooms` - Get all rooms
- `POST /api/rooms` - Add new room
- `PUT /api/rooms/<id>` - Update room
- `DELETE /api/rooms/<id>` - Delete room

### Student Management
- `GET /api/students` - Get all students
- `POST /api/students` - Add new student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### Booking Management
- `GET /api/bookings` - Get all bookings
- `POST /api/bookings` - Create booking
- `PUT /api/bookings/<id>` - Update booking
- `DELETE /api/bookings/<id>` - Delete booking

### Feedback Management
- `GET /api/feedback` - Get all feedback
- `POST /api/feedback` - Submit feedback
- `PUT /api/feedback/<id>` - Reply to feedback
- `DELETE /api/feedback/<id>` - Delete feedback

## 🚀 Usage Guide

### For Admin:
1. Login with admin credentials
2. Add rooms with different types (Single, Double, Triple, Quad)
3. Register students with their details and set passwords
4. Create bookings by assigning students to available rooms
5. Track payments and manage check-ins/check-outs
6. View and reply to student feedback
7. Monitor dashboard for quick statistics

### For Students:
1. Login with email and password provided by admin
2. View assigned room details
3. Check booking information and payment status
4. Submit feedback or queries
5. View admin responses to feedback

## 🔒 Security Notes

- This is a development version with basic authentication
- For production use, implement:
  - Password hashing (bcrypt, argon2)
  - JWT tokens for session management
  - HTTPS encryption
  - Input validation and sanitization
  - Rate limiting
  - CSRF protection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Your Name - [Your GitHub Profile](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- Background image from [Unsplash](https://unsplash.com)
- Icons and emojis for better UI/UX
- Flask framework and community

## 📧 Contact

For any queries or suggestions, please open an issue or contact at your.email@example.com

---

⭐ If you found this project helpful, please give it a star!
