from flask import Flask, render_template, request, send_file, redirect, url_for
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
            return render_template('index.html', error="Please enter a video URL.")

        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            return render_template('index.html', error=f"Download failed: {str(e)}")

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
