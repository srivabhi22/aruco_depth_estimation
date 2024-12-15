import cv2
import numpy as np

# Load the image
image_path = "images.png"  # Replace with the path to your image
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image at path {image_path} not found!")

# Convert to grayscale (required for ArUco detection)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

# Load the predefined dictionary of ArUco markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)  # Choose an appropriate dictionary
parameters = cv2.aruco.DetectorParameters()

# Detect ArUco markers
corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

# Draw the detected markers on the image
if ids is not None:
    print("Detected ArUco markers:")
    for marker_id, corner in zip(ids.flatten(), corners):
        print(f"ID: {marker_id}, Corners: {corner}")
        # Draw a box around the detected marker
        cv2.aruco.drawDetectedMarkers(image, corners, ids)
else:
    print("No ArUco markers detected.")
    for candidate in rejected:
        for corner in candidate:
            # Draw a polygon around each rejected candidate
            cv2.polylines(image, [corner.astype(int)], isClosed=True, color=(0, 0, 255), thickness=2)


# Display the image with detected markers
cv2.imshow("Detected ArUco Markers", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
