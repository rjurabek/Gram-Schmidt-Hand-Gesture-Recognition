import cv2
import mediapipe as mp
import numpy as np


def gram_schmidt(vectors):
    orthogonal = []

    for v in vectors:
        v = np.array(v, dtype=np.float64)

      
        for u in orthogonal:
            projection = (
                np.dot(v, u) / np.dot(u, u)
            ) * u

            v = v - projection

      
        norm = np.linalg.norm(v)

        if norm > 1e-8:
            orthogonal.append(v)

    
    orthonormal = []

    for v in orthogonal:
        v = v / np.linalg.norm(v)
        orthonormal.append(v)

    return orthonormal


def create_hand_coordinate_system(landmarks):
    """
    Create a coordinate system using the wrist,
    index finger and pinky.
    """

    wrist = landmarks[0]
    index_mcp = landmarks[5]
    pinky_mcp = landmarks[17]

  
    v1 = index_mcp - wrist

    v2 = pinky_mcp - wrist

    vectors = [v1, v2]

    basis = gram_schmidt(vectors)

    if len(basis) < 2:
        return None

    return basis


def distance(a, b):
    return np.linalg.norm(a - b)


def recognize_gesture(landmarks):
    """
    Simple gesture recognition.
    """

    wrist = landmarks[0]

    
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    
    index_dist = distance(index_tip, wrist)
    middle_dist = distance(middle_tip, wrist)
    ring_dist = distance(ring_tip, wrist)
    pinky_dist = distance(pinky_tip, wrist)

    index_base = distance(index_mcp, wrist)
    middle_base = distance(middle_mcp, wrist)
    ring_base = distance(ring_mcp, wrist)
    pinky_base = distance(pinky_mcp, wrist)

  
    index_open = index_dist > index_base * 1.35
    middle_open = middle_dist > middle_base * 1.35
    ring_open = ring_dist > ring_base * 1.25
    pinky_open = pinky_dist > pinky_base * 1.20

    fingers = [
        index_open,
        middle_open,
        ring_open,
        pinky_open
    ]

    count = sum(fingers)

   
    if count == 4:
        return "OPEN HAND"

    if count == 0:
        return "FIST"

    if index_open and middle_open and not ring_open and not pinky_open:
        return "PEACE"

    if index_open and not middle_open and not ring_open and not pinky_open:
        return "ONE"


    thumb_extended = distance(thumb_tip, wrist) > distance(index_mcp, wrist)

    if thumb_extended and count == 0:
        return "THUMBS UP"

    return "UNKNOWN"

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()


while True:

    success, frame = cap.read()

    if not success:
        print("ERROR: Cannot read camera")
        break

   
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture = "NO HAND"

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:


            landmarks = []

            for point in hand_landmarks.landmark:

                x = point.x
                y = point.y
                z = point.z

                landmarks.append(
                    np.array([x, y, z])
                )


            basis = create_hand_coordinate_system(
                landmarks
            )
            gesture = recognize_gesture(
                landmarks
            )
    
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            wrist = landmarks[0]
            if basis is not None:
                axis_length = 0.15
                axis_x = wrist + basis[0] * axis_length

                
                axis_y = wrist + basis[1] * axis_length

                h, w, _ = frame.shape

                wrist_pixel = (
                    int(wrist[0] * w),
                    int(wrist[1] * h)
                )

                x_pixel = (
                    int(axis_x[0] * w),
                    int(axis_x[1] * h)
                )

                y_pixel = (
                    int(axis_y[0] * w),
                    int(axis_y[1] * h)
                )

               
                cv2.line(
                    frame,
                    wrist_pixel,
                    x_pixel,
                    (255, 0, 0),
                    3
                )

                cv2.line(
                    frame,
                    wrist_pixel,
                    y_pixel,
                    (0, 255, 0),
                    3
                )

    cv2.rectangle(
        frame,
        (10, 10),
        (400, 80),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        gesture,
        (25, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Gram-Schmidt Hand Gesture Recognition",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()