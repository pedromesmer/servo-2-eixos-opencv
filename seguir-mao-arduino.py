import cv2
import mediapipe as mp
import numpy as np
import serial
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)

keypoints_list = []

# alterar porta de acordo com as configurações do arduino
port = '/dev/cu.usbmodem1301'
baudrate = 115200
timeout = .1

arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            keypoints = []
            for i, landmark in enumerate(hand_landmarks.landmark):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                keypoints.append([round(landmark.x, 6), round(landmark.y, 6), round(landmark.z, 6)])

                if i == 8: # ponta indicador

                    x_send = int(landmark.x * 1000)
                    y_send = int(landmark.y * 1000)

                    msg = f"{x_send},{y_send}\n"
                    arduino.write(msg.encode("utf-8"))

                    cv2.putText(frame, f"{i}: ({landmark.x:.2f}, {landmark.y:.2f}, {landmark.z:.2f})",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)

                    threshold = 0.05

                    if abs(landmark.x - 0.50) < threshold and abs(landmark.y - 0.50) < threshold:
                        cv2.putText(frame, "CENTRO", (x, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            keypoints_list.append(keypoints)

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
