import websockets
import pygame
import asyncio
import json
import time
import os
import tempfile
import base64

# Initialize the pygame mixer for audio operations.
pygame.mixer.init()

# Get the event loop for the current context.
loop = asyncio.get_event_loop()

def play_audio(audio_file_path):
    """
    Load and play an audio file using pygame.

    Parameters:
        audio_file_path (str): The file system path to the audio file.
    """
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

async def unload_audio():
    """
    Asynchronously monitors and unloads the audio track once it finishes playing.
    Continuously checks every second to see if the audio is still playing.
    """
    while True:
        await asyncio.sleep(1)
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.unload()
                print("Audio unloaded")
                break
            except Exception as e:
                print(f"Error unloading audio: {e}")
                break

async def receive_file(fileName, fileData):
    """
    Receives a base64 encoded file, decodes it, and writes it to the file system.

    Parameters:
        fileName (str): The name of the file to save.
        fileData (str): Base64 encoded data of the file.
    """
    if os.path.exists(fileName):
        os.remove(fileName)
    with open(fileName, "wb") as file:
        file.write(base64.b64decode(fileData))
        print(f"File received: {fileName}")

def handle_audio_command(content_obj):
    """
    Handles the command to play audio if specified in the message object.

    Parameters:
        content_obj (dict): A JSON object containing potential audio commands.
    """
    if "play_audio" in content_obj:
        try:
            audio_FileName = sanitize_filename(content_obj["play_audio"])
            print(f"Received audio file: {audio_FileName}")
            audio_path = os.path.join(os.curdir, audio_FileName)
            if os.path.exists(audio_path):
                play_audio(audio_path)
                print(f"Playing audio: {audio_path}")
        except ValueError as e:
            print(f"Error: {e}")

def get_rotating_filename(base_path, base_name, extension, limit=10):
    """
    Generates a rotating filename within a specified limit to avoid file overwrites.

    Parameters:
        base_path (str): The directory path where the file will be saved.
        base_name (str): The base name for the file.
        extension (str): The file extension.
        limit (int): The maximum number of files before the index resets.
    
    Returns:
        str: The full path to the file with the generated name.
    """
    index_file_path = os.path.join(base_path, f"{base_name}_index.txt")
    
    if os.path.exists(index_file_path):
        with open(index_file_path, 'r') as file:
            last_index = int(file.read().strip())
    else:
        last_index = 0

    next_index = (last_index % limit) + 1

    with open(index_file_path, 'w') as file:
        file.write(str(next_index))

    filename = f"{base_name}_{next_index}.{extension}"
    return os.path.join(base_path, filename)

def sanitize_filename(filename):
    """
    Sanitizes the filename, removing unsafe characters and enforcing restrictions on length and file extensions.

    Parameters:
        filename (str): The filename to sanitize.

    Returns:
        str: The sanitized filename if valid, raises ValueError otherwise.

    Raises:
        ValueError: If the filename contains unauthorized extensions or exceeds length constraints.
    """
    allowed_extensions = {'.mp3', '.wav'}
    
    filename = filename.strip()
    filename = filename.replace('/', '').replace('\\', '').replace('\0', '')
    filename = os.path.basename(filename)
    
    root, ext = os.path.splitext(filename)
    if ext.lower() not in allowed_extensions:
        raise ValueError(f"Unauthorized file extension: {ext}")
    
    max_length = 50
    if len(filename) > max_length:
        raise ValueError(f"Filename too long. Max length is {max_length} characters.")
    
    return filename

async def handler():
    """
    Main handler function for WebSocket communication and processing received commands.

    Establishes a WebSocket connection to the specified URI and listens for incoming messages,
    handling audio playback and file transfer operations based on the content of the messages.
    """
    uri = "ws://localhost:3000"
    async with websockets.connect(uri, max_size=20000000) as websocket:
        await websocket.send("{\"request\": \"message from raspberry audio client\"}")
        done = False
        while not done:
            time.sleep(10/1000)
            message = await websocket.recv()
            print(message)
            if isinstance(message, str):
                try:  
                    parsed_message = json.loads(message)
                    if "play_audio" in parsed_message:
                        handle_audio_command(parsed_message)
                        asyncio.create_task(unload_audio())
                    elif "operation" in parsed_message and parsed_message["operation"] == "file_transfer":
                        file_name = get_rotating_filename(os.curdir, "audioFile", "mp3")
                        await receive_file(file_name, parsed_message["file"])
                        play_audio(file_name)
                        asyncio.create_task(unload_audio())
                    elif "stop_audio" in parsed_message:
                        pygame.mixer.music.stop()
                        print("Audio stopped")
                except ValueError:
                    print("Could not parse message")
                    continue

asyncio.run(handler())