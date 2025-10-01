import os
import sys
import subprocess
import time

def setup_database():
    if not os.path.exists('test.db'):
        subprocess.run([sys.executable, 'create_sample_database.py', '--reset'], check=True)
    return True

def launch_web_app():
    web_app_path = os.path.join('web_interface', 'flask_server.py')
    if not os.path.exists(web_app_path):
        return False
    
    process = subprocess.Popen([sys.executable, web_app_path], cwd=os.getcwd())
    time.sleep(2)
    print("School Lunch System: http://127.0.0.1:5000")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
    return True

def main():
    setup_database()
    launch_web_app()

if __name__ == "__main__":
    main()
