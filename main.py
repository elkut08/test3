import time
from datetime import datetime
import cv2

cap = cv2.VideoCapture(0)

is_recording = False
video_writer = None
prev_time = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
    prev_time = current_time

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cv2.putText(frame, "MotionWeb", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Date: {now}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame, "Classes: person, cat, car", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 80, 200), 1)

    if is_recording and video_writer is not None:
        video_writer.write(frame)
        cv2.putText(frame, "REC [TEST_V]", (frame.shape[1] - 170, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("MotionWeb", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('e'):
        break
    elif key == ord('v'):
        if not is_recording:
            is_recording = True
            h, w, _ = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            filename = f"test_v_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
            video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))
        else:
            is_recording = False
            if video_writer:
                video_writer.release()
    elif key == ord('s'):
        img_name = f"test_s_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(img_name, frame)

cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()