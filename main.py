import cv2
import torch
import time

# -------------------------------
# Load YOLOv5 model
# -------------------------------
# Uses the pretrained 'yolov5s' model from Ultralytics hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# -------------------------------
# Helper functions
# -------------------------------

def get_position(x, frame_width):
    """
    Returns horizontal position of object based on x-coordinate.
    - left: left third
    - center: middle third
    - right: right third
    """
    if x < frame_width / 3:
        return "left"
    elif x < 2 * frame_width / 3:
        return "center"
    else:
        return "right"

def get_distance(y, frame_height):
    """
    Estimates approximate distance of object from camera using y-coordinate.
    Returns one of: "very close", "close", "a bit far", "far away"
    """
    ratio = y / frame_height
    if ratio > 0.75:
        return "very close"
    elif ratio > 0.55:
        return "close"
    elif ratio > 0.35:
        return "a bit far"
    else:
        return "far away"

# -------------------------------
# Main scanning function
# -------------------------------

def scan_environment(duration=3, max_objects=6, min_conf=0.4):
    """
    Scans the environment using webcam for a given duration (seconds).
    Returns a list of unique detected object descriptions.
    """
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    detected_objects = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Stop scanning after specified duration
        if time.time() - start_time > duration:
            break

        frame_height, frame_width = frame.shape[:2]

        # YOLOv5 detection
        results = model(frame)
        detections = results.xyxy[0]

        if len(detections) > 0:
            # Sort by confidence descending
            detections = detections[detections[:, 4].argsort(descending=True)]

            # Process top objects only
            for *box, conf, cls in detections[:max_objects]:
                if conf < min_conf:
                    continue

                x1, y1, x2, y2 = map(int, box)
                label = model.names[int(cls)]
                obj_center_x = (x1 + x2) // 2
                obj_center_y = (y1 + y2) // 2

                position = get_position(obj_center_x, frame_width)
                distance = get_distance(obj_center_y, frame_height)

                description = f"{label} {distance} at your {position}"
                detected_objects.append(description)

    cap.release()
    cv2.destroyAllWindows()

    # Remove duplicates while preserving order
    unique_objects = []
    seen = set()
    for obj in detected_objects:
        if obj not in seen:
            unique_objects.append(obj)
            seen.add(obj)

    return unique_objects
