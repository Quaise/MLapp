from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from utils.process_video import process_video

app = Flask(__name__)
CORS(app)  # Allow frontend requests

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    # Process video (detection, save result in static/output.mp4)
    process_video(video_path)

    return jsonify({"message": "Processing complete", "video_url": "/video"})

@app.route('/video')
def serve_video():
    return send_from_directory('static', 'output.mp4')

if __name__ == '__main__':
    app.run(debug=True)
