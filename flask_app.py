from flask import Flask, jsonify, request
from flask_cors import CORS


from getdata import get_url

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'PyTubeBot -> <a href="https://t.me/ytubepy_bot" style="color: red; decoration: none;">more info</a>'

@app.route("/getimage", methods=["POST"])
def get_image():
    data = request.get_json()
    
    if not data or "url" not in data or "type" not in data:
        return jsonify({'error': 'Invalid input.'}), 400
    
    url = data["url"]
    data_type = data["type"]
    
    if not url.strip() or not data_type.strip():
        return jsonify({'error': 'Please enter valid data.'}), 400
    if data_type not in ["playlist", "video"]:
        return jsonify({'error': 'Please enter valid content type.'}), 400
    try:
        result = get_url(url, data_type)
        return jsonify({"image": result}), 200
    except Exception:
        return jsonify({'error': 'Content not found.'}), 400
if __name__ == '__main__':
    app.run(debug=False)
