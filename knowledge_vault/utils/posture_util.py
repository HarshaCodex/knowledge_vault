import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions.pose import PoseLandmark


def load_pose_model():
    mp_pose = mp.solutions.pose
    
    pose = mp_pose.Pose(static_image_mode=True,
                        model_complexity=2,
                        enable_segmentation=False,
                        smooth_landmarks=False,
                        min_detection_confidence=0.5)
    
    return pose

def extract_landmarks(image_bytes):
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    bgr_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    rgb_image.flags.writeable = False

    image_pose = load_pose_model().process(rgb_image)

    landmarks = image_pose.pose_landmarks.landmark

