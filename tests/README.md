# Tests Directory

This directory contains various test and utility scripts used during development and debugging.

## 📋 Test Files

### 🔐 Login Testing
- **`test_user_authentication.py`** - Test login functionality and display valid usernames
- **`test_login_functionality.py`** - Test database login logic directly
- **`verify_login_system.py`** - Alternative login functionality tester

### 👥 User Management Testing  
- **`display_user_database.py`** - Display all users from database (with Row object handling)
- **`show_all_students.py`** - Alternative user display utility

### 🔧 System Testing
- **`check_database_status.py`** - System status checker (database + web server)

## 🚀 Usage

Run any test from the root directory:

```bash
# Test login functionality
python tests/test_user_authentication.py

# Show all database users  
python tests/show_all_students.py

# Check system status
python tests/check_database_status.py

# Test database login logic
python tests/test_login_functionality.py
```

## 📝 Notes

- All tests expect `test.db` to exist in the root directory
- Some tests require the Flask web server to be running
- These are development/debugging tools, not production code
- Main system uses only the core files in the root directory

## 🗄️ Database Requirements

Tests work with the sample database containing:
- 20 test students (Alice Johnson, Bob Smith, etc.)
- 4 sample meals with rating system
- Transaction and meal schedule tables

Created during system development and consolidation phases.
