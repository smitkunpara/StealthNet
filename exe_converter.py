import subprocess

# run exerunner.exe file without any data
# subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\exerunner.py"])

# run bakara.exe file without any data
# subprocess.call(["pyinstaller","--onefile","--noconsole","Browser.py"])
subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\Browser.py"])
# subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\bakara.py"])