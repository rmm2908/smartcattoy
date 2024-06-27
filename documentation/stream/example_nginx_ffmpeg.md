# Example setup for streaming web server
This example setup will provide the necessary configuration for a simple web server serving m3u8 video files using [nginx](https://nginx.org/en/).<br>
These instrunctions were last tested on a debian machine. Depending on which operating system you are using, some steps may vary.
## Setting up the web server
First, we will set up a nginx instance with which we will serve the video stream.<br>
### Install nginx
<b>Install nginx using apt</b><br>
``` sudo apt install nginx ```<br>
### Setup site
Once nginx is instaslled, only some basic configuration is necessary for a minimal nginx setup to provide a HLS stream. The configuration for nginx is located under "/etc/nginx". To serve the stream, we will create a new site under "/etc/nginx/sites-available/stream.config" using the following configuration:
```
server {
	listen 80 default_server;
	listen [::]:80 default_server;

	root /var/www/stream;

	index index.html index.htm index.nginx-debian.html;

	server_name _;

	location / {
		# CORS
		add_header 'Access-Control-Allow-Origin' '*' always;
		add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
		add_header 'Access-Control-Allow-Headers' 'Range';

		types {
			application/vnd.apple.mpegurl m3u8;
			video/mp2t ts;
		}
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ =404;
		autoindex on;
	}
}
```
This configuration will a site on port 80 using the directory "/var/www/stream". In this directory, the video file for the stream should be placed.<br>
Different types for the video can be defined - by default, SmartCatToy uses m3u8.<br>
### Enable the site
To enable the site we just configured, we need to create a symbolic link to sites-enabled:
``` sudo ln -s /etc/nginx/sites-available/stream.conf /etc/nginx/sites-enabled/stream.conf ```<br>
After creating the link, nginx needs to be reloaded:<br>
``` sudo systemctl reload nginx ```
## Provide video resource for streaming
To provide a file that can be streamed via HLS from a camera installed on the toy, the toy needs to send a video stream to the server. For example, this could be achieved using [ffmpeg](https://ffmpeg.org/).
### Stream camera feed from toy to server
Using ffmpeg, the footage from an installed camera can be sent to the server. A [python script](../../raspberry/camera_client.py) running on the toy will send the camera footage to the server on port 8001 using UDP.
### Convert incoming stream to video file
On the server, we need to listen on this port and convert the incoming stream to a video file in the m3u8 format, so that it can be served using the nginx site we created.<br>
#### ffmpeg command to convert UDP stream to m3u8
This command will listen on the UDP port 8001 and convert the stream to a m3u8 and split the incoming frames into segments (.ts files):<br>
``` sudo ffmpeg -y -i udp://localhost:8001 -preset ultrafast -tune zerolatency -omit_video_pes_length 0 -g 90 -flags -global_header -fflags nobuffer -flags low_delay /var/www/stream/bucket/stream.m3u8 ```<br>
This command uses various parameters and presets to try to reduce the streaming delay caused by HLS streaming. Once the server starts to receive UDP packets on the specified port, ffmpeg will create a stream.m3u8 file and segment the incoming video feed into small .ts-files.
## Resulting HLS streaming resource
If the above instrunctions were all carried out, a video file will be created from the incoming camera feed and can be queried using HLS. If the exact configurations and folder structures were used, it will be available under ``` http://<server-address>/bucket/stream.m3u8 ```