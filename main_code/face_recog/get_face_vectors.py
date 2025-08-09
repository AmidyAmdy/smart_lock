import cv2
import face_recognition


def get_vectors(img):
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)

    if len(face_locations) == 0:
        print(f"Лицо не найдено на изображении")
        return None, None, 1

    return face_locations, face_recognition.face_encodings(rgb_image, known_face_locations=face_locations)[0], 0
