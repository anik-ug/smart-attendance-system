"""Live face recognition + automatic attendance marking."""
import cv2
import face_recognition
import numpy as np

from database import get_all_users, mark_attendance

THRESHOLD = 0.5      # lower = stricter matching
SCALE = 0.25         # resize frame for faster processing


def run_recognition():
    users = get_all_users()
    if not users:
        print("No registered users. Run register.py first.")
        return

    ids = [u[0] for u in users]
    names = [u[1] for u in users]
    rolls = [u[2] for u in users]
    known_encodings = [u[3] for u in users]

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    print("Recognition started. Press 'q' to quit.")
    process_this_frame = True
    results = []  # (top, right, bottom, left, label, color)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if process_this_frame:
            small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
            rgb_small = np.ascontiguousarray(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
            locations = face_recognition.face_locations(rgb_small)
            encodings = face_recognition.face_encodings(rgb_small, locations)

            results = []
            for (top, right, bottom, left), enc in zip(locations, encodings):
                distances = face_recognition.face_distance(known_encodings, enc)
                best = int(np.argmin(distances))
                top, right, bottom, left = [int(v / SCALE) for v in (top, right, bottom, left)]

                if distances[best] < THRESHOLD:
                    newly_marked = mark_attendance(ids[best])
                    status = "MARKED" if newly_marked else "Already marked"
                    label = f"{names[best]} ({rolls[best]}) - {status}"
                    color = (0, 200, 0)
                    if newly_marked:
                        print(f"Attendance marked: {names[best]} ({rolls[best]})")
                else:
                    label = "Unknown"
                    color = (0, 0, 255)
                results.append((top, right, bottom, left, label, color))

        process_this_frame = not process_this_frame

        for top, right, bottom, left, label, color in results:
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Smart Attendance (press q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_recognition()
