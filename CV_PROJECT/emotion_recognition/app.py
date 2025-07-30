import pickle

import cv2

from utils import get_face_landmarks



emotions = ['HAPPY', 'SAD', 'SURPRISED', 'ANGRY', 'NEUTRAL']
# After training


with open('CV_PROJECT/emotion_recognition/model', 'rb') as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

while ret:
    ret, frame = cap.read()

    face_landmarks = get_face_landmarks(frame, draw=True, static_image_mode=False)
    try:
        output = model.predict([face_landmarks])
   
        print((output[0]))
        cv2.putText(frame,
                    emotions[int(output[0])],
                (10, frame.shape[0] - 1),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (0, 255, 0),
                5)
    except Exception as e:
        print("Error:", e)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.waitKey(50)


cap.release()
cv2.destroyAllWindows()