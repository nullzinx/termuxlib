import subprocess
import json

def send_notification(title:str,content:str):
    subprocess.run([
        "termux-notification",
        "-t",title,
        "-c",content

    ],check=True)


class device:
  def battery_status():
      return subprocess.run("termux-battery-status",shell=True,capture_output=True).stdout.decode()

  def location_gps():
      return subprocess.run("termux-location -p gps",shell=True,capture_output=True).stdout.decode()
  
  def sensor_list():
      return subprocess.run("termux-sensor -l",shell=True,capture_output=True).stdout.decode()
  
  def sensor_read(target:str):
      return subprocess.run([
        "termux-sensor",
        "-s",target,
        "-n 1"],shell=True,capture_output=True).stdout().decode()

  def get_fingerprint():
      return subprocess.run("termux-fingerprint",shell=True,captue_output=True).stdout.decode()


class tts:
    def engine_list():
        return subprocess.run("termux-tts-engines",shell=True,capture_output=True).stdout.decode()
    def speak(text:str):
        subprocess.run(["termux-tts-speak",text])


class sms:
    def contact_list():
        return subprocess.run("termux-contact-list",shell=True,capture_output=True).stdout.decode()
    def send(phone_number:str,msg:str):
        subprocess.run([
            "termux-sms-send","-n",
            phone_number,msg
        ])
    def sms_list():
        return subprocess.run("termux-sms-list",shell=True,capture_output=True).stdout.decode()


class telephony:
    def info():
        return subprocess.run("termux-telephony-deviceinfo",shell=True,capture_output=True).stdout.decode()
    def makecall(phone_number:str):
        subprocess.run([
            "termux-telephony-call",phone_number
        ])

class wifi:
    def info():
        return subprocess.run("termux-wifi-connectioninfo",shell=True,capture_output=True).stdout.decode()
    def scan_networks():
        return process.run("termux-wifi-scaninfo",shell=True,capture_output=True).stdout.decode()


class clipboard:
    def copy(text:str):
        subprocess.run([
        "termux-clipboard-set",text
        ])
    def read_clipboard():
        return subprocess.run("termux-clipboard-get",shell=True,capture_output=True).stdout.decode()
    

class camera:      
  def info():
     return subprocess.run("termux-camera-info",shell=True,capture_output=True).stdout.decode()

  def take_photo(outputfile:str,camera:str):
     if camera == "front":
        subprocess.run([
          "termux-camera-photo",
          "-c",0,outputfile
        ])
     elif camera == "back":
        subprocess.run([
          "termux-camera-photo",
          "-c",1,outputfile
        ])

  def torch(state:bool):
     if state == True:
        subprocess.run("termux-torch on",shell=True)
     elif state == False:
        subprocess.run("termux-torch off",shell=True)


if __name__ == "__main__":
  # camera.torch(True)
  send_notification("python","teste")
  print(device.battery_status())
  print(camera.info())
  print(sms.contact_list())
