import cv2
import torch
import streamlit as st
import numpy as np

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

def get_distance(y, frame_height):
    """Estimates the approximate distance of an object."""
    ratio = y / frame_height
    if ratio > 0.75:
        return "very close"
    elif ratio > 0.55:
        return "close"
    elif ratio > 0.35:
        return "a bit far"
    else:
        return "far away"

def process_video_frame(frame: np.ndarray):
    """
    Processes a single video frame to detect objects, draw boxes, and return descriptions.
    """
    model = load_model()
    
    # Run object detection
    results = model(frame)
    detections = results.xyxy[0]
    
    detected_objects = []
    if len(detections) > 0:
        # Sort detections by confidence
        detections = detections[detections[:, 4].argsort(descending=True)]
        
        for *box, conf, cls in detections[:6]: # Process top 6 objects
            if conf < 0.4:
                continue

            label = model.names[int(cls)]
            x1, y1, x2, y2 = map(int, box)
            obj_center_x = (x1 + x2) // 2
            obj_center_y = (y1 + y2) // 2

            # Get position and distance
            position = get_position(obj_center_x, frame.shape[1])
            distance = get_distance(obj_center_y, frame.shape[0])
            
            description = f"{label} {distance} at your {position}"
            detected_objects.append(description)
            
            # Draw bounding boxes and labels on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (36, 255, 12), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)
            
    return frame, detected_objects