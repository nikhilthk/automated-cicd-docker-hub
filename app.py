import os
import platform
import socket
import time

from flask import Flask, jsonify, render_template

app = Flask(__name__)
START_TIME = time.time()


def format_uptime(seconds):
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours}h {minutes}m {secs}s"


def get_info():
    uptime_seconds = time.time() - START_TIME
    return {
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "commit": os.getenv("GIT_SHA", "local")[:7],
        "built_at": os.getenv("BUILD_TIME", "not built by pipeline"),
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "uptime_seconds": int(uptime_seconds),
        "uptime": format_uptime(uptime_seconds),
    }


@app.route("/")
def home():
    return render_template("index.html", info=get_info())


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/info")
def api_info():
    return jsonify(get_info())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)