"""Register a new user: capture face samples and store ONLY the encrypted
face vector (no photo is ever written to disk)."""
import cv2
import face_recognition
import numpy as np

from database import add_user

SAMPLES_NEEDED = 5


def register_user():
    print("PRIVACY NOTICE: only an encrypted numerical face vector is stored.")
    print("No photo is saved. Data stays on this machine.")
    consent = input("Do you give consent to store your face vector? (y/n): ")
    if consent.strip().lower() != "y":
        print("Consent not given. Registration cancelled.")
        return

    name = input("Enter name: ").strip()
    roll_no = input("Enter roll no / ID: ").strip()
    if not name or not roll_no:
        print("Name and roll no are required.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    encodings = []
    print("Press 'c' to capture (one face in frame), 'q' to quit.")

    while len(encodings) < SAMPLES_NEEDED:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, f"Captured: {len(encodings)}/{SAMPLES_NEEDED}  (c = capture, q = quit)",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Register", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("c"):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            locations = face_recognition.face_locations(rgb)
            if len(locations) != 1:
                print(f"Found {len(locations)} faces. Need exactly 1. Try again.")
                continue
            enc = face_recognition.face_encodings(rgb, locations)[0]
            encodings.append(enc)
            print(f"Sample {len(encodings)} captured.")

    cap.release()
    cv2.destroyAllWindows()

    if len(encodings) < SAMPLES_NEEDED:
        print("Registration cancelled (not enough samples).")
        return

    mean_encoding = np.mean(encodings, axis=0)
    if add_user(name, roll_no, mean_encoding):
        print(f"User '{name}' ({roll_no}) registered. Encrypted vector stored, no photo saved.")
    else:
        print(f"Roll no '{roll_no}' already exists.")


if __name__ == "__main__":
    register_user()