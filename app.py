from flask import Flask, render_template, request
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template("index.html", error="Please provide a video URL.")

        video_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
        
        ydl_opts = {
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return render_template("index.html", download_link=f"/{filename}")
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Sign in to confirm" in error_msg:
                return render_template("index.html", error="This video requires login and can't be downloaded.")
            elif "Too Many Requests" in error_msg:
                return render_template("index.html", error="YouTube is rate-limiting the server. Please try again later.")
            elif "not made this video available in your country" in error_msg:
                return render_template("index.html", error="This video is not available in your region.")
            else:
                return render_template("index.html", error="Failed to download video. It might be restricted or private.")

    return render_template("index.html")
