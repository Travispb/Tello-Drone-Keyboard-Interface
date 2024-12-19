# 🚁 **Tello Drone Keyboard Interface**

This project allows you to control your Tello Drone using a keyboard interface. 🕹️  

## 📋 **Setup Instructions**

To get started, ensure you have the required dependencies installed. Use the following commands in your terminal:

```bash
pip install tellopy
pip install av
pip install opencv-python
pip install image
pip install djitellopy
```

---

## 📦 **Dependencies**

- `tellopy` - To interface with the Tello Drone.  
- `av` - Handles video decoding and processing.  
- `opencv-python` - For image processing and video stream visualization.  
- `image` - Additional image handling tools.  
- `djitellopy` - Simplifies drone communication and control.

---

## 🚀 **How to Run**

1. Install the dependencies listed above.  
2. Connect your Tello Drone to your Wi-Fi.  
3. Run the script using Python:

   ```bash
   python main.py
   ```

4. Control the drone with your keyboard and enjoy the flight! 🎮

---

## **Keyboard Controls**

| Key             | Action                  |
|-----------------|-------------------------|
| `W`            | Move forward            |
| `S`            | Move backward           |
| `A`            | Move left               |
| `D`            | Move right              |
| `SPACE`        | Ascend                  |
| `L-CONTROL`    | Descend                 |
| `LEFT ARROW`   | Rotate counterclockwise |
| `RIGHT ARROW`  | Rotate clockwise        |

---

## 🛠️ **Troubleshooting**

- **Issue:** Unable to connect to the drone.  
  **Solution:** Ensure the drone is powered on and connected to your Wi-Fi.  

- **Issue:** Missing dependencies.  
  **Solution:** Re-run the setup commands to ensure all packages are properly installed.

---

## 💡 **Features**

- Full keyboard-based control of the Tello Drone.  
- Real-time video feed (via OpenCV).  

---

## 🤝 **Contributions**

Contributions are welcome! Fork this repository, make your changes, and submit a pull request.  

---
