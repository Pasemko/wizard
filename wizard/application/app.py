import cv2 as cv

from wizard.application.video_capture import VideoCapture
from wizard.detectors.hand_gesture_detector import HandGestureDetector
from wizard.application.app_startegy import HumanComputerInteractionApp, DatasetRecordingApp
from wizard.application.painter import Painter
from wizard.configuration.paths import backend_folder_path


class MainApp:

    def __init__(self):
        self.video_capture = VideoCapture()
        self.hand_gesture_detector = HandGestureDetector()
        self.context = HumanComputerInteractionApp()
        self.painter = Painter()

        self.video = cv.VideoWriter('video.mp4',
                                    cv.VideoWriter_fourcc(*'XVID'),
                                    10, (int(self.video_capture.cap.get(3)), int(self.video_capture.cap.get(4))))


    def __del__(self):
        cv.destroyAllWindows()
        self.video.release()


    def run(self):
        while True:
            key = cv.waitKey(1)
            if key == ord('q'):
                break
            elif ord('0') <= key <= ord('9'):
                self.context.update_with_parameters({'gesture_id': int(chr(key))})
            else:
                self.decide_strategy(key)

            ret, frame = self.video_capture.read()
            if not ret:
                break

            hand_gestures = self.hand_gesture_detector.process_frame(frame)
            if hand_gestures:
                self.context.handle_hand_gestures(hand_gestures)

                # Draw Hand gestures info
                for gesture in hand_gestures:
                    rect = self.painter.calc_bounding_rect(frame, gesture.landmarks)
    
                    frame = self.painter.draw_info_text(frame, gesture.name, rect)
                    frame = self.painter.draw_bounding_rect(frame, rect)
                    frame = self.painter.draw_landmarks(frame, gesture.landmarks)
                    
                    if gesture.id == 3:
                        frame = self.painter.draw_line_between_fingers(frame, gesture.landmarks, 
                                                                       self.hand_gesture_detector.mp_hands.HandLandmark.THUMB_TIP,
                                                                       self.hand_gesture_detector.mp_hands.HandLandmark.INDEX_FINGER_TIP)
                    

            cv.imshow('Wizard', frame)
            # self.video.write(frame)
    
    def decide_strategy(self, key):
        if key == ord('d'):
            self.context = DatasetRecordingApp()
        elif key == ord('n'):
            self.context = HumanComputerInteractionApp()
