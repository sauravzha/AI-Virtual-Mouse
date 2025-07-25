# AI-Virtual-Mouse
AI Hand Gesture Virtual Mouse 🖱️✨
This project provides a futuristic way to interact with your computer by transforming your hand into a virtual mouse. Using just a standard webcam, this Python application tracks your hand movements and gestures in real-time, allowing you to perform standard mouse operations like moving the cursor, clicking, and scrolling without any physical hardware.

This repository contains all the necessary code and the pre-trained machine learning model to run the application on your own machine.

🔧 Technology Stack
This project is built with a combination of powerful, open-source libraries:

Python 3.8+

OpenCV: For capturing the webcam feed and displaying video.

MediaPipe: For high-fidelity hand and finger tracking.

Scikit-learn: For the Random Forest classification model that recognizes gestures.

PyAutoGUI: For programmatically controlling the mouse and keyboard.

🚀 Features & Gesture Controls
The application can recognize a variety of gestures, each mapped to a specific mouse function.

Gesture

Action

Pointing (One finger)

Moves the mouse cursor

Fist

Performs a Left Click

"Call Me" Sign

Performs a Right Click

"OK" Sign

Scrolls Up

"Peace" Sign

Scrolls Down

🛠️ Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Make sure you have Python 3.8 or newer installed on your system.

2. Clone the Repository (or Download)
If you have Git, you can clone the repository from your terminal:

git clone [https://github.com/YOUR_USERNAME/AI-Virtual-Mouse.git](https://github.com/YOUR_USERNAME/AI-Virtual-Mouse.git)
cd AI-Virtual-Mouse

(Replace YOUR_USERNAME with your actual GitHub username).

Alternatively, you can download the project as a ZIP file from GitHub and extract it.

3. Install Dependencies
Navigate to the project folder in your terminal and run the following command to install the required Python libraries:

pip install opencv-python mediapipe scikit-learn pyautogui

4. Trained Model
The trained model (model.p) is included in this repository. Ensure it is in the same directory as the virtual_mouse.py script.

🏃‍♀️ How to Run
Make sure your webcam is connected and not being used by another application.

Open your terminal and navigate to the project directory.

Run the main script:

python virtual_mouse.py

A window showing your webcam feed will appear. Show your hand to the camera to start controlling the mouse.

To stop the program, press the 'q' key on your keyboard while the webcam window is active.

⚙️ How It Works
The application operates through a real-time pipeline:

Video Capture: The script uses OpenCV to capture video frames from your default webcam.

Hand Tracking: Each frame is passed to MediaPipe, which detects and tracks the 21 key landmarks (joints) of the hand, providing their 3D coordinates.

Data Normalization: The landmark coordinates are flattened into a single array to serve as the input for the machine learning model.

Gesture Prediction: This data is fed into a pre-trained scikit-learn (Random Forest) model (model.p), which predicts the gesture being made based on the spatial relationship of the hand landmarks.

Mouse Action: Based on the predicted gesture, PyAutoGUI is used to execute the corresponding mouse action (move, click, scroll) on your operating system.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
This project was trained on the HaGRID (HAnd Gesture Recognition Image Dataset).

Special thanks to the developers of MediaPipe, OpenCV, and PyAutoGUI.
