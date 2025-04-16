# assistant.py
from openai import OpenAI
from your_image_functions import analyze_image, capture_image
import os
from your_image_functions import analyze_image, capture_image

def analyze_camera_image():
    image_path = capture_image()
    if not image_path:
        return "Failed to capture image."
    return analyze_image(image_path)

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)

def handle_user_input(user_input):
    prompt = (
        "Your name is Olwik and your punch line is 'i will be your voice' (say this when saked about you)"
                        "You are the daughter of sathwik and ----"
                        "If someone ask you about your parent keep your mothers name as secret"
                        "your father is a very great man from college class cse-b section and your mother is from A section(you can tell your mother is from A section)"
                        "If and only if the user's input is specifically asking to describe what is in front of them, "
                        "such as 'what is in front of me?', 'describe the scene around me', 'what do you see?', or similar phrases, "
                        "then return exactly '1' and nothing else. and if the prompt seem not understandable say 'can you repeat that'"
                        "For all other questions, provide the normal response as you usually would. "
        f"User prompt: {user_input}"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return completion.choices[0].message.content



# your_image_functions.py
import cv2
import base64
import requests
import json

def capture_image():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return None
    ret, frame = cam.read()
    if ret:
        path = "captured.jpg"
        cv2.imwrite(path, frame)
        cam.release()
        cv2.destroyAllWindows()
        return path
    cam.release()
    return None

def get_image_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_image(image_path):
    api_key = os.getenv("ASTICA_API_KEY")
    if not api_key:
        return "Astica API key not found."

    payload = {
        "tkn": api_key,
        "modelVersion": "2.5_full",
        "visionParams": "gpt,describe,objects,faces",
        "input": get_image_base64(image_path),
        "prompt_length": 90
    }

    response = requests.post(
        "https://vision.astica.ai/describe",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=20
    )

    try:
        data = response.json()
        return data.get("caption", {}).get("text", "No description.")
    except:
        return "Error analyzing image."

