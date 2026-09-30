from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime, timedelta
import sys
import os
from typing import Dict, Any, Union

# Add parent directory to Python path to import our database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lunch_system_database import SchoolLunchDB

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('Set SECRET_KEY before starting the application')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)

# Initialize database with absolute path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.environ.get('DATABASE_PATH', os.path.join(project_root, 'test.db'))
db = SchoolLunchDB(db_path)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if not username:
        flash('Enter your name')
        return redirect(url_for('index'))
    
    # Direct database query to avoid Row object issues
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        
        # Look for student by name (case-insensitive)
        cursor.execute("SELECT id, name FROM students WHERE LOWER(name) = LOWER(?)", (username,))
        student = cursor.fetchone()
        
        
        conn.close()
        
        if student:
            session.clear()
            session.permanent = True
            session['username'] = student[1]  # Use the actual name from database
            session['student_id'] = student[0]  # student ID
            return redirect(url_for('dashboard'))
        else:
            flash('Username not found')
            return redirect(url_for('index'))
            
    except Exception as e:
        app.logger.exception('Login failed')
        flash('Login is temporarily unavailable')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/api/meals')
def get_meals():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        meals = db.get_all_meals()
        meals_list = []
        
        if meals:  # Check if meals is not None
            for meal in meals:
                meals_list.append({
                    'id': meal[0],
                    'name': meal[1],
                    'description': meal[2],
                    'price': meal[3],
                    'category': meal[4],
                    'rating': round(meal[5], 1) if meal[5] else 0.0,  # meal[5] is rating
                    'rating_count': meal[6] if meal[6] else 0  # meal[6] is rating_count
                })
        
        return jsonify(meals_list)
    except Exception as e:
        app.logger.exception('Failed to load meals')
        return jsonify({'error': 'Failed to load meals'}), 500

@app.route('/api/order', methods=['POST'])
def order_meal():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    meal_id = data.get('meal_id')
    
    if not meal_id:
        return jsonify({'error': 'No meal selected'}), 400
    
    # Record the transaction
    student_id = session.get('student_id')
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        transaction_id = db.record_transaction(student_id, meal_id, today)
        return jsonify({'success': True, 'message': 'Order placed successfully!'})
    except Exception as e:
        return jsonify({'error': 'Failed to place order'}), 500

@app.route('/api/rate', methods=['POST'])
def rate_meal():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    meal_id = data.get('meal_id')
    rating = data.get('rating')
    
    if not meal_id or not rating:
        return jsonify({'error': 'Missing meal ID or rating'}), 400
    
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    success = db.rate_meal(meal_id, rating)
    if success:
        return jsonify({'success': True, 'message': 'Rating submitted!'})
    else:
        return jsonify({'error': 'Failed to submit rating'}), 500

@app.route('/api/import-openfoodfacts', methods=['POST'])
def import_from_openfoodfacts():
    """Importera måltider från Open Food Facts API"""
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    search_term = data.get('search_term', 'pasta')
    
    try:
        result = db.import_meals_from_openfoodfacts(search_term)
        
        if "error" in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'message': f"Importerade {result['added']} nya måltider för söktermen '{result['search_term']}'",
            'details': result
        })
    except Exception as e:
        return jsonify({'error': f'Import misslyckades: {str(e)}'}), 500

@app.route('/api/test-openfoodfacts')
def test_openfoodfacts():
    """Test-endpoint för att testa Open Food Facts API"""
    try:
        # Import här för att undvika problem om modulen inte finns
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from skolmaten_api import search_food_ingredients
        
        meals = search_food_ingredients("pasta")
        return jsonify({
            'success': True,
            'meals_found': len(meals),
            'sample_meals': meals[:3] if meals else []  # Visa första 3 som exempel
        })
    except ImportError:
        return jsonify({'error': 'Open Food Facts API inte tillgängligt'}), 500
    except Exception as e:
        return jsonify({'error': f'Test misslyckades: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='127.0.0.1', port=5000)

