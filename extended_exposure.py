import cv2
import numpy as np
import math

cap = cv2.VideoCapture('tokyo23162321.mp4')
# cap = cv2.VideoCapture('tube.mp4')
# cap = cv2.VideoCapture('road.mp4')
# cap = cv2.VideoCapture('stairs.mp4')

if not cap.isOpened():
    print("Error opening video stream or file")

width = int(cap.get(4))
height = int(cap.get(3))
frameRate = cap.get(5)
frameCount = cap.get(7)

result = np.empty([width, height, 3])

last_frame = np.empty([width, height, 1])

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

sum_of_weights = 0

while cap.isOpened():
    ret, frame = cap.read()
    frameID = cap.get(1)

    if frameID % math.floor(frameRate / 2) == 0:
    # if ret:
        print(frameID)
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()

        if last_frame.any():
            kp1, des1 = sift.detectAndCompute(current_frame, None)
            kp2, des2 = sift.detectAndCompute(last_frame, None)
            matches = flann.knnMatch(des1, des2, k=2)

            # ratio test as per Lowe's paper
            good = []
            for i, (m, n) in enumerate(matches):
                if m.distance < 0.7 * n.distance:
                    good.append(m)

            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            draw_params = dict(matchColor=(0, 255, 0),
                               singlePointColor=None,
                               matchesMask=matchesMask,
                               flags=2)

            match_frame = cv2.drawMatches(current_frame, kp1, last_frame, kp2, good, None, **draw_params)

            frame = cv2.warpPerspective(frame, M, (height, width))

            cv2.imshow("warped", frame)

            weight = 0.8 ** (30 * (frameCount - frameID) / (frameCount-math.floor(frameRate / 2)))

            for x in range(width):
                for y in range(height):
                    result[x, y, 0] += weight * frame[x, y, 0]
                    result[x, y, 1] += weight * frame[x, y, 1]
                    result[x, y, 2] += weight * frame[x, y, 2]

            sum_of_weights += weight

            last_frame = cv2.warpPerspective(current_frame, M, (height, width))
        else:
            last_frame = current_frame

    if not ret:
        break

for x in range(width):
    for y in range(height):
        result[x, y, 0] = result[x, y, 0] / sum_of_weights
        result[x, y, 1] = result[x, y, 1] / sum_of_weights
        result[x, y, 2] = result[x, y, 2] / sum_of_weights

cv2.imwrite('extended_exposure_tokyo.png', result)
# cv2.imwrite('extended_exposure_tube.png', result)
# cv2.imwrite('extended_exposure_road.png', result)
# cv2.imwrite('extended_exposure_stairs.png', result)

cap.release()
cv2.destroyAllWindows()
