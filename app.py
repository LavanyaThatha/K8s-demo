import os, socket, time
from flask import Flask, jsonify

app = Flask(__name__)
START = time.time()
hits = 0

def info():
    return {
        "pod": os.getenv("POD_NAME", socket.gethostname()),
        "pod_ip": os.getenv("POD_IP", "n/a"),
        "node": os.getenv("NODE_NAME", "n/a"),
        "namespace": os.getenv("NAMESPACE", "n/a"),
        "version": os.getenv("APP_VERSION", "v1"),
        "uptime_seconds": int(time.time() - START),
        "hits_on_this_pod": hits,
    }

@app.route("/")
def home():
    global hits
    hits += 1
    rows = "".join(f"<tr><td>{k}</td><td><b>{v}</b></td></tr>" for k, v in info().items())
    return (f"<html><head><meta http-equiv='refresh' content='2'></head>"
            f"<body style='font-family:sans-serif'><h1>Running on Kubernetes</h1>"
            f"<table cellpadding='6'>{rows}</table></body></html>")

@app.route("/info")
def api():
    global hits
    hits += 1
    return jsonify(info())

@app.route("/health")
def health():
    return "ok"

@app.route("/crash")
def crash():
    os._exit(1)   # kills the app on purpose so you can watch Kubernetes restart it

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)