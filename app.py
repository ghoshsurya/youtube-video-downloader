from flask import Flask, render_template, request, send_file
import os
import yt_dlp
from pathlib import Path

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads/videos"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video_no_ffmpeg(youtube_url):
    ydl_opts = {
        'format': 'best[ext=mp4][height>=144]',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title).100s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_title = ydl.prepare_filename(info_dict)
    return video_title

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    try:
        file_path = download_video_no_ffmpeg(video_url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"<h3>Error downloading video: {str(e)}</h3>"

if __name__ == '__main__':
    app.run(debug=True)
