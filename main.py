from flask import Flask, request, jsonify
import io
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    html = ""
    with open("index.html", "r") as f:
        html = f.read()
    return html















# @app.route("/api/read", methods=["POST"])
# def receiveDataRead():
#     data = datatoimage.imageToData(request.json["image-data"])
#     outstring = ""
#     for i in data:
#         outstring += data[i]+"$"
#     return outstring





# @app.route("/create", methods=["GET"])
# def create():
#     html = ""
#     with open("create.html", "r") as f:
#         html = f.read()
#     return html


# @app.route("/image", methods=["POST"])
# def returnImage():
#     return render_template('image.html', imagedata = request.form["image-data"])


# @app.route("/image/download", methods=["POST"])
# def DownloadLogFile():
#     try:
#         tempFile = io.BytesIO(base64.b64decode(request.form["image-data"]));
#         return send_file(, as_attachment=True)
#     except Exception as e:
#         self.log.exception(e)
#         self.Error(400)