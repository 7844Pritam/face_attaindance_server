import os
import face_recognition
from werkzeug.utils import secure_filename

DATASET_PATH = './attendance_faces'
# khgjgj
def load_known_faces(path=DATASET_PATH):
    encodings, names = [], []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                img_path = os.path.join(root, file)
                img = face_recognition.load_image_file(img_path)
                enc = face_recognition.face_encodings(img)
                if enc:
                    encodings.append(enc[0])
                    names.append(os.path.basename(root))
    return encodings, names

def recognize_face(uploaded_file, known_faces, known_names, threshold=0.45):
    try:
        img = face_recognition.load_image_file(uploaded_file)
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            return None

        face_encoding = encodings[0]
        face_distances = face_recognition.face_distance(known_faces, face_encoding)

        if not face_distances.any():
            return None

        best_match = face_distances.argmin()
        if face_distances[best_match] < threshold:
            confidence = round((1 - face_distances[best_match]) * 100, 2)
            return known_names[best_match], confidence
        else:
            return None
    except Exception as e:
        print(f"[ERROR] recognize_face: {e}")
        return None

def save_new_employee(name, image_file):
    try:
        folder = os.path.join(DATASET_PATH, name)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, secure_filename(image_file.filename))
        image_file.save(path)
        return True
    except Exception as e:
        print(f"[ERROR] save_new_employee: {e}")
        return False
