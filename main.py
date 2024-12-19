from time import sleep
import tkinter as tk
from tkinter import StringVar, OptionMenu, Label
import cv2
from djitellopy import Tello
from PIL import Image, ImageTk
import threading

drone = Tello()

# Key states
key_states = {
    "w": False,
    "s": False,
    "a": False,
    "d": False,
    "Left": False,
    "Right": False,
    "space": False,
    "Control_L": False,
}

# Function to process and display Tello's video feed in the Tkinter window
def processTelloVideo(drone, video_label):
    def update_video():
        frame = drone.get_frame_read().frame
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Congert BGR to RGB
        img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.imgtk = img
        video_label.configure(image=img)
        video_label.after(10, update_video)

    update_video()

# Function to initialize the drone and its video stream
def startDrone(video_label):
    drone.connect()
    drone.streamon()
    processTelloVideo(drone, video_label)

# Function for drone takeoff
def takeOff(drone):
    drone.takeoff()

# Function for drone landing
def landDrone(drone):
    drone.land()

# Function to update drone movement
def updateDroneMovement():
    speed = 50
    lr, fb, ud, yv = 0, 0, 0, 0
    if key_states["w"]:
        fb = speed
    elif key_states["s"]:
        fb = -speed
    elif key_states["a"]:
        lr = -speed
    elif key_states["d"]:
        lr = speed
    elif key_states["Left"]:
        yv = -speed
    elif key_states["Right"]:
        yv = speed
    elif key_states["space"]:
        ud = speed
    elif key_states["Control_L"]:
        ud = -speed

    return [lr, fb, ud, yv]

# Function to disable keyboard controls
def disableKeyboard():
    for key in key_states:
        key_states[key] = False

# Functions to handle key press and release events
def onKeyPress(event):
    if event.keysym in key_states:
        key_states[event.keysym] = True

def onKeyRelease(event):
    if event.keysym in key_states:
        key_states[event.keysym] = False

# Function for a pre-programmed planned flight
def plannedFlight(start_button, window):
    start_button.config(state="disabled")  # Disable the start button
    disableKeyboard()  # Disable keyboard controls
    try:
        drone.takeoff()
        drone.move_forward(300)
        drone.move_up(150)
        drone.move_left(50)
        drone.move_up(100)
        drone.flip_back()
        drone.move_down(50)
        drone.move_back(75)
        drone.land()
    except Exception as e:
        print(f"Error during planned flight: {e}")
    finally:
        start_button.config(state="normal")  # Re-enable the start button
        print("Planned flight complete!")

# Function to update battery and flight time
def updateBatteryAndTime(battery_label, time_label):
    try:
        battery = drone.get_battery()
        flight_time = drone.get_flight_time()
        battery_label.config(text=f"Battery: {battery}%")
        time_label.config(text=f"Flight Time: {flight_time} seconds")
    except Exception as e:
        print(f"Failed to fetch battery or flight time: {e}")
    battery_label.after(1000, updateBatteryAndTime, battery_label, time_label)

# Function to change instructions text
def instructionsText(mode):
    if mode == "Keyboard Control":
        return "Drone Controls:\n W: Forward | S: Backward\n A: Left    | D: Right\n Left Arrow: Rotate CCW | Right Arrow: Rotate CW\n Space: Up  |  Ctrl: Down"
    elif mode == "Cool Pre-Programmed Flight":
        return "MAKE SURE YOU HAVE PLENTY OF OPEN SPACE. YOU WILL NOT BE ABLE TO CONTROL THE DRONE ONCE YOU HIT START"

# Function to dynamically update instructions and buttons
def updateModeUI(window, mode_var, instructions_label, start_button_placeholder):
    mode = mode_var.get()
    instructions_label.config(text=instructionsText(mode))

    # Clear previous button
    for widget in start_button_placeholder.winfo_children():
        widget.destroy()

    # Add "Start Planned Flight" button if in pre-programmed flight mode
    if mode == "Cool Pre-Programmed Flight":
        start_button = tk.Button(
            start_button_placeholder, text="Start Planned Flight",
            command=lambda: plannedFlight(start_button, window)
        )
        start_button.pack()


# Function to take a photo
def takePhoto():
    try:
        frame = drone.get_frame_read().frame
        if frame is not None:
            file_path = "photo123.jpg"
            cv2.imwrite(file_path, frame)
            print(f"Photo saved as {file_path}")
    except Exception as e:
        print(f"Error taking photo: {e}")



# Create the User Interface
def createApp():
    window = tk.Tk()
    window.title("Tello Control Screen")

    # Control modes
    controlMode = ["Keyboard Control", "Cool Pre-Programmed Flight"]
    selectedMode = StringVar()
    selectedMode.set(controlMode[0])

    # Dropdown for control modes
    dropdown = OptionMenu(window, selectedMode, *controlMode)
    dropdown.pack(pady=20)

    # Video feed label
    video_label = tk.Label(window)
    video_label.pack(pady=20)

    # Battery and flight time labels
    battery_label = tk.Label(window, text="Battery: N/A")
    battery_label.pack()
    time_label = tk.Label(window, text="Flight Time: N/A")
    time_label.pack()

    # Frame for buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Start Drone", command=lambda: startDrone(video_label)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Takeoff", command=lambda: takeOff(drone)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Land", command=lambda: landDrone(drone)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Take Photo", command=takePhoto).pack(side="left", padx=10)

    # Instructions label
    instructions_label = tk.Label(window, text=instructionsText(selectedMode.get()), justify="left", padx=10, pady=10)
    instructions_label.pack()

    # Placeholder for the Start Planned Flight button
    start_button_placeholder = tk.Frame(window)
    start_button_placeholder.pack()

    # Update UI when mode changes
    selectedMode.trace("w", lambda *args: updateModeUI(window, selectedMode, instructions_label, start_button_placeholder))

    # Bind keyboard keys
    window.bind("<KeyPress>", onKeyPress)
    window.bind("<KeyRelease>", onKeyRelease)

    # Start updating battery and flight time
    updateBatteryAndTime(battery_label, time_label)

    # Main loop to send drone controls
    def movement_loop():
        while True:
            values = updateDroneMovement()
            drone.send_rc_control(values[0], values[1], values[2], values[3])
            sleep(0.05)

    threading.Thread(target=movement_loop, daemon=True).start()
    window.mainloop()

if __name__ == "__main__":
    createApp()
