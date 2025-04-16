from flask import Flask, request, jsonify
from assistant import handle_user_input


app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    message = data.get('message', '')
    result = handle_user_input(message)
    return jsonify({'response': result})

@app.route('/analyze', methods=['GET'])
def analyze():
    result = analyze_camera_image()
    return jsonify({'description': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
