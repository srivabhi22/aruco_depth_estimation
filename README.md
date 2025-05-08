# **Aruco Depth Estimation**

This repository is designed for testing the **robotic arm of a quadruped**. It provides functionalities for both **tennis ball detection** and **Aruco marker depth estimation**.

---

## **Features**

### **1. Tennis Ball Detection:**

* Supports both **static** and **real-time** ball detection.
* Optimized for use with Raspberry Pi and Bookworm Debian version.

### **2. Aruco Marker Depth Estimation:**

* **Camera Calibration:** Uses chessboard images to perform accurate camera calibration.
* **Depth Estimation:** Extracts the distortion matrix and leverages it for precise depth measurement of Aruco markers.

---

## **Usage Instructions**

### **For Raspberry Pi with Bookworm Debian Version:**

This repository is primarily developed and tested on Raspberry Pi with the **Bookworm Debian** version.

### **To Use on Your PC:**

1. **Create a Virtual Environment:**

   ```bash
   python3 -m venv aruco_venv
   source aruco_venv/bin/activate
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program:**

   ```bash
   python path/to/your/script.py
   ```
