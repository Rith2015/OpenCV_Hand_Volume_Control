import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize audio control 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# volume range
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]

cap = cv2.VideoCapture(0)
is_muted = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Get screen coordinates
            thumb_pos = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))
            index_pos = (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0]))

            # Draw visualization of index finger, thumb and the line between index finger and thumb
            cv2.circle(frame, thumb_pos, 10, (255, 0, 0), -1)
            cv2.circle(frame, index_pos, 10, (0, 255, 0), -1)
            cv2.line(frame, thumb_pos, index_pos, (0, 255, 255), 2)

            # Calculate distance between thumb and index finger
            distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)

            # Normalize distance to range
            normalized_distance = min(max((distance - 0.08) / (0.2 - 0.08), 0), 1)

            if normalized_distance < 0.01:  # Mute if distance is smaller then certain distance
                if not is_muted:
                    volume.SetMute(1, None)
                    is_muted = True
                    print("Muted")
            elif is_muted:  # Unmute when the fingers move apart
                volume.SetMute(0, None)
                is_muted = False
                print("Unmuted")

            if not is_muted:
                # Adjust volume based on the distance  between index finger and thumb
                new_volume = normalized_distance * (max_volume - min_volume) + min_volume
                volume.SetMasterVolumeLevelScalar(normalized_distance, None)

    # Display video feed
    cv2.imshow("Hand Gesture Volume Control", frame)

    # Press 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
