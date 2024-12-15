import cv2
import numpy as np

# load in the calibration data
calib_data_path = r"OpenCV\Distance Estimation\calib_data\MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 6  # centimeters (measure your printed marker size)

# Load ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
aruco_params = cv2.aruco.DetectorParameters()

# Initialize the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

def estimate_pose_and_distance(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        # Define 3D points of the marker corners (assuming Z = 0, center origin)
        obj_points = np.array([
            [-MARKER_SIZE / 2,  MARKER_SIZE / 2, 0],
            [ MARKER_SIZE / 2,  MARKER_SIZE / 2, 0],
            [ MARKER_SIZE / 2, -MARKER_SIZE / 2, 0],
            [-MARKER_SIZE / 2, -MARKER_SIZE / 2, 0]
        ], dtype=np.float32)

        # Iterate through each marker
        for i in range(len(ids)):
            # SolvePnP for pose estimation
            _, rvecs, tvecs = cv2.solvePnP(
                obj_points, corners[i][0], cam_mat, dist_coef
            )

            # Draw axis and marker
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, cam_mat, dist_coef, rvecs, tvecs, 0.03)

            # Extract translation vector
            tvec = tvecs.ravel()  # Flatten the vector
            distance = np.linalg.norm(tvec)  # Distance in meters

            # Display distance on the marker
            text = f"ID: {ids[i][0]}, Dist: {distance:.2f}m"
            cv2.putText(frame, text, tuple(corners[i][0][0].astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(f"Marker ID: {ids[i][0]}, Distance: {distance:.2f} meters")
    else:
        print("No markers detected")

    return frame



# Main function
def main():
    cap = cv2.VideoCapture(0)  # Replace with video file path if needed

    if not cap.isOpened():
        print("Error: Cannot access camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            break

        # Estimate pose and distance
        frame = estimate_pose_and_distance(frame)

        # Display the output
        cv2.imshow("Pose and Distance Estimation", frame)

        # Exit with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
