#!/usr/bin/env python3
"""
Code validation script to check for syntax errors and basic issues.
"""

import ast
import os
import sys
from typing import List, Tuple


def validate_python_file(filepath: str) -> Tuple[bool, str]:
    """
    Validate a Python file for syntax errors.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file is empty or only comments
        if not content.strip() or all(line.strip().startswith('#') or not line.strip() 
                                     for line in content.split('\n')):
            return False, "File is empty or contains only comments"
        
        # Parse the AST to check syntax
        ast.parse(content)
        return True, "OK"
        
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def find_python_files(directory: str) -> List[str]:
    """Find all Python files in directory."""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    return python_files


def main():
    """Main validation function."""
    print("🔍 Code Validation Report")
    print("=" * 50)
    
    current_dir = os.getcwd()
    python_files = find_python_files(current_dir)
    
    if not python_files:
        print("❌ No Python files found!")
        return 1
    
    total_files = len(python_files)
    valid_files = 0
    issues = []
    
    for filepath in python_files:
        relative_path = os.path.relpath(filepath, current_dir)
        is_valid, message = validate_python_file(filepath)
        
        if is_valid:
            print(f"✅ {relative_path}: {message}")
            valid_files += 1
        else:
            print(f"❌ {relative_path}: {message}")
            issues.append((relative_path, message))
    
    print("\n" + "=" * 50)
    print(f"📊 Summary: {valid_files}/{total_files} files valid")
    
    if issues:
        print(f"\n🚨 Issues found in {len(issues)} files:")
        for filepath, message in issues:
            print(f"  - {filepath}: {message}")
        return 1
    else:
        print("🎉 All Python files are syntactically correct!")
        return 0


if __name__ == "__main__":
    sys.exit(main())