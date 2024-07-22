import subprocess

# run exerunner.exe file without any data
# subprocess.call(["pyinstaller","--onefile","--noconsole","bakara.py"])



# run bakara.exe file without any data
# subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\Browser.py"])
# subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\Browser.py"])
# subprocess.call(["pyinstaller","--onefile","--noconsole","StealthNet\\bakara.py"])
subprocess.call(["pyinstaller","--onefile","--noconsole","bakara.py"])
# subprocess.call(["pyinstaller","--onefile","--noconsole","BackdoorExecutor.py"])