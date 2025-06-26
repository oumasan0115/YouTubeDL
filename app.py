from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    type_ = request.args.get("type", "audio")

    if not url:
        return "URL is required", 400

    ydl_opts = {
        "format": "bestvideo+bestaudio/best" if type_ == "video" else "bestaudio",
        "outtmpl": "output.%(ext)s",
        "cookiefile": "cookies.txt",
    }

    if type_ == "audio":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if type_ == "audio":
            filename = filename.rsplit(".", 1)[0] + ".mp3"

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
