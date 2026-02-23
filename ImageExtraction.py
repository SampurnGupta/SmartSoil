import serial
import time
import os

# User settings
SERIAL_PORT = 'COM7'    # <-- Change this to your COM port
BAUD_RATE = 115200
TIMEOUT = 10  # seconds
# timeout defines how long (in seconds) the Python script will keep waiting for data from ESP32-CAM.
# If there is no new data for 10 seconds, it assumes the transfer is finished and stops reading.
SAVE_FOLDER = "captured_images"  # Folder to save images

IMAGE_INTERVAL = 10  # Interval between saving images in seconds
INACTIVITY_TIMEOUT = 60  # Timeout after 1 minute of inactivity

# Make sure the save folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
print("Waiting for ESP32-CAM to send data...")

image_data = b''
last_received_time = time.time()  # Track the last received time
start_time = time.time()  # Start time to check inactivity timeout
last_saved_time = time.time()  # Track the last time an image was saved

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            image_data += data
            last_received_time = time.time()  # Update last received time
            print("Data received, waiting for end marker...")

        # Check if "###END###" signal is received, indicating end of image data
        if b"###END###" in image_data:
            print("End of image data received.")
            # Remove the "###END###" signal before saving the image
            image_data = image_data.replace(b"###END###", b"")

            # Save the image as latest.jpg (replacing the previous one) after IMAGE_INTERVAL
            if time.time() - last_saved_time >= IMAGE_INTERVAL:
                if image_data:
                    filename = "latest.jpg"  # Always save as latest.jpg
                    filepath = os.path.join(SAVE_FOLDER, filename)
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    print(f"Image saved as {filepath}")
                    last_saved_time = time.time()  # Update the last saved time

            image_data = b''  # Reset image data after saving

        # Check if 5 minutes of inactivity have passed
        if time.time() - last_received_time >= INACTIVITY_TIMEOUT:
            print("No data received for 5 minutes. Terminating...")
            break

except Exception as e:
    print(f"Error: {e}")

ser.close()
