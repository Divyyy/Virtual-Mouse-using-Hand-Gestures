# **Virtual Mouse using Hand Gestures**

This project allows you to control your computer's mouse using hand gestures, providing a touchless way to interact with your screen. It uses your webcam to track your hand movements and translate them into mouse actions like moving the cursor, clicking, and even taking screenshots.

## **Features**

* **Mouse Movement:** Control the cursor by moving your index finger.  
* **Left Click:** Perform a left click by bending your middle finger.  
* **Right Click:** Perform a right click by bending your ring finger.  
* **Double Click:** Perform a double click by bending both your middle and ring fingers.  
* **Screenshot:** Take a screenshot by making a fist.

## **Technologies Used**

* **Python:** The core programming language for the project.  
* **OpenCV:** Used for capturing the video feed from the webcam, processing frames (like flipping the image), and displaying the video stream with drawn landmarks back to the user.  
* **MediaPipe:** A powerful framework from Google that provides a pre-trained hand-tracking model. It analyzes each frame to detect the presence of a hand and returns the 3D coordinates of its 21 key landmarks.  
* **PyAutoGUI & Pynput:** A combination of libraries used to programmatically control the mouse and keyboard. PyAutoGUI handles moving the cursor and taking screenshots, while Pynput manages the click events.  
* **NumPy:** A fundamental library for numerical computation. It's used here to perform the vector math required for calculating the angles and distances between hand landmarks.

## **Installation**

1. **Clone the repository:**  
   git clone https://github.com/your-username/virtual-mouse.git  
   cd virtual-mouse

2. **Create a virtual environment (optional but recommended):**  
   python \-m venv venv  
   source venv/bin/activate  \# On Windows, use \`venv\\Scripts\\activate\`

3. **Install the required dependencies:**  
   pip install \-r requirements.txt

   *(Note: You will need to create a requirements.txt file. See below for its content.)*

## **requirements.txt**

Create a file named requirements.txt in the root of your project directory and add the following lines:

opencv-python  
mediapipe  
pyautogui  
pynput  
numpy

## **Usage**

To run the virtual mouse, execute the main Python script from your terminal:

python "vritual mouse.py"

A window will appear showing your webcam feed with the hand landmarks drawn on it. Your hand gestures will now control the mouse. To stop the program, press the 'q' key.

## **How It Works: From Pixels to Clicks**

The application translates your hand movements into mouse actions through a four-step pipeline:

1. **Camera Input:** OpenCV continuously captures frames from your webcam. Each frame is flipped horizontally so that your hand's movement appears natural and intuitive (moving your hand right moves the cursor right).  
2. **Hand Landmark Detection:** Each frame is passed to MediaPipe's Hand Tracking model. If a hand is detected, the model returns 21 landmarks for that hand. Each landmark is a point with x, y, and z coordinates, normalized between 0 and 1\. For this 2D mouse, we primarily use the x and y coordinates.  
3. **Gesture Recognition:** This is the core logic of the application. Custom functions analyze the geometric relationships between the landmarks to determine the gesture being made.  
   * **Distances:** The distance between two landmarks (e.g., the thumb tip and index finger tip) is calculated. This is crucial for determining if a finger is "touching" another.  
   * **Angles:** The angle formed by three landmarks (e.g., the joints of a finger) is calculated to determine if a finger is bent or straight. For example, a straight finger will have an angle close to 180 degrees at its middle joint, while a bent finger will have a much smaller angle.  
4. **Mouse Action:** Once a gesture is recognized, a corresponding command is sent to the operating system.  
   * pyautogui.moveTo(x, y) is used to position the cursor, mapping the index finger's normalized coordinates to your screen's pixel dimensions.  
   * mouse.click() or mouse.press() from the pynput library is used to execute left, right, or double clicks.

## **Code Explanation**

Here’s a breakdown of the key functions that make the gesture recognition possible:

* **get\_angle(a, b, c)**: This function calculates the angle at point b formed by the lines connecting a-b and b-c. It uses np.arctan2 to find the angle of each vector and then finds the difference to get the angle between them. This is the fundamental tool for checking if a finger is bent.  
* **get\_distance(landmark\_list)**: This function calculates the straight-line distance between two landmark points. The result is then interpolated from the camera's normalized coordinate system to a larger scale (\[0, 1000\]) to make it easier to work with when setting gesture thresholds.  
* **is\_left\_click(landmarks\_list, thumb\_index\_dist)**: This function defines the conditions for a left click. It returns True only if the angle of the middle finger is small (i.e., it's bent), the ring finger is relatively straight, and the distance between the thumb and index finger is large (to avoid clicking while moving the cursor). Similar logic applies to is\_right\_click and is\_double\_click.  
* **detect\_gestures(...)**: This is the main control function. In each frame, it checks for the defined gestures in a specific order of priority. It first checks for mouse movement, then for the various clicks, and finally for the screenshot gesture. This prevents multiple actions from being triggered simultaneously.

## **Future Scope**

* **Drag and Drop:** Implement a gesture for holding down the mouse button to allow for dragging and dropping.  
* **Scrolling:** Add gestures for vertical and horizontal scrolling.  
* **Customizable Gestures:** Allow users to define their own gestures for different actions.