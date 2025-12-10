import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions.pose import Pose
from mediapipe.python.solutions.pose import PoseLandmark

from knowledge_vault.models.schemas import Posture


def load_pose_model() -> Pose:
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

    pose_model = load_pose_model()
    results = pose_model.process(rgb_image)

    if not results.pose_landmarks:
        return None

    return results.pose_landmarks.landmark

def _calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def detect_posture(landmarks):
    issues = []
    score = 100

    left_shoulder = [landmarks[PoseLandmark.LEFT_SHOULDER.value].x, landmarks[PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[PoseLandmark.RIGHT_SHOULDER.value].y]
    left_hip = [landmarks[PoseLandmark.LEFT_HIP.value].x, landmarks[PoseLandmark.LEFT_HIP.value].y]
    left_ear = [landmarks[PoseLandmark.LEFT_EAR.value].x, landmarks[PoseLandmark.LEFT_EAR.value].y]
    left_knee = [landmarks[PoseLandmark.LEFT_KNEE.value].x, landmarks[PoseLandmark.LEFT_KNEE.value].y]

    torso_angle = _calculate_angle(left_shoulder, left_hip, left_knee)
    if torso_angle < 160:
        issues.append("slouch")
        score -= 20

    if left_ear[0] < left_shoulder[0] - 0.05:
        issues.append("forward head")
        score -= 20

    if abs(left_shoulder[1] - right_shoulder[1]) > 0.05:
        issues.append("shoulder tilt")
        score -= 10

    status = "good" if not issues else "bad"

    return Posture(status=status, issues=issues, score=score)
