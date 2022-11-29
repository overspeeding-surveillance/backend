from flask import Flask, Response, render_template, request, send_from_directory, jsonify
from custom_utils.generate import generate
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files['video']
    filename = secure_filename(str(uuid.uuid4()) + f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"filename": filename})


# @app.route("/static_files/<path:path>")
# def static_files(path):
#     return send_from_directory("uploads", path)


@app.route("/video_feed")
def video_feed():
    filename = request.args['filename']
    if not filename:
        return "no filename in query-parameters"
    if not os.path.exists('uploads/' + filename):
        return "invalid filename"
    return Response(generate('uploads/' + filename), mimetype="multipart/x-mixed-replace; boundary=frame")
