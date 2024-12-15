# importing packages
import numpy as np
import matplotlib.pyplot as plt
import cv2

videoCapture = cv2.VideoCapture(0)
prevCircle = None # circle from the previous frame that represents current circle in the frame
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

# checking if the video capture device is opened properly
while True:
    ret, frame = videoCapture.read()
    if not ret:
        break
    
    # converting to frame from BGR to GRAY
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # applying blurring to get rid of noise (if any)
    blurFrame = cv2.GaussianBlur(grayFrame, ksize=(17,17), sigmaX=0)

    # applying hough circle transform
    circles = cv2.HoughCircles(blurFrame, method=cv2.HOUGH_GRADIENT, dp=1.2, 
                               minDist=100, param1=100, param2=30, minRadius=60, maxRadius=200)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None:
                chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                   chosen = i 

        cv2.circle(frame, center=(chosen[0],chosen[1]), radius=1, color=(0,100,100), thickness=3)
        cv2.circle(frame, center=(chosen[0],chosen[1]), radius=chosen[2], color=(0,255,0), thickness=3)
        prevCircle = chosen

    cv2.imshow("circles", frame)    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

videoCapture.release()
cv2.destroyAllWindows()