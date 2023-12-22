import concurrent.futures
import requests, time
# import logging
from tools.logger_config import configure_logger                        # Production Env, python runs in "yolov5" whereas "tools" is under "yolov5" parent folder
# from logger_config import configure_logger                              # Local Dev Environment for standalone unit testing
from datetime import datetime
import sys, time, win32evtlog, win32evtlogutil


### TRIGGER ALARM
class Alarm:   
    Bay1="http://192.168.1.221/26/"
    Bay2="http://192.168.1.222/26/"
    ForkLift1="http://192.168.1.223/26/"
    ForkLift2="http://192.168.1.224/26/"
    DEV_Bay="http://192.168.0.225/26/"
    DEV_ForkLift="http://192.168.0.226/26/"
    ON="on"
    OFF="off"

    def __init__(self):  
        self.logfile=logFile()
        self.logfile.logsys("10")                                            # detect-cam.py started
    
    def __del__(self):
        self.logfile.logsys("20")                                            # detect-cam.py ended
        del self.logfile

    def trigger_alarm(self,ip):
        self.alarm(ip + self.ON)
        self.alarm(ip + self.OFF)

    def alarm(self,ip_action):
        try:
            self.logfile.log(f"Sending request to {ip_action}")
            response = requests.get(ip_action, verify=False, timeout=9)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            time.sleep(3)
        except requests.exceptions.ConnectTimeout:
            self.logfile.log(f"Connection to IP {ip_action} timed out. Check network connectivity.")

        except requests.exceptions.ConnectionError:
            self.logfile.log(f"Failed to connect to IP {ip_action}. Verify the IP address and network status.")

        except requests.exceptions.HTTPError as err:
            if err.response is not None:
                self.logfile.log(f"HTTP error occurred: {err.response.status_code} {err.response.reason}")
            else:
                self.logfile.log(f"HTTP error occurred: {err}")


        except requests.exceptions.RequestException as e:
            self.logfile.log(f"An unexpected error occurred: {e}")
        except Exception as e:
            self.logfile.log(f"An error occurred: {e}")

    def setoff_alarm(self,ip):
    # threading.Thread(target = trigger_alarm, args = (DEV_Bay,)).start()
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            future = executor.submit(trigger_alarm, DEV_Bay)
            try:
                future.result()  # Wait for task completion
            except Exception as e:
                print(f"Error in alarm task: {e}")  # Handle exception in the main thread

                try:
                    future.cancel()  # Attempt to cancel the task if it's still running
                except Exception as cancel_error:
                    print(f"Error canceling task: {cancel_error}")  # Handle potential cancellation errors


### LOGGING
### do not change as this has to synchronize with CREATE project
class logFile:

    def __init__(self):
        self.logger = configure_logger(logger_type="logfile")  # Create a single logger for general logging
        self.wa_logger = configure_logger(logger_type="whatsapp")  # Separate logger for warnings

    def log(self, msg):
        try:
            printable_msg = msg
            print(msg)
        except UnicodeEncodeError:
            encoded_msg = msg.encode('utf-8', 'replace').decode('utf-8', 'replace')
            print(encoded_msg)
            printable_msg = ''.join(c if c.isprintable() else f'\\x{ord(c):02x}' for c in msg)
        self.logger.info(printable_msg)  # Use self.logger for general logging

    def logsys(self, event_code):
        try:
            # Validate event_code
            if not isinstance(event_code, str) or not event_code.isdigit(): 
                raise ValueError("event_code must be a number in string format ('01','02'...,'12')")

            event_dict = {
                "00": "Remote_Alarm.Fire WA Alert",
                "01": "Remote_Alarm.Bay 1 Alarm",
                "02": "Remote_Alarm.Bay 2 Alarm",
                "03": "Remote_Alarm.Forklift1 Alarm",
                "04": "Remote_Alarm.Forklift2 Alarm",
                "05": "Remote_Alarm.Unsafe handling of moving metal",
                "06": "Remote_Alarm.Stacking Height Exceeded",
                "10": "Detect-Cam.py.System Start",
                "11": "Remote_Alarm.System Test",
                "12": "Remote_Alarm.System Check",
                "20": "Detect-Cam.py.System End"
            }

            EVT_APP_NAME = event_dict.get(event_code, "Unknown Event")

            if EVT_APP_NAME == "Unknown Event":
                raise ValueError(f"Unknown event code: {event_code}")

            EVT_ID = 7777  # Got this from another event
            EVT_CATEG = int(event_code) # 0001-start #0010 = end
            EVT_STRS = [EVT_APP_NAME + " at " + datetime.now().strftime("%d/%b/%Y %H:%M:%S")]
            EVT_DATA = b"Aison EyeFire IoT Panel Event Data"

            win32evtlogutil.ReportEvent(\
                EVT_APP_NAME, EVT_ID, eventCategory=EVT_CATEG,\
                eventType=win32evtlog.EVENTLOG_INFORMATION_TYPE, strings=EVT_STRS,\
                data=EVT_DATA)

            self.log(EVT_APP_NAME)

        except ValueError as e:
            # print(f"Invalid event_code: {e}")
            self.log(f"Invalid event_code: {e}")

        except Exception as e:
            # print(f"An error occurred: {e}")
            self.log(f"An error occurred: {e}")       
    

### CLI TESTING
def main():
    # logfile = logFile()
    # logfile.log("this is a test")
    # logfile.logsys("12")
    # logfile.logsys("13")

    # dd/mm/YY H:M:S
    # now=datetime.now()
    # dt_string = "app started: " + now.strftime("%d/%m/%Y %H:%M:%S")
    # logfile.log("this is good")
    # logfile.logger.info("app_start")
    
    alarm = Alarm()
    alarm.trigger_alarm(alarm.Bay1)
    # alarm.setoff_alarm(DEV_Bay)
    # logfile.log("app ended" + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


if __name__ == '__main__':
    main()