# JohMilAnt_Nackademin

**Gruppprojekt, examinerande**

A modular Python project template with proper error handling, logging, and testing infrastructure.

## 🚀 Features

- ✅ **Modular Architecture**: Well-organized code structure with separate modules
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Input Validation**: Sanitization and validation of user inputs
- ✅ **Testing Framework**: Unit tests with pytest
- ✅ **Type Hints**: Full type annotation support
- ✅ **Configuration Management**: Environment-based configuration
- ✅ **Code Quality**: Linting and formatting tools included

## 📁 Project Structure

```
JohMilAnt_Nackademin/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py           # Utility functions
│   └── modules/
│       ├── __init__.py
│       └── core.py              # Core application logic
├── tests/
│   ├── __init__.py
│   ├── test_main.py             # Tests for main module
│   └── test_utils.py            # Tests for utilities
├── main.py                      # Main entry point
├── requirements.txt             # Project dependencies
├── pyproject.toml              # Project configuration
├── CODE_REVIEW.md              # Code review report
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JohannesFalk99/JohMilAnt_Nackademin.git
   cd JohMilAnt_Nackademin
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Running the Application

```bash
python main.py
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_main.py -v
```

### Code Quality Checks

```bash
# Code formatting with black
black .

# Linting with flake8
flake8 src tests

# Type checking with mypy
mypy src
```

## 🔧 Configuration

The application uses environment variables for configuration:

- `DEBUG`: Set to 'true' to enable debug mode
- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Example:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python main.py
```

## 🧪 Testing

The project includes comprehensive tests:

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test module interactions
- **Input Validation Tests**: Test security and data validation

### Test Coverage

Run tests with coverage report:
```bash
python -m pytest --cov=src --cov-report=html
```

## 🔒 Security Features

- **Input Sanitization**: All string inputs are sanitized to prevent injection attacks
- **Type Validation**: Strict type checking for all inputs
- **Environment Variable Validation**: Safe handling of environment variables
- **Error Handling**: Proper exception handling to prevent information leakage

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Keep functions small and focused

### Testing
- Write tests for all new features
- Maintain test coverage above 80%
- Test both success and failure cases
- Use descriptive test names

### Error Handling
- Always handle potential exceptions
- Log errors appropriately
- Provide meaningful error messages
- Fail gracefully

## 🐛 Code Review Findings

See [CODE_REVIEW.md](CODE_REVIEW.md) for detailed code review findings and recommendations.

### Fixed Issues:
- ✅ **Critical Syntax Error**: Fixed invalid Python syntax in main.py
- ✅ **Missing Modularity**: Implemented proper modular structure
- ✅ **No Error Handling**: Added comprehensive error handling
- ✅ **Missing Dependencies**: Added requirements.txt and pyproject.toml
- ✅ **No Testing**: Implemented pytest-based testing framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **JohannesFalk99** - *Initial work* - [JohannesFalk99](https://github.com/JohannesFalk99)

## 🙏 Acknowledgments

- Thanks to Nackademin for the project requirements
- Code review and security best practices implementation
