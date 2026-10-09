from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)

# Configure CORS to allow Private Network Access
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "ngrok-skip-browser-warning"]
}})

STORAGE_PATH = "/sdcard"

ALLOWED_COMMANDS = {
    "mkdir_footer": ["mkdir", "-p", os.path.join(STORAGE_PATH, "footer")],
    "shutdown": ["su", "-c", "reboot -p"],
    "open_notepad": ["notepad.exe"],
}


@app.route("/run", methods=["POST", "OPTIONS"])
def execute_command():
    # 1. Handle Preflight OPTIONS request cleanly
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, ngrok-skip-browser-warning"
        # CRITICAL: Permits public HTTPS websites to call local network IPs
        response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response, 200

    # 2. Safe JSON retrieval (silent=True prevents 400 bad request errors if body is unexpected)
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    if action not in ALLOWED_COMMANDS:
        return jsonify({"status": "error", "message": "Unauthorized action"}), 400

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[action],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=10
        )

        res = jsonify({
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr
        })
        res.headers["Access-Control-Allow-Origin"] = "*"
        res.headers["Access-Control-Allow-Private-Network"] = "true"
        return res, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)