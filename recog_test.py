
import os
import face_recognition
import cv2

image_path = "./my_test/favPic.jpg"

if not os.path.exists(image_path):
    raise ValueError(f"Image not found at Specified Path: {image_path}")

image = cv2.imread(image_path)

img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

img_rgb.astype('uint8')

# cv2.imshow("Converted Image", img_rgb)
# cv2.waitKey(0)

# print("Image Type: ", image.dtype)

face_location = face_recognition.face_locations(image)

for (top, right, bottom, left) in face_location:
        cv2.rectangle(image, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)

cv2.imshow('img',image)
cv2.waitKey(0)

print(face_location)