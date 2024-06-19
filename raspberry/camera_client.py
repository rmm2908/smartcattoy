import asyncio
import subprocess

camera_name = 'DroidCam Source 3'

async def handler():
    done = False
    while not done:
        record_cmd = ['ffmpeg', '-f', 'dshow', '-i' , 'video=' + camera_name, '-preset', 'ultrafast', '-tune', 'zerolatency', '-f', 'mpegts', '-s', '854x480', '-omit_video_pes_length', '0', 'udp://192.168.178.90:8001']
        subprocess.run(record_cmd)
        done = True

asyncio.run(handler())