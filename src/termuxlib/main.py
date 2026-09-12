import subprocess
import json
import random

class notification:
    def send(title:str,content:str,priority:str or "min",id:str or f"{random.randint(1,9999)}" ):
       testing_sending_sucess = subprocess.run([
        "termux-notification",
        "-t",title,
        "-c",content,
        "-p",priority,
        "--id",id

       ],check=True).returncode
        if testing_sending_sucess == 0:
            return 0
        else:
            return 1

    def remove(id:str):
        process = subprocess.run(["termux-notification-remove",id])
        return process.returncode 


class device:
  def battery_status():
      process = subprocess run("termux-battery-status",capture_output=True)
      returncode = process.returncode
      if returncode == 0:
          return json.load(process.stdout.decode())
      
      return returncode 

  def location_gps():
      process = subprocess.run("termux-location -p gps",capture_output=True)
      returncode = process.returncode

      if returncode == 0:
            gps_formatted = json.load(process.stdout.decode())
            return returncode,gps_formatted 

      return returncode

  def sensor_list():
      process = subprocess.run("termux-sensor -l",capture_output=True)
      returncode = process.returncode
      if returncode == 0:
            return json.load(process.stdout.decode())

      return returncode

  def sensor_read(target:str):
      process = subprocess.run(["termux-sensor","-s",target,"-n 1""],capture_output=True)
      returncode = process.returncode
      if returncode == 0:
            sensor_info_formatted = json.load(process.stdout.decode())
            return returncode,sensor_info_formatted
      
        return returncode

  def get_fingerprint():
      process = subprocess.run("termux-fingerprint",capture_output=True)
      returncode = process.returncode

      if returncode == 0:
            formatted_fingerprint = json.load(process.stdout.decode())
            return returncode,formatted_fingerprint
      return returncode

class tts:
    def engine_list():
        process = subprocess.run("termux-tts-engines",capture_output=True)
        returncode = subprocess.returncode
        if returncode == 0:
            engines_tts_formatted = json.load(process.stdout.decode())
            return returncode,engines_tts_formatted
        else:
            return returncode

    def speak(text:str):
        process = subprocess.run(["termux-tts-speak",text])
        return process.statuscode

class sms:
    def contact_list():
        process = subprocess.run("termux-contact-list",capture_output=True)
        returncode = process.returncode 
        if returncode == 0:
            contact_list_formatted = json.load(process.stdout.decode)
            return returncode,contact_list_formatted
        
        return returncode


    def send(phone_number:str,msg:str):
        process = subprocess.run([
            "termux-sms-send","-n",
            phone_number,msg
        ])
        return subprocess.returncode

    def sms_list():
        process = subprocess.run("termux-sms-list",capture_output=True)
        returncode = subprocess.returncode
        if returncode == 0:
            smslist_formmated = json.load(process.stdout.decode())
            return returncode,smslist_formmated 
    
        return returncode 
    
class telephony:
    def info():
        process = subprocess.run("termux-telephony-deviceinfo",capture_output=True)
        returncode = process.returncode

        if returncode == 0:
            telephony_informations_formatted = json.load(process.stdout.decode())
            return returncode,telephony_informations_formatted 
        return returncode 

    def makecall(phone_number:str):
        process = subprocess.run(["termux-telephony-call",phone_number])
        return process.returncode 

class wifi:
    def info():
        process = subprocess.run("termux-wifi_connectioninfo",capture_output=True)
        returncode = process.returncode

        if returncode == 0:
            wifi_informations_formatted = json.load(process.stdout.decode())
            return returncode,wifi_informations_formatted 
        return returncode

    def scan_networks():
        process = subprocess.run("termux-wifi-scaninfo",capture_output=True)
        returncode = process.returncode 

        if returncode == 0:
            scanresult_informations_formatted = json.load(process.stdout.decode())
             return returncode,scanresult_informations_formatted
        return returncode

class clipboard:
    def copy(text:str):
        process = subprocess.run([
        "termux-clipboard-set",text
        ])
        return process.returncode

    def read_clipboard():
        process = subprocess.run("termux-clipboard-get",capture_output=True)
        clipboard_content_formattef = json.load(process.stdout.decode())
        returncode = process.returncode 
        return returncode,process

class camera:      
  def info():
     process = subprocess.run("termux-camera-info",capture_output=True)
     camera_informations_formatted = json.load(process.stdout.decode())
     returncode = process.returncode
     return returncode,process

  def take_photo(outputfile:str,camera:str):
     if camera == "front":
        process = subprocess.run([
          "termux-camera-photo",
          "-c",0,outputfile
        ])

     elif camera == "back":
        process = subprocess.run([
          "termux-camera-photo",
          "-c",1,outputfile
        ])

     return process.returncode 

  def torch(state:bool):
     if state == True:
        process = subprocess.run("termux-torch on")

     elif state == False:
        process = subprocess.run("termux-torch off")
    
    return process.returncode
