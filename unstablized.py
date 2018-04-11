import cv2
import numpy as np
import math

# cap = cv2.VideoCapture('traffic08560937.mp4')
cap = cv2.VideoCapture('tokyo23162321.mp4')

if not cap.isOpened():
    print("Error opening video stream or file")

width = 720
height = 1280
frameRate = cap.get(5)

result = np.empty([width, height, 3])

while cap.isOpened():
    ret, frame = cap.read()
    frameID = cap.get(1)

    if frameID % math.floor(frameRate / 2) == 0:
        print(frameID)

        for x in range(width):
            for y in range(height):
                # Y = 0.2126 R + 0.7152G + 0.0722B (ITU BT.709: http://www.itu.int/rec/R-REC-BT.709)
                Y = 0.2126 * frame[x, y, 2] + 0.7152 * frame[x, y, 1] + 0.0722 * frame[x, y, 0]
                reference_Y = 0.2126 * result[x, y, 2] + 0.7152 * result[x, y, 1] + 0.0722 * result[x, y, 0]

                if Y > reference_Y:
                    result[x, y, 0] = frame[x, y, 0]
                    result[x, y, 1] = frame[x, y, 1]
                    result[x, y, 2] = frame[x, y, 2]

    if not ret:
        break

# cv2.imwrite('unstabilized_manhattan_maximum_shutter.png', result)
cv2.imwrite('unstabilized_tokyo_maximum_shutter.png', result)

cap.release()
cv2.destroyAllWindows()
