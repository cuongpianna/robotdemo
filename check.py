import subprocess
import requests

def check_connection():
    bash_command = "/usr/bin/google-chrome-stable http://localhost:5000"
    if(requests.get('https://nguyenvanhieuu.com/').status_code != 200):
        output = subprocess.check_output(['bash', '-c', bash_command])


if __name__ == '__main__':
    check_connection()