from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        try:
            # Create a unique temp filename
            filename = f"{uuid.uuid4()}.mp4"
            filepath = f"/tmp/{filename}"  # Safe on Render

            ydl_opts = {
                'format': 'best',
                'outtmpl': filepath
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # Serve file to user
            return send_file(filepath, as_attachment=True)

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('index.html')
