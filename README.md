# Smart Attendance System (Face Recognition)

## Setup
python -m venv venv
venv\Scripts\activate        (Windows)  |  source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt

## Run (in this order)
1. python register.py      -> register each person (press 'c' 5 times)
2. python face_utils.py    -> live recognition, marks attendance automatically
3. python app.py           -> admin dashboard at http://127.0.0.1:5000  (admin / admin123)
