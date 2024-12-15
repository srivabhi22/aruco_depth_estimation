# importing packages
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the static image
image_path = "tennis_ball.jpeg"  # Replace with the path to your image
frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

prevCircle = None  # Circle from the previous iteration (if needed)
dist = lambda x1, y1, x2, y2: (x1 - x2)**2 + (y1 - y2)**2

# Convert the image from BGR to GRAY
grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Apply blurring to reduce noise
blurFrame = cv2.GaussianBlur(grayFrame, ksize=(17, 17), sigmaX=0)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(
    blurFrame, 
    method=cv2.HOUGH_GRADIENT, 
    dp=1.2, 
    minDist=100, 
    param1=100, 
    param2=30, 
    minRadius=60, 
    maxRadius=200
)

if circles is not None:
    circles = np.uint16(np.around(circles))
    chosen = None
    for i in circles[0, :]:
        if chosen is None:
            chosen = i
        if prevCircle is not None:
            if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                chosen = i

    # Draw the selected circle
    cv2.circle(frame, center=(chosen[0], chosen[1]), radius=1, color=(0, 100, 100), thickness=3)
    cv2.circle(frame, center=(chosen[0], chosen[1]), radius=chosen[2], color=(0, 255, 0), thickness=3)
    prevCircle = chosen

# Display the result
cv2.imshow("Circles", frame)
cv2.waitKey(0)  # Wait indefinitely until a key is pressed
cv2.destroyAllWindows()

# Optionally save the output image
output_path = "output_image.jpg"  # Replace with your desired output path
cv2.imwrite(output_path, frame)
