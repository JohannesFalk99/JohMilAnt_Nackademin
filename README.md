# School Lunch System (Skolmatssystem)

A comprehensive school lunch management system built with Python, Flask, and SQLite. This system allows students to view meal options, place orders, rate meals, and manage their lunch accounts.

## 📋 Overview

This project is a school lunch ordering and management system that provides:
- Student authentication and login
- Meal browsing and ordering
- Rating system for meals
- Transaction tracking
- Sample data generation for testing
- Web-based user interface

## 🗂️ File Structure and Documentation

### Core Database Files

#### `database_wrapper.py`
**Purpose**: Low-level SQLite database wrapper with thread-safe connection management.

**Key Features**:
- Thread-safe database connections using `threading.local()`
- Context manager support for transactions
- Automatic commit/rollback handling
- Row factory for dictionary-like result access

**Main Methods**:
- `execute(sql, params)` - Execute SELECT queries and return results
- `execute_write(sql, params)` - Execute INSERT/UPDATE/DELETE and return last row ID
- `transaction()` - Context manager for atomic operations
- `close()` - Close database connection

**Usage Example**:
```python
db = SQLiteDB('test.db')
results = db.execute("SELECT * FROM students WHERE grade = ?", ["9"])
```

---

#### `lunch_system_database.py`
**Purpose**: High-level database abstraction layer for the school lunch system.

**Key Features**:
- Complete database schema management (students, meals, meal_schedule, transactions)
- Student management operations (add, update, search, get all)
- Meal management (add, rate, schedule, search)
- Transaction recording and history tracking
- Rating system with average calculation
- JSON menu import functionality

**Database Schema**:
- **students**: id, name, grade, class, allergies, external_account_id, created_at
- **meals**: id, name, description, price, category, rating, rating_count, created_at
- **meal_schedule**: id, meal_id, date, available_quantity, created_at
- **transactions**: id, student_id, meal_id, date, external_transaction_id, status, created_at

**Main Methods**:
- `initialize_database()` - Create all required tables
- `add_student(student_info)` - Register a new student
- `add_meal(meal_info)` - Add a new meal option
- `get_all_students()` - Retrieve all registered students
- `get_all_meals()` - Retrieve all available meals
- `record_transaction(student_id, meal_id, date)` - Record a meal purchase
- `rate_meal(meal_id, rating)` - Submit a meal rating (1-5 stars)
- `import_menu_from_json(json_file_path)` - Import meals from JSON file

---

### Utility Scripts

#### `create_sample_database.py`
**Purpose**: Generate a complete test database with sample students, meals, and transactions.

**Key Features**:
- Creates 25 sample Swedish students with realistic names and allergies
- Generates 10 Swedish meal options with pricing and ratings
- Creates 30 days of historical transaction data
- Command-line interface with options for reset and verbose output
- Automatic database initialization

**Sample Data Includes**:
- Students: Alice Johansson, Björn Svensson, Caroline Andersson, etc.
- Meals: Köttbullar med potatismos, Laxpasta, Vegetarisk lasagne, etc.
- Random transactions spread across 30 days

**Command-line Usage**:
```bash
# Create/update database with default settings
python create_sample_database.py

# Reset database (remove existing data)
python create_sample_database.py --reset

# Verbose output mode
python create_sample_database.py --verbose

# Custom database path
python create_sample_database.py --database my_lunch.db
```

**Arguments**:
- `--reset` - Remove existing database before creating new one
- `--verbose` / `-v` - Show detailed output during setup
- `--database` / `-d` - Specify custom database file path (default: test.db)

---

#### `launch_application.py`
**Purpose**: Simple launcher script to set up and start the entire application.

**Key Features**:
- Automatically creates database if it doesn't exist
- Launches the Flask web server
- Handles graceful shutdown on Ctrl+C
- Provides access URL to user

**Usage**:
```bash
python launch_application.py
```

The application will be available at: http://127.0.0.1:5000

---

### Web Interface

#### `web_interface/flask_server.py`
**Purpose**: Flask web server providing the REST API and web interface for the lunch system.

**Key Features**:
- Session-based authentication (username only, no password)
- RESTful API endpoints for meals and orders
- HTML template rendering for login and dashboard
- Real-time meal data retrieval
- Order placement and rating submission

**Routes**:
- `GET /` - Login page (redirects to dashboard if already logged in)
- `POST /login` - Process login with student name
- `GET /logout` - Clear session and return to login
- `GET /dashboard` - Main dashboard for logged-in students
- `GET /api/meals` - JSON endpoint returning all available meals
- `POST /api/order` - Place a meal order
- `POST /api/rate` - Submit a meal rating

**API Response Examples**:

`GET /api/meals`:
```json
[
  {
    "id": 1,
    "name": "Köttbullar med potatismos",
    "description": "Klassiska svenska köttbullar...",
    "price": 120.00,
    "category": "Huvudrätt",
    "rating": 4.6,
    "rating_count": 30
  }
]
```

`POST /api/order`:
```json
{
  "meal_id": 1
}
```

---

#### `web_interface/templates/`
**Purpose**: HTML templates for the web interface.

**Files**:
- `login.html` - Login page where students enter their name
- `dashboard.html` - Main student dashboard showing available meals
- `dashboard_new.html` - Alternative/newer dashboard design (development version)

**Template Features**:
- Bootstrap-based responsive design
- JavaScript for dynamic meal loading
- AJAX calls for ordering and rating
- Session management integration

---

### Tests Directory

#### `tests/README.md`
**Purpose**: Documentation for all test and utility scripts.

**Contents**: Describes the purpose and usage of each test file in the tests directory.

---

#### `tests/test_user_authentication.py`
**Purpose**: Validate login functionality and display valid usernames from the database.

**Key Features**:
- Lists all students in the database with their IDs and allergies
- Provides login instructions
- Shows example usernames to try
- Directly connects to test.db for validation

**Usage**:
```bash
python tests/test_user_authentication.py
```

---

#### `tests/test_login_functionality.py`
**Purpose**: Test the database login logic directly without web server.

**Usage**:
```bash
python tests/test_login_functionality.py
```

---

#### `tests/verify_login_system.py`
**Purpose**: Alternative login functionality tester.

**Usage**:
```bash
python tests/verify_login_system.py
```

---

#### `tests/display_user_database.py`
**Purpose**: Display all users from database with proper Row object handling.

**Key Features**:
- Handles SQLite Row objects correctly
- Displays formatted student information
- Shows allergies and account details

**Usage**:
```bash
python tests/display_user_database.py
```

---

#### `tests/show_all_students.py`
**Purpose**: Alternative utility to display all students in the database.

**Usage**:
```bash
python tests/show_all_students.py
```

---

#### `tests/check_database_status.py`
**Purpose**: System health checker that validates database and web server status.

**Key Features**:
- Checks if test.db exists and is accessible
- Validates database schema
- Checks web server availability
- Provides diagnostic information

**Usage**:
```bash
python tests/check_database_status.py
```

---

#### `tests/test_login.py` and `tests/print_users.py`
**Purpose**: Additional testing utilities for user management and authentication.

---

### Database File

#### `test.db`
**Purpose**: SQLite database file containing all application data.

**Contents**:
- Student records
- Meal options
- Meal schedules
- Transaction history

**Note**: This file is created automatically by `create_sample_database.py` or `launch_application.py`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Flask (for web interface)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JohannesFalk99/JohMilAnt_Nackademin.git
cd JohMilAnt_Nackademin
```

2. Install dependencies:
```bash
pip install flask
```

### Quick Start

**Option 1: Using the launcher script (Recommended)**
```bash
python launch_application.py
```

**Option 2: Manual setup**
```bash
# Create sample database
python create_sample_database.py --reset

# Start web server
python web_interface/flask_server.py
```

3. Open your browser and navigate to: http://127.0.0.1:5000

4. Login with any student name (case insensitive):
   - Alice Johansson
   - Björn Svensson
   - Caroline Andersson
   - etc. (see full list in `tests/test_user_authentication.py`)

---

## 🎯 Features

### For Students
- **Simple Login**: Enter your name to access the system (no password required)
- **View Meals**: Browse available meal options with descriptions and prices
- **Place Orders**: Order meals with a single click
- **Rate Meals**: Provide feedback with a 5-star rating system
- **View History**: See your past orders and transactions

### For Administrators
- **Student Management**: Add and manage student records with allergy information
- **Meal Management**: Create and update meal options with pricing
- **Transaction Tracking**: Monitor all meal purchases
- **Rating Analytics**: View average ratings and feedback for each meal

### Technical Features
- **Thread-Safe Database**: Multi-threaded access with proper transaction handling
- **RESTful API**: JSON-based API for integration with other systems
- **Sample Data**: Realistic test data for development and demonstration
- **Comprehensive Testing**: Multiple test utilities for validation

---

## 📊 Database Schema

### Students Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| name | TEXT | Student full name |
| grade | TEXT | Student grade level |
| class | TEXT | Class identifier (e.g., "9A") |
| allergies | TEXT | Comma-separated allergen list |
| external_account_id | TEXT | External system reference |
| created_at | TIMESTAMP | Record creation time |

### Meals Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| name | TEXT | Meal name |
| description | TEXT | Detailed description |
| price | REAL | Cost in currency |
| category | TEXT | Meal category |
| rating | REAL | Average rating (0-5) |
| rating_count | INTEGER | Number of ratings |
| created_at | TIMESTAMP | Record creation time |

### Transactions Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| student_id | INTEGER | Foreign key to students.id |
| meal_id | INTEGER | Foreign key to meals.id |
| date | DATE | Transaction date |
| external_transaction_id | TEXT | External system reference |
| status | TEXT | Transaction status |
| created_at | TIMESTAMP | Record creation time |

---

## 🔧 Development

### Running Tests
```bash
# Test authentication
python tests/test_user_authentication.py

# Check system status
python tests/check_database_status.py

# Display all students
python tests/show_all_students.py
```

### Database Reset
```bash
python create_sample_database.py --reset --verbose
```

### Custom Database Path
```bash
python create_sample_database.py --database custom.db
```

---

## 📝 Notes

- **Authentication**: The system uses simple name-based authentication without passwords (suitable for school environments)
- **Language**: Interface and sample data are in Swedish (svenska)
- **Allergies**: System tracks student allergies but doesn't currently filter meals automatically
- **Development Status**: This is a development/educational project with sample data

---

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your own learning purposes.

---

## 📄 License

This project is part of an educational assignment at Nackademin.

---

## 👥 Authors

- JohannesFalk99
- Milad
- Antonio

---

## 🆘 Support

For issues or questions:
1. Check the test utilities in the `tests/` directory
2. Review the inline documentation in each Python file
3. Examine the database schema documentation above

---

## 🔍 Quick Reference

### Most Important Files
1. `launch_application.py` - Start here to run the application
2. `create_sample_database.py` - Set up test data
3. `lunch_system_database.py` - Core database logic
4. `web_interface/flask_server.py` - Web server and API

### Common Tasks
- **Start application**: `python launch_application.py`
- **Reset database**: `python create_sample_database.py --reset`
- **Test login**: `python tests/test_user_authentication.py`
- **Check status**: `python tests/check_database_status.py`
