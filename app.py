from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "YouTubeDL API is running!"

@app.route("/download", methods=["GET"])
def download_audio():
    url = request.args.get("url")
    if not url:
        return "URL is required", 400

    # YouTubeから音声を抽出
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "output.%(ext)s",
        "cookiefile": "cookies.txt",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
