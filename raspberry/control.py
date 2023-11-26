import socket
import time
import json
import threading
import serial
import sys
import logging

#Serial Connection to Arduino
#ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.05)
#ser.reset_input_buffer()

#HTTP Port Connection to Start the WebServer on Port 9988
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9988))
s.listen(1)

#while True:
    #ser.write(str("forward\n").encode("utf-8"))
    #if ser.in_waiting > 0:
    #    print(ser.readline())
    #time.sleep(3)
    #ser.write(str("stop\n").encode("utf-8"))
    #time.sleep(3)

def action(binaryData):
    decodedData = binaryData.decode("UTF-8")
    print(decodedData)
    #if "{" in decodedData:
      #positionOfContent = decodedData.index("{")
      #jsonContent = decodedData[positionOfContent:]
      #content_obj = json.loads(jsonContent)
      #if findCommandInString(decodedData):
          #serialCommand = createMotorString(content_obj)
          #print("SerialCommand: " + serialCommand)
        #ser.write(str.encode(serialCommand))

try:
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        response = r'''HTTP/1.0 200 OK
Access-Control-Allow-Origin:  http://localhost:9988
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Content-Type, Authorization
'''
        conn.sendall(response.encode('UTF-8'))
        conn.close()
        action(data)
except Exception as e:
   logging.error('Error at %s', 'division', exc_info=e)
   s.close()
finally:
    s.close()