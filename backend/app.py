from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db, init_db
import os

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Admin Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', 'admin')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if user_type == 'admin':
        cursor.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            conn.close()
            return jsonify({'success': True, 'message': 'Login successful', 'user_type': 'admin'})
    else:  # student login
        cursor.execute('SELECT * FROM students WHERE email = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            conn.close()
            return jsonify({'success': True, 'message': 'Login successful', 'user_type': 'student', 'student_id': user['id'], 'student_name': user['name']})
    
    conn.close()
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# Room Management
@app.route('/api/rooms', methods=['GET', 'POST'])
def rooms():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM rooms')
        rooms = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(rooms)
    
    elif request.method == 'POST':
        data = request.json
        try:
            cursor.execute('''
                INSERT INTO rooms (room_number, room_type, capacity, price, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['room_number'], data['room_type'], data['capacity'], 
                  data['price'], data.get('status', 'available')))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Room added successfully'})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/rooms/<int:room_id>', methods=['PUT', 'DELETE'])
def room_detail(room_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE rooms 
            SET room_number = ?, room_type = ?, capacity = ?, price = ?, status = ?
            WHERE id = ?
        ''', (data['room_number'], data['room_type'], data['capacity'], 
              data['price'], data['status'], room_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Room updated successfully'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Room deleted successfully'})

# Student Management
@app.route('/api/students', methods=['GET', 'POST'])
def students():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM students')
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(students)
    
    elif request.method == 'POST':
        data = request.json
        try:
            cursor.execute('''
                INSERT INTO students (name, email, phone, address, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['name'], data['email'], data['phone'], data.get('address', ''), data.get('password', '123456')))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Student added successfully'})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/students/<int:student_id>', methods=['PUT', 'DELETE'])
def student_detail(student_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE students 
            SET name = ?, email = ?, phone = ?, address = ?, password = ?
            WHERE id = ?
        ''', (data['name'], data['email'], data['phone'], data['address'], data.get('password', '123456'), student_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student updated successfully'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student deleted successfully'})

# Booking Management
@app.route('/api/bookings', methods=['GET', 'POST'])
def bookings():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT b.*, s.name as student_name, r.room_number 
            FROM bookings b
            JOIN students s ON b.student_id = s.id
            JOIN rooms r ON b.room_id = r.id
        ''')
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(bookings)
    
    elif request.method == 'POST':
        data = request.json
        try:
            cursor.execute('''
                INSERT INTO bookings (student_id, room_id, check_in_date, check_out_date, amount_paid, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['student_id'], data['room_id'], data['check_in_date'], 
                  data.get('check_out_date'), data.get('amount_paid', 0), data.get('status', 'active')))
            
            # Update room status
            cursor.execute('UPDATE rooms SET status = ? WHERE id = ?', ('occupied', data['room_id']))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Booking created successfully'})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/bookings/<int:booking_id>', methods=['PUT', 'DELETE'])
def booking_detail(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE bookings 
            SET student_id = ?, room_id = ?, check_in_date = ?, 
                check_out_date = ?, amount_paid = ?, status = ?
            WHERE id = ?
        ''', (data['student_id'], data['room_id'], data['check_in_date'],
              data['check_out_date'], data['amount_paid'], data['status'], booking_id))
        
        # Update room status if booking is completed
        if data['status'] == 'completed':
            cursor.execute('UPDATE rooms SET status = ? WHERE id = ?', ('available', data['room_id']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Booking updated successfully'})
    
    elif request.method == 'DELETE':
        # Get room_id before deleting
        cursor.execute('SELECT room_id FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()
        if booking:
            cursor.execute('UPDATE rooms SET status = ? WHERE id = ?', ('available', booking['room_id']))
        
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Booking deleted successfully'})

# Dashboard Stats
@app.route('/api/stats', methods=['GET'])
def stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM rooms')
    total_rooms = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as occupied FROM rooms WHERE status = "occupied"')
    occupied_rooms = cursor.fetchone()['occupied']
    
    cursor.execute('SELECT COUNT(*) as total FROM students')
    total_students = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as active FROM bookings WHERE status = "active"')
    active_bookings = cursor.fetchone()['active']
    
    cursor.execute('SELECT SUM(amount_paid) as revenue FROM bookings')
    total_revenue = cursor.fetchone()['revenue'] or 0
    
    conn.close()
    
    return jsonify({
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': total_rooms - occupied_rooms,
        'total_students': total_students,
        'active_bookings': active_bookings,
        'total_revenue': total_revenue
    })

# Feedback Management
@app.route('/api/feedback', methods=['GET', 'POST'])
def feedback():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        if student_id:
            cursor.execute('''
                SELECT f.*, s.name as student_name 
                FROM feedback f
                JOIN students s ON f.student_id = s.id
                WHERE f.student_id = ?
                ORDER BY f.created_date DESC
            ''', (student_id,))
        else:
            cursor.execute('''
                SELECT f.*, s.name as student_name 
                FROM feedback f
                JOIN students s ON f.student_id = s.id
                ORDER BY f.created_date DESC
            ''')
        feedbacks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(feedbacks)
    
    elif request.method == 'POST':
        data = request.json
        try:
            cursor.execute('''
                INSERT INTO feedback (student_id, subject, message, status)
                VALUES (?, ?, ?, ?)
            ''', (data['student_id'], data['subject'], data['message'], 'pending'))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/feedback/<int:feedback_id>', methods=['PUT', 'DELETE'])
def feedback_detail(feedback_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute('''
            UPDATE feedback 
            SET status = ?, admin_reply = ?
            WHERE id = ?
        ''', (data.get('status', 'pending'), data.get('admin_reply', ''), feedback_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Feedback updated successfully'})
    
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Feedback deleted successfully'})

# Student Dashboard
@app.route('/api/student/dashboard/<int:student_id>', methods=['GET'])
def student_dashboard(student_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Get student info
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = dict(cursor.fetchone())
    
    # Get active booking
    cursor.execute('''
        SELECT b.*, r.room_number, r.room_type, r.price
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE b.student_id = ? AND b.status = 'active'
    ''', (student_id,))
    booking = cursor.fetchone()
    booking = dict(booking) if booking else None
    
    # Get feedback count
    cursor.execute('SELECT COUNT(*) as count FROM feedback WHERE student_id = ?', (student_id,))
    feedback_count = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'student': student,
        'booking': booking,
        'feedback_count': feedback_count
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
