import cv2
import face_recognition
import numpy as np
from .get_face_vectors import get_vectors
from db_scripts.db_scripts import get_from_db

def face_check(frame):
    faces = get_from_db()
    known_vectors = np.array([face[1] for face in faces])

    face_locations, vector, flag = get_vectors(frame)

    if flag:
        return False

    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    results = face_recognition.compare_faces(known_vectors, vector, tolerance=0.6)
    if any(results):
        return True
    else:
        return False