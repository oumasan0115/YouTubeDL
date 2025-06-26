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

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return {"error": "URL is required"}, 400

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tempfile.gettempdir() + "/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
