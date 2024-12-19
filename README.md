# Hand Volume Control
This project implements a system to control your computer's audio volume using hand gestures via a webcam. It leverages MediaPipe for hand tracking and pycaw for audio control.

## Features
- **Mute and Unmute**: Bring your thumb and index finger together to mute, and separate them to unmute.
- **Volume Adjustment**: Adjust the volume by varying the distance between your thumb and index finger. The closer they are, the lower the volume, and vice versa.

## Prerequisites
Make sure you have the following installed:
- Python 3.7+
- OpenCV
- MediaPipe
- pycaw
- comtypes

You can install the required Python libraries with the following command:

```bash
pip install -r requirements.txt
```
Or with this command: 
```bash
pip install opencv-python mediapipe pycaw comtypes
```
## How It Works
1. **Hand Tracking**: The program uses MediaPipe to detect and track hand landmarks from the webcam feed.
2. **Gesture Recognition**: Key landmarks (thumb and index finger tips) are used to calculate the distance between them.
3. **Volume Control**:
   - If the distance is below a threshold, the system mutes.
   - If the distance increases again, it unmutes.
   - The distance is also normalized to adjust volume smoothly based on its magnitude.

## Code Explanation
- MediaPipe Hands is used to detect and process hand landmarks.
- pycaw is utilized to interface with the audio system for volume control.

### Main Loop
- Captures video frames from the webcam.
- Processes each frame to detect hand landmarks.
- Extracts key points (thumb and index finger tips).
- Calculates distance and normalizes it.
- Adjusts the volume or toggles mute/unmute based on gesture.

## Usage
1. Run the script:

```bash
   python hand_volume_control.py
```
2. Allow access to your webcam.
3. Perform gestures in front of the camera:
   - **Mute/Unmute**: Touch your thumb and index finger together to mute. Separate them to unmute.
   - **Volume Adjustment**: Vary the distance between your thumb and index finger.
4. Press `q` to exit the application.
