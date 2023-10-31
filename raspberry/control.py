import serial
import time

ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 0.05)
ser.reset_input_buffer()



while True:
    ser.write(str("forward\n").encode("utf-8"))
    if ser.in_waiting > 0:
        print(ser.readline())
    time.sleep(3)
    ser.write(str("stop\n").encode("utf-8"))
    time.sleep(3)
