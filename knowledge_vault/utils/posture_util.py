import mediapipe as mp

def load_pose_model():
    mp_pose = mp.solutions.pose
    
    pose = mp_pose.Pose(static_image_mode=True,
                        model_complexity=2,
                        enable_segmentation=False,
                        smooth_landmarks=False,
                        min_detection_confidence=0.5)
    
    return pose