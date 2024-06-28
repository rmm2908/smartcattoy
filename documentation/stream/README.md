# Stream
The SmartCatToy app provides the possibility of live streaming a camera feed from the toy.  It does this by querying a web server to stream a video using HLS (HTTP-Livestreaming). Therefore, a web server providing such a stream is needed for this feature to work.
## Requirements
* ### Web server
    A web server is needed to provide the video resource for the stream.
It is important that the video file can be accessed directly via URL (also consider CORS).
* ### Video ressource for streaming
    A video file in the correct format (default: m3u8) can be served through the web server to the app. SmartCatToy does this by sending the camera feed to the server using UDP. The server then converts the incoming UDP stream to the required video format.
### Example using nginx and ffmpeg
Instructions for setting up such a environment can be found [here](example_nginx_ffmpeg.md).