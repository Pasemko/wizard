import cv2 as cv
import mediapipe as mp
from wizard.models.keypoint_classifier import KeyPointClassifier

GESTURE_LABELS = [
    'Index Finger',
    'V Sign with Thumb',
    'Three Fingers',
    'Palm',
]

class HandGestureInfo:
    def __init__(self, id=-1, name="", landmarks=None):
        self.id = id 
        self.name = name
        self.landmarks = landmarks


class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.keypoint_classifier = KeyPointClassifier()

    def process_frame(self, frame):
        gestures = []
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                gesture = HandGestureInfo()
                id = self.keypoint_classifier(self.__preprocess_landmarks(landmarks))
                gesture.id = id
                gesture.name = GESTURE_LABELS[id]
                gesture.landmarks = landmarks

                gestures.append(gesture)
        
        return gestures

    def __preprocess_landmarks(self, landmarks):
        # Convert to 1D array
        landmark_points = []
        for landmark in landmarks.landmark:
            landmark_points.append(landmark.x)
            landmark_points.append(landmark.y)
            landmark_points.append(landmark.z)

        return landmark_points