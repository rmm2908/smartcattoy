import asyncio
import websockets
import json
import serial


#Serial Connection to Arduino
#ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.05)
#ser = serial.Serial('COM3', baudrate = 9600, timeout = 0.05)
#ser.reset_input_buffer()

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

# create handler for each connection
async def handler():
    uri = "wss://hackathoncattoy.azurewebsites.net"
    async with websockets.connect(uri) as websocket:
        #await websocket.send("{\"request\": \"message from raspberry\"}")
        done = False
        while not done:
            message = await websocket.recv()
            print(message)
            if "{" in message:
                positionOfContent = message.index("{")
                jsonContent = message[positionOfContent:]
                content_obj = json.loads(jsonContent)
                print(jsonContent)
                if findCommandInString(message):
                    serialCommand = createMotorString(content_obj)
                    print("SerialCommand: " + serialCommand)
                    #ser.write(str(serialCommand).encode("UTF-8"))
asyncio.run(handler())
