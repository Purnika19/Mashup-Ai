# Mashup AI – YouTube Audio Mashup Generator
### Overview

Mashup AI is a Flask-based web application that allows users to generate a custom MP3 mashup from YouTube songs of a specified singer.

### The system:

🔷 Searches YouTube for N songs of a singer

🔷 Downloads the audio

🔷 Cuts the first Y seconds from each track

🔷 Merges them into a single MP3

🔷 Compresses the file into a ZIP

🔷 Sends it to the user via email


### Features

🔷 Search and download N songs of a singer using yt-dlp

🔷 Cut the first Y seconds from each track

🔷 Merge all audio segments into one MP3 file

🔷 Generate downloadable ZIP archive

🔷 Email delivery using SMTP (Gmail App Password supported)

🔷 Modern animated frontend using Tailwind CSS

🔷 Flask backend with Gunicorn deployment support


### Technologies Used

🔷 Python 3.11

🔷 Flask

🔷 Gunicorn

🔷 yt-dlp

🔷 pydub

🔷 FFmpeg

🔷 Tailwind CSS

🔷 Render (Deployment)




### Deployment (Render)

🔷 Push code to GitHub

🔷 Create Web Service on Render

🔷 Build Command: pip install -r requirements.txt

🔷 Start Command: gunicorn app:app

🔷 Add environment variables

🔷 Ensure .python-version contains 3.11.9


### Important Notes

🔷 Python 3.11 is required

🔷 FFmpeg must be installed

🔷 yt-dlp may face rate limits from YouTube

🔷 Gmail App Password is required for email sending


### Author

Purnika Malhotra

Roll No: 102303412
