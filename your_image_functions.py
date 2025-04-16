# your_image_functions.py
import cv2
import base64
import requests
import os

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

