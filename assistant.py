# assistant.py
from openai import OpenAI
from your_image_functions import analyze_image, capture_image
import os

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def handle_user_input(user_input):
    prompt = (
        "If and only if the user's input is specifically asking to describe what is in front of them, "
        "such as 'what is in front of me?', 'describe the scene around me', 'what do you see?', or similar phrases, "
        "then return exactly '1' and nothing else. "
        "Otherwise, answer normally. "
        f"User prompt: {user_input}"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content

def analyze_camera_image():
    image_path = capture_image()
    return analyze_image(image_path) if image_path else "No image available."
