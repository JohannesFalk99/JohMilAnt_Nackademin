from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to Python path to import our database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from school_lunch_db import SchoolLunchDB

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize database
db = SchoolLunchDB('school_lunch.db')

def get_user_from_db(username, role=None):
    """
    Fetch user info from the database by username.
    Optionally filter by role.
    Returns dict with user info or None.
    """
    user = db.get_user_by_username(username)
    if not user:
        return None
    if role and user.get('role') != role:
        return None
    return user

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['userType']

    user = get_user_from_db(username, user_type)
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password or role')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = get_user_from_db(session['username'])
    if not user:
        flash('User not found')
        return redirect(url_for('index'))

    stats = db.get_statistics()
    today = datetime.now().strftime('%Y-%m-%d')

    return render_template('dashboard.html',
                         user_name=user['name'],
                         user_role=user['role'],
                         stats=stats,
                         current_time=datetime.now())

@app.route('/api/meals/today')
def get_todays_meals():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    today = datetime.now().strftime('%Y-%m-%d')
    meals = db.get_meals_by_date(today)

    if not meals:
        meals = db.get_all_meals()

    meals_list = []
    for meal in meals:
        meal_dict = {
            'id': meal[0],
            'name': meal[1],
            'description': meal[2],
            'price': meal[3],
            'category': meal[4],
            'picture_url': meal[5] or '/static/images/default-meal.jpg',
            'allergens': meal[6],
            'ingredients': meal[7],
            'calories': meal[9],
            'preparation_time': meal[10],
            'serving_size': meal[11],
            'is_vegetarian': bool(meal[13]),
            'is_vegan': bool(meal[14]),
            'is_gluten_free': bool(meal[15]),
            'is_halal': bool(meal[16]),
            'is_kosher': bool(meal[17]),
            'spice_level': meal[18]
        }
        meals_list.append(meal_dict)

    return jsonify(meals_list)

@app.route('/api/meals/filter/<filter_type>')
def filter_meals(filter_type):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    if filter_type == 'all':
        meals = db.get_all_meals()
    else:
        meals = db.get_meals_by_dietary_restriction(filter_type)

    meals_list = []
    for meal in meals:
        meal_dict = {
            'id': meal[0],
            'name': meal[1],
            'description': meal[2],
            'price': meal[3],
            'category': meal[4],
            'picture_url': meal[5] or '/static/images/default-meal.jpg',
            'allergens': meal[6],
            'is_vegetarian': bool(meal[13]),
            'is_vegan': bool(meal[14]),
            'is_gluten_free': bool(meal[15]),
            'is_halal': bool(meal[16]),
            'spice_level': meal[18]
        }
        meals_list.append(meal_dict)

    return jsonify(meals_list)

@app.route('/api/order', methods=['POST'])
def place_order():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_from_db(session['username'])
    if not user or user['role'] != 'student':
        return jsonify({'error': 'Only students can place orders'}), 403

    data = request.get_json()
    meal_ids = data.get('meal_ids', [])

    if not meal_ids:
        return jsonify({'error': 'No meals selected'}), 400

    student_id = user.get('student_id', 1)
    today = datetime.now().strftime('%Y-%m-%d')

    order_ids = []
    for meal_id in meal_ids:
        transaction_id = db.record_transaction(
            student_id=student_id,
            meal_id=meal_id,
            date=today,
            external_transaction_id=None
        )
        order_ids.append(transaction_id)

    return jsonify({
        'success': True,
        'message': f'Order placed successfully! {len(meal_ids)} meals ordered.',
        'order_ids': order_ids
    })

@app.route('/api/orders/history')
def get_order_history():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_from_db(session['username'])
    if not user or user['role'] not in ['student', 'staff']:
        return jsonify({'error': 'Only students and staff can view order history'}), 403

    student_id = user.get('student_id', 1)
    history = db.get_meal_history(student_id, limit=20)

    orders = []
    for order in history:
        orders.append({
            'id': order[0],
            'meal_name': order[-1],
            'date': order[3],
            'status': order[5] if len(order) > 5 else 'completed',
            'created_at': order[6] if len(order) > 6 else order[3]
        })

    return jsonify(orders)

@app.route('/api/stats/dashboard')
def get_dashboard_stats():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    stats = db.get_statistics()
    today = datetime.now().strftime('%Y-%m-%d')
    daily_transactions = db.get_daily_transactions(today)

    return jsonify({
        'total_students': stats.get('total_students', 0),
        'total_meals': stats.get('total_meals', 0),
        'orders_today': len(daily_transactions) if daily_transactions else 0,
        'students_online': 248,
        'current_time': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/reports/<report_type>')
def get_reports(report_type):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = get_user_from_db(session['username'])
    if not user or user['role'] not in ['admin', 'staff']:
        return jsonify({'error': 'Insufficient permissions'}), 403

    if report_type == 'popular_meals':
        data = db.generate_report('popular_meals')
    elif report_type == 'daily_sales':
        today = datetime.now().strftime('%Y-%m-%d')
        data = db.generate_report('daily_sales', {'date': today})
    elif report_type == 'student_activity':
        data = db.generate_report('all_student_activity')
    else:
        return jsonify({'error': 'Invalid report type'}), 400

    return jsonify(data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    db.setup_initial_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        return jsonify({'error': 'Invalid report type'}), 400
    
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    # Setup initial data if database is empty
    db.setup_initial_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
