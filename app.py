from flask import Flask, request, jsonify, render_template_string
from assistant import handle_user_input, analyze_camera_image

app = Flask(__name__)

# Home route with a basic HTML form
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

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or request.form
    message = data.get('message', '')
    result = handle_user_input(message)
    return jsonify({'response': result})

@app.route('/analyze', methods=['GET'])
def analyze():
    result = analyze_camera_image()
    return jsonify({'description': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
