import subprocess
import getpass
import time

user = getpass.getuser()
get = lambda x: subprocess.check_output(["/bin/bash", "-c", x]).decode("utf-8")
ws1 = get("wmctrl -lp"); t = 0
subprocess.call(["/bin/bash", "-c", "chromium-browser&"])
while t < 30:
    ws2 = [w.split()[2] for w in get("wmctrl -lp").splitlines() if not w in ws1]
    procs = [[p for p in get("ps -u "+user).splitlines() \
              if "chromium-bro" in p and w in p] for w in ws2]
    if len(procs) > 0:
        command = "xdotool type 'chrome://inspect'&&xdotool key Return"
        subprocess.call(["/bin/bash", "-c", command])
        break
    time.sleep(0.5)
    t = t+1