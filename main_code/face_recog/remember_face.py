import cv2
from db_scripts.db_scripts import add_to_db
import numpy as np
from face_recog.get_face_vectors import get_vectors
import os

def remember_face(name):
    vectors = []
    print("Текущий рабочий каталог:", os.getcwd())

    for i in range(1, 4):
        photo_files = [f for f in os.listdir(f'photos/{name}') if f.lower().endswith('.jpg')]
        for photo in photo_files:
            with open(f"photos/{name}/{photo}", "rb") as f:
                img_bytes = f.read()
            img_np = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            _, vector, _ = get_vectors(img)
            vectors.append(vector)

    face_encoding = np.mean(vectors, axis = 0)

    add_to_db(name, face_encoding.tolist())

    print("Вектор лица успешно сохранён")
