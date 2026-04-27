from flask import Flask, render_template, request, jsonify
import hashlib

app = Flask(__name__)

# Trang chính
@app.route("/")
def home():
    return render_template("index.html")

# Trang Hash
@app.route("/hash")
def hash_page():
    return render_template("hash.html")

# API Hash
@app.route("/hash/compute", methods=["POST"])
def compute_hash():
    data = request.get_json()
    text = data.get("text", "")
    algorithm = data.get("algorithm", "")

    if text == "":
        return jsonify({"result": "Error: Empty input"})

    if algorithm == "md5":
        result = hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha256":
        result = hashlib.sha256(text.encode()).hexdigest()
    else:
        result = "Error: Invalid algorithm"

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)