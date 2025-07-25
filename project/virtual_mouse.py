import cv2
import mediapipe as mp
import pickle
import numpy as np
import pyautogui

# Load the trained model from the file
try:
    with open('model.p', 'rb') as f:
        model_dict = pickle.load(f)
    model = model_dict['model']
except FileNotFoundError:
    print("❌ Error: 'model.p' not found.")
    print("Please make sure you have downloaded the model file from Colab and placed it in the same folder as this script.")
    exit()

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Get screen size
screen_width, screen_height = pyautogui.size()

print("✅ Virtual mouse started. Show your hand to the camera.")
print("Press 'q' to quit.")

# Gesture labels mapping (must match the labels used during training)
# The model was trained on: ['fist', 'palm', 'peace', 'one', 'two', 'call', 'ok']
labels_dict = {
    'fist': 'Click',
    'palm': 'Move',
    'one': 'Move', # Pointing with one finger to move
    'peace': 'Scroll Down',
    'ok': 'Scroll Up',
    'call': 'Right Click',
    'two': 'Right Click'
}

# Smoothing variables for cursor movement
smooth_factor = 0.7
prev_x, prev_y = 0, 0

# Click debounce variables
last_click_time = 0
click_delay = 0.5 # seconds

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a more intuitive mirror-like view
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find hand landmarks
    results = hands.process(frame_rgb)

    predicted_gesture = "No hand detected"

    if results.multi_hand_landmarks:
        data_aux = []
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark coordinates for prediction
            for landmark in hand_landmarks.landmark:
                data_aux.append(landmark.x)
                data_aux.append(landmark.y)

            # Make a prediction
            prediction = model.predict([np.asarray(data_aux)])
            predicted_gesture_raw = prediction[0]
            predicted_gesture = labels_dict.get(predicted_gesture_raw, "Unknown")


            # --- MOUSE CONTROL LOGIC ---
            index_finger_tip = hand_landmarks.landmark[8] # Landmark for index finger tip
            x, y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)

            # Smooth the movement
            current_x = prev_x + (x - prev_x) * (1 - smooth_factor)
            current_y = prev_y + (y - prev_y) * (1 - smooth_factor)


            if predicted_gesture == 'Move':
                pyautogui.moveTo(current_x, current_y)

            elif predicted_gesture == 'Click':
                # Debounce the click to prevent multiple clicks
                if (cv2.getTickCount() - last_click_time) / cv2.getTickFrequency() > click_delay:
                    pyautogui.click()
                    print("Action: Left Click")
                    last_click_time = cv2.getTickCount()
            
            elif predicted_gesture == 'Right Click':
                if (cv2.getTickCount() - last_click_time) / cv2.getTickFrequency() > click_delay:
                    pyautogui.rightClick()
                    print("Action: Right Click")
                    last_click_time = cv2.getTickCount()

            elif predicted_gesture == 'Scroll Up':
                pyautogui.scroll(100) # Scroll up
                print("Action: Scroll Up")

            elif predicted_gesture == 'Scroll Down':
                pyautogui.scroll(-100) # Scroll down
                print("Action: Scroll Down")

            prev_x, prev_y = current_x, current_y


    # Display the predicted gesture on the frame
    cv2.putText(frame, f"Gesture: {predicted_gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow('AI Virtual Mouse', frame)

    # Check for 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
print("Virtual mouse stopped.")

