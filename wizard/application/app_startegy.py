import csv
from abc import ABC, abstractmethod
from wizard.configuration import paths
import mediapipe as mp
from wizard.application.autogui_controller import *
from wizard.configuration.constants import *
from math import hypot
import numpy as np
import subprocess
import cv2 as cv

LEFT_BUTTON_PRESSED = False
RIGHT_BUTTON_PRESSED = False

def transform_point(point, img_param, screen_param):
    return int(min(point * screen_param, screen_param - 1))

class AppStrategy(ABC):

    @abstractmethod
    def handle_hand_gestures(self, hand_gestures):
        pass

    @abstractmethod
    def update_with_parameters(self, parameters: dict):
        pass


class DatasetRecordingApp(AppStrategy):

    def __init__(self):
         super().__init__()
         self.currently_recording_gesture_id = -1

    def handle_hand_gestures(self, hand_gestures):
        for gesture in hand_gestures:
            preprocessed_landmarks = self.__preprocess_landmarks(gesture.landmarks)
            if self.currently_recording_gesture_id != -1:
                with open(paths.keypoints_dataset_path(), 'a+', newline="") as f:
                                writer = csv.writer(f)
                                writer.writerow([
                                    self.currently_recording_gesture_id, 
                                    *preprocessed_landmarks
                                    ])
        
        self.currently_recording_gesture_id = -1
    

    def update_with_parameters(self, parameters: dict):
         if 'gesture_id' in parameters:
              self.currently_recording_gesture_id = parameters['gesture_id']
        

    def __preprocess_landmarks(self, landmarks): # TODO: Extract to utils to get rid of code dublications (see HandGestureDetector)
        # Convert to 1D array
        landmark_points = []
        for landmark in landmarks.landmark:
            landmark_points.append(landmark.x)
            landmark_points.append(landmark.y)
            landmark_points.append(landmark.z)

        return landmark_points


class HumanComputerInteractionApp(AppStrategy):
    def handle_hand_gestures(self, hand_gestures):
        for gesture in hand_gestures:
             self.hand_gestures_dispatcher(gesture)


    def update_with_parameters(self, parameters: dict):
        
         pass
    
    def hand_gestures_dispatcher(self, gesture):
        global LEFT_BUTTON_PRESSED, RIGHT_BUTTON_PRESSED

        if gesture.id == 1:
            if self.check_fingers_touching(gesture.landmarks,
                                           mp.solutions.hands.HandLandmark.THUMB_TIP,
                                           mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP):
                # Check if the left button is not already pressed
                if not LEFT_BUTTON_PRESSED:
                        press_left_mouse_button()
                        LEFT_BUTTON_PRESSED = True
            elif LEFT_BUTTON_PRESSED:
                    release_left_mouse_button()
                    LEFT_BUTTON_PRESSED = False

            if self.check_fingers_touching(gesture.landmarks,
                                           mp.solutions.hands.HandLandmark.THUMB_TIP,
                                           mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP):
                click_right_mouse_button()

            pointer_finger_landmark = gesture.landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]

            x = transform_point(pointer_finger_landmark.x, IMG_HEIGHT, SCREEN_HEIGHT)
            y = transform_point(pointer_finger_landmark.y, IMG_WIDTH, SCREEN_WIDTH)
            move_cursor(x, y)

        if gesture.id == 0:
            pointer_finger_landmark = gesture.landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            x = transform_point(pointer_finger_landmark.x, IMG_HEIGHT, SCREEN_HEIGHT)
            y = transform_point(pointer_finger_landmark.y, IMG_WIDTH, SCREEN_WIDTH)
            move_cursor(x, y)
        
        if gesture.id == 3:
            thumb_landmark = gesture.landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            x1, y1 = int(thumb_landmark.x * SCREEN_WIDTH), int(thumb_landmark.y * SCREEN_HEIGHT)

            pointer_finger_landmark = gesture.landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            x2, y2 = int(pointer_finger_landmark.x * SCREEN_WIDTH), int(pointer_finger_landmark.y * SCREEN_HEIGHT)

            
            length = hypot(x1 - x2, y1 - y2)
            vol = np.interp(length, [15, 220], [0, 100])

            # Set the volume using AppleScript
            subprocess.run(['osascript', '-e', f'set volume output volume {int(vol)}'])
    
    def check_fingers_touching(self, landmarks, finger1_id, finger2_id):
        finger_1 = landmarks.landmark[finger1_id]
        finger_2 = landmarks.landmark[finger2_id]
        
        finger_1_x = int(finger_1.x * SCREEN_WIDTH)
        finger_1_y = int(finger_1.y * SCREEN_HEIGHT)
        finger_2_x = int(finger_2.x * SCREEN_WIDTH)
        finger_2_y = int(finger_2.y * SCREEN_HEIGHT)

        distance = ((finger_1_x - finger_2_x) ** 2 + (finger_1_y - finger_2_y) ** 2) ** 0.5
        
        # Threshold for determining if thumb and index finger are touching
        threshold = 55

        return distance <= threshold

