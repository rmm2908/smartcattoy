import socket
import time
import json
import threading
import serial
import sys
import logging

#Serial Connection to Arduino
#ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.05)
#ser = serial.Serial('COM3', baudrate = 9600, timeout = 0.05)
#ser.reset_input_buffer()

#HTTP Port Connection to Start the WebServer on Port 9988
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9988))
s.listen(1)

def findCommandInString(text):
    if "motor1PW" in text:
        return True
    if "motor1D" in text:
        return True
    if "motor2PW" in text:
        return True
    if "motor2D" in text:
        return True


def createMotorString(content_obj):
 return str(content_obj["motor1PW"]) + "," + str(content_obj["motor1D"]) + "," + str(content_obj["motor2PW"]) + "," + str(content_obj["motor2D"]) + "," + "\n"


def action(binaryData):
    decodedData = binaryData.decode("UTF-8")
    print(decodedData)
    if "{" in decodedData:
      positionOfContent = decodedData.index("{")
      jsonContent = decodedData[positionOfContent:]
      content_obj = json.loads(jsonContent)
      if findCommandInString(decodedData):
          serialCommand = createMotorString(content_obj)
          print("SerialCommand: " + serialCommand)
          #ser.write(str(serialCommand).encode("UTF-8"))

try:
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        response = r'''HTTP/1.0 200 OK
Access-Control-Allow-Origin:  *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
Access-Control-Max-Age: 600
User-Agent: RaspbianOS/12
'''
        conn.send(response.encode('UTF-8'))
        conn.close()
        action(data)
except Exception as e:
   logging.error('Error at %s', 'division', exc_info=e)
   s.close()
finally:
    s.close()