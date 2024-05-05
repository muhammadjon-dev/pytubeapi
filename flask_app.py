from flask import Flask, jsonify, request
from flask_cors import CORS


from getdata import get_url

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'PyTubeBot -> <a href="https://t.me/ytubepy_bot" style="color: red; decoration: none;">more info</a>'

@app.route("/getimage", methods=["POST"])
def spam_checker():
    data = request.get_json()
    
    if not data or "url" not in data or "type" not in data:
        return jsonify({'error': 'Invalid input.'}), 400
    
    url = data["url"]
    data_type = data["type"]
    
    if not url.strip():
        return jsonify({'error': 'Please enter valid url.'}), 400
    
    result = get_url(url)
    return jsonify({"image": result}), 200

if __name__ == '__main__':
    app.run(debug=False)
