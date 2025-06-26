# app.py
from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import tempfile
import os
app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    mode = data.get("mode", "audio")  # "audio" or "video"

    if not url:
        return {"error": "URLがありません"}, 400

    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "%(title)s.%(ext)s")

    ydl_opts = {
        'outtmpl': filepath,
        'quiet': True,
    }

    if mode == "audio":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
        })
    else:
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            ext = 'm4a' if mode == "audio" else info['ext']
            filename = ydl.prepare_filename(info).replace("%(ext)s", ext)

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

