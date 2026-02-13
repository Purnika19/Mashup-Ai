import sys
import os
import shutil
import logging
import uuid
from yt_dlp import YoutubeDL
from pydub import AudioSegment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Mashup:
    def __init__(self, singer_name, num_videos, duration, output_file):
        self.singer_name = singer_name
        self.num_videos = int(num_videos)
        self.duration = int(duration)
        self.output_file = output_file

        if not self.output_file.endswith('.mp3'):
            self.output_file += '.mp3'

        # Unique folder every run (prevents Windows locking issue)
        self.download_dir = f"mashup_downloads_{uuid.uuid4().hex}"

        self._configure_ffmpeg()

    def _configure_ffmpeg(self):
        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")

        if not ffmpeg_path:
            raise RuntimeError("FFmpeg is not installed or not in PATH.")

        AudioSegment.converter = ffmpeg_path
        if ffprobe_path:
            AudioSegment.ffprobe = ffprobe_path

        logger.info(f"FFmpeg found at: {ffmpeg_path}")

    def validate_inputs(self):
        if self.num_videos <= 10:
            raise ValueError("Number of videos (N) must be greater than 10.")
        if self.duration <= 20:
            raise ValueError("Duration (Y) must be greater than 20 seconds.")

    def download_videos(self):
        os.makedirs(self.download_dir, exist_ok=True)

        logger.info(f"Downloading {self.num_videos} songs of {self.singer_name}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'ignoreerrors': True,

            # ✅ FIXED JS runtime config
            'js_runtimes': {
                'node': {
                    'path': r'C:\Program Files\nodejs\node.exe'
                }
            },

            # ✅ Enable remote challenge solver
            'remote_components': ['ejs:github'],

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        query = f"ytsearch{self.num_videos}:{self.singer_name} songs"

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])

        files = [
            os.path.join(self.download_dir, f)
            for f in os.listdir(self.download_dir)
            if f.endswith('.mp3')
        ]

        if len(files) == 0:
            raise RuntimeError("No videos downloaded. Check internet or singer name.")

        if len(files) < self.num_videos:
            logger.warning("Downloaded fewer videos than requested.")

        return files

    def process_audio(self, files):
        logger.info(f"Cutting first {self.duration} seconds from each audio...")

        combined_audio = AudioSegment.empty()
        extract_duration = self.duration * 1000

        for file_path in files:
            try:
                audio = AudioSegment.from_mp3(file_path)

                if len(audio) > extract_duration:
                    combined_audio += audio[:extract_duration]
                else:
                    combined_audio += audio

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")

        return combined_audio

    def run(self):
        self.validate_inputs()

        files = self.download_videos()
        final_audio = self.process_audio(files)

        logger.info("Exporting final mashup...")
        final_audio.export(self.output_file, format="mp3")

        logger.info(f"Mashup created successfully: {self.output_file}")


def main():
    if len(sys.argv) != 5:
        print("Usage: python 102303412.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        print("Example: python 102303412.py \"Sharry Maan\" 20 30 output.mp3")
        sys.exit(1)

    singer_name = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    try:
        mashup = Mashup(singer_name, num_videos, duration, output_file)
        mashup.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


