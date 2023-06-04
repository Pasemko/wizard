import cv2 as cv
import numpy as np
import mediapipe as mp

# TODO: Pass styles to painter constructor
class Painter:
    def draw_bounding_rect(self, image, rect):
        cv.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]),
                    (0, 0, 0), 1)

        return image

    def draw_info_text(self, image, text, rect):
        cv.rectangle(image, (rect[0], rect[1]), (rect[2], rect[1] - 22),
                    (0, 0, 0), -1)

        cv.putText(image, text, (rect[0] + 5, rect[1] - 4),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

        return image

    def draw_landmarks(self, image, landmarks):
        mp.solutions.drawing_utils.draw_landmarks(image, 
                                                  landmarks,
                                                  mp.solutions.hands.HAND_CONNECTIONS)

        return image
    
    def draw_line_between_fingers(self, image, landmarks, finger_1, finger_2):
        image_width, image_height = image.shape[1], image.shape[0]
        finger_1_tip = landmarks.landmark[finger_1]
        finger_2_tip = landmarks.landmark[finger_2]
        image = cv.line(image, 
                        (int(finger_1_tip.x * image_width), int(finger_1_tip.y * image_height)), 
                        (int(finger_2_tip.x * image_width), int(finger_2_tip.y * image_height)), 
                        (0, 255, 0), 
                        2)
        
        return image

    
    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for landmark in landmarks.landmark:
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]
