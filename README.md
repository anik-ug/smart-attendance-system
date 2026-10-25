# Smart Attendance System (Face Recognition)

A privacy-first attendance system that marks attendance automatically using face recognition.
Only an **encrypted numerical face vector** is stored. No face photo is ever saved.

## Features

- Face registration with consent prompt (5 samples averaged into one 128-D vector)
- Live face recognition through webcam (HOG detector + dlib ResNet encoding)
- Automatic attendance marking, one entry per user per day
- Face vectors stored **encrypted** (Fernet / AES) in SQLite, no images on disk
- Admin dashboard: login, filter by date/user, export CSV
- Offline processing, no third-party server or API

## Tech Stack

Python 3.11, OpenCV, face_recognition (dlib), NumPy, Flask, SQLite, pandas, cryptography

## Project Structure

```
smart-attendance-system/
├── app.py            # Flask admin dashboard
├── database.py       # SQLite functions (users, attendance)
├── crypto_utils.py   # Encrypt / decrypt face vectors
├── face_utils.py     # Live recognition + attendance marking
├── register.py       # Consent + capture + store encrypted vector
├── show_db.py        # Demo: shows what is actually stored
├── templates/        # login.html, dashboard.html
├── dataset/          # kept empty (no photos are stored)
└── requirements.txt
```

## Setup (macOS / Linux)

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install cmake
pip install -r requirements.txt
pip install "setuptools<81"
```

Windows: use `venv\Scripts\activate` instead of `source venv/bin/activate`.

Note: Python 3.11 is recommended, because dlib may fail to build on very new Python versions.
On macOS, allow camera access for your terminal / VS Code when prompted.

## Usage (run in this order)

1. Register a user (consent `y`, name, roll no, press `c` 5 times):
```bash
   python register.py
```
2. Start live recognition (press `q` in the camera window to quit):
```bash
   python face_utils.py
```
3. Start the admin dashboard and open http://127.0.0.1:5000 (default login: `admin` / `admin123`):
```bash
   python app.py
```
4. Check what is stored in the database:
```bash
   python show_db.py
```

## Privacy and Security

- Consent is asked before registration.
- Only a 128-number face vector is stored, never a photo (`dataset/` stays empty).
- The vector is encrypted before it is written to `attendance.db` (column `users.encoding`).
- The encryption key is in `secret.key`. **Never commit or share this file.**
- All processing is local and offline.
- Limitation: a face vector is still biometric data. The key currently sits next to the database;
  in production it should be in an environment variable or a key vault.

## Known Limitations

- No liveness detection, so a printed photo or video can fool the system.
- Accuracy drops in low light, extreme angles and with masks.
- Admin credentials are hardcoded for the demo; change them before any real use.

## Future Scope (Major Project)

Liveness / anti-spoofing, geofencing, analytics dashboard, edge deployment (Raspberry Pi / Jetson),
FAR / FRR / EER evaluation, key management with a vault, absent list and reports.