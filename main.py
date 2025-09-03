import cv2
import torch
import streamlit as st
import numpy as np
from PIL import Image

# Use Streamlit's caching to load the model only once
@st.cache_resource
def load_model():
    """Loads and caches the YOLOv5 model."""
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)
    return model

def get_position(x, frame_width):
    """Returns the horizontal position of an object."""
    if x < frame_width / 3:
        return "left"
    elif x < 2 * frame_width / 3:
        return "center"
    else:
        return "right"

def process_image(image_data):
    """
    Processes a single image to detect objects and returns descriptions.
    """
    model = load_model()
    
    # Convert the uploaded image data to an OpenCV-compatible format
    pil_image = Image.open(image_data)
    frame = np.array(pil_image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    frame_height, frame_width = frame.shape[:2]
    
    # Run object detection
    results = model(frame)
    detections = results.xyxy[0]
    
    detected_objects = []
    if len(detections) > 0:
        # Sort detections by confidence score
        detections = detections[detections[:, 4].argsort(descending=True)]
        
        for *box, conf, cls in detections[:6]: # Process top 6 objects
            if conf < 0.4:
                continue

            label = model.names[int(cls)]
            x1, y1, x2, y2 = map(int, box)
            obj_center_x = (x1 + x2) // 2
            position = get_position(obj_center_x, frame_width)
            
            description = f"a {label} at your {position}"
            detected_objects.append(description)
            
    return detected_objects