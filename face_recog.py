
import face_recognition as fr
import cv2
import numpy as np
import os
from db import load_known_faces, check_in, create_table

create_table()

known_names, index_nums, known_name_encodings = load_known_faces()


def encode_image(img_path):
    image_loaded = fr.load_image_file(img_path)
    encodings = fr.face_encodings(image_loaded)
    
    if encodings:
        encoding = encodings[0].tobytes()
        
        return encoding

def recognize_faces(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(frame_rgb, model="hog")
    face_encodings = fr.face_encodings(frame_rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Check in the member if recognized
        if name:
            check_in(name, index_nums[best_match_index])
            # cursor.execute("INSERT INTO attendance (name) VALUES (?)", (name,))
            # conn.commit()

    return frame

def generate_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            frame = recognize_faces(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





# # path = "./train/"
# path = "./my_test/"

# known_names = []
# known_name_encodings = []

# images = os.listdir(path)
# for _ in images:
#     image = fr.load_image_file(path + _)
#     image_path = path + _
#     encoding = fr.face_encodings(image)[0]

#     known_name_encodings.append(encoding)
#     known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

# print(known_names)

# # test_image = "./test/test.jpg"
# test_image = "./my_test/p1.jpg"
# image = cv2.imread(test_image)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# face_locations = fr.face_locations(image)
# face_encodings = fr.face_encodings(image, face_locations)

# for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#     matches = fr.compare_faces(known_name_encodings, face_encoding)
#     name = ""

#     face_distances = fr.face_distance(known_name_encodings, face_encoding)
#     best_match = np.argmin(face_distances)

#     if matches[best_match]:
#         name = known_names[best_match]

#     cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
#     cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
#     font = cv2.FONT_HERSHEY_DUPLEX
#     cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


# cv2.imshow("Result", image)
# cv2.imwrite("./output.jpg", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
