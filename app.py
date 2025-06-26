from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp
import os
import tempfile
import shutil

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

    temp_dir = tempfile.mkdtemp()

    try:
        # タイトル取得（事前情報取得）
        with yt_dlp.YoutubeDL({"cookiefile": "cookies.txt", "quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "downloaded").replace("/", "_").replace("\\", "_")

        if type_ == "audio":
            output_path = os.path.join(temp_dir, f"{title}.%(ext)s")
            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": output_path,
                "cookiefile": "cookies.txt",
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            }
            target_file = os.path.join(temp_dir, f"{title}.mp3")

        else:  # type == video
            output_path = os.path.join(temp_dir, f"{title}.%(ext)s")
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": output_path,
                "cookiefile": "cookies.txt",
                "quiet": True,
                "merge_output_format": "mp4",  # これが重要
            }
            target_file = os.path.join(temp_dir, f"{title}.mp4")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(target_file, as_attachment=True)

    except Exception as e:
        return str(e), 500

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
