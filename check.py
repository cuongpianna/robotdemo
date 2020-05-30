import subprocess
import requests
import urllib
import os


def check_connection():
    bash_command = "/usr/bin/google-chrome-stable http://localhost:5000"
    try:
        a = urllib.request.urlopen("http://www.stackoverfozzzs.com").getcode()
        if a == 404:
            output = os.system(bash_command)
    except:
        output = os.system(bash_command)
    # if(requests.head('http://nguyenvanhieu.com/').status_code != 200):
    #     output = subprocess.check_output(['bash', '-c', bash_command])


if __name__ == '__main__':
    check_connection()
