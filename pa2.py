import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)
top, right, bottom, left = 100, 100, 500, 400
num_frames = 0


def background(ROI):
    # change color to grey
    grey = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (35, 35), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return threshold


def drawContour(threshold, video):
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        # find hand area
        cnt = max(contours, key=cv2.contourArea)
        cv2.drawContours(video, [cnt + (right, top)], -1, (0, 0, 255))
        hull = cv2.convexHull(cnt)
        cv2.drawContours(video, [hull + (right, top)], 0, (255, 0, 0), 0)
        cv2.imshow("Thesholded", threshold)

        return cnt


def CalculateAngle(cnt, video):
    hull = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull)

    num_def = 0
    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / np.pi

        if angle <= 90:
            num_def += 1

    return num_def


def printNumber(num_def):
    if num_def == 0:
        cv2.putText(video, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        # print(1)
    elif num_def == 1:
        cv2.putText(video, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        # print(2)
    elif num_def == 2:
        cv2.putText(video, "THREE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        # print(3)
    elif num_def == 3:
        cv2.putText(video, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        # print(4)
    elif num_def == 4:
        cv2.putText(video, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        # print(5)
    else:
        cv2.putText(video, "Can't count", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)


while (True):
    ret, video = cap.read()
    video = cv2.flip(video, 1)

    # define region of interest
    ROI = video[top:bottom, right:left]
    cv2.rectangle(video, (left, top), (right, bottom), (0, 255, 255), 2)

    # background
    threshold = background(ROI)

    # draw hand contour
    cnt = drawContour(threshold, video)

    num_frames += 1

    hull = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull)

    num_def = CalculateAngle(cnt, video)
    printNumber(num_def)

    cv2.imshow("Video", video)

    k = cv2.waitKey(10)
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
