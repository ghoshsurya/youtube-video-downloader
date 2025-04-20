from flask import Flask, request, render_template, send_file
import os
import yt_dlp
import glob

app = Flask(__name__)
DOWNLOAD_DIR = "downloads/videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video_no_ffmpeg(youtube_url):
    ydl_opts = {
        'format': 'best[ext=mp4][height>=144]',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title).100s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['video_url']
        try:
            download_video_no_ffmpeg(url)
            list_of_files = glob.glob(f'{DOWNLOAD_DIR}/*')
            latest_file = max(list_of_files, key=os.path.getctime)
            return send_file(latest_file, as_attachment=True)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
