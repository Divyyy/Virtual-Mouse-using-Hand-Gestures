#!/usr/bin/env python
# coding: utf-8

# In[76]:


import cv2
import mediapipe as mp
import pyautogui
import app
from pynput.mouse import Button, Controller
mouse = Controller()


# In[77]:


screen_width, screen_height = pyautogui.size()
mouse = Controller()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode = False,
    model_complexity = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7,
    max_num_hands = 1,
)
    


# In[78]:


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None


# In[79]:


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x= int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x,y)


# In[80]:


def is_left_click(landmarks_list, thumb_index_dist):
    return (
        app.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        app.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmarks_list, thumb_index_dist):
    return (
        app.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 70 and
        app.get_angle(landmarks_list[9], landmarks_list[6], landmarks_list[8]) > 60 and
        thumb_index_dist > 40
    )

def is_double_click(landmarks_list, thumb_index_dist):
    return (
        app.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        app.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmarks_list, thumb_index_dist):
    return (
        app.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and
        app.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
        thumb_index_dist < 50
    )

           


# In[81]:


def detect_gestures(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = app.get_distance([landmarks_list[4], landmarks_list[5]])

        # Move mouse
        if thumb_index_dist < 50 and app.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
            move_mouse(index_finger_tip)

        # Left Click
        elif is_left_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame, "Left Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # Right Click
        elif is_right_click(landmarks_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame, "Right Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        # Double Click
        elif is_double_click(landmarks_list, thumb_index_dist):
            mouse.click(Button.left, 2)
            cv2.putText(frame, "Double Click", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        # Screenshot
        elif is_screenshot(landmarks_list, thumb_index_dist):
            pyautogui.screenshot("screenshot.png")
            cv2.putText(frame, "Screenshot Taken", (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)


# In[ ]:


def find_camera(max_index=5):
    """Automatically find the first working camera"""
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Using camera {i}")
            return cap
    raise Exception("No camera found")


def main():
    cap = find_camera()  # automatically selects camera
    draw = mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # mirror the frame
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            processed = hands.process(frameRGB)
            landmarks_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            detect_gestures(frame, landmarks_list, processed)

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to quit
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



# In[ ]:





# In[ ]:




