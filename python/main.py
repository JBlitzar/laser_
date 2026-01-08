import serial
import time
import numpy as np
import cv2

# Replace with your ESP32 serial port
ser = serial.Serial("/dev/cu.usbserial-0001", 115200, timeout=1)
time.sleep(2)  # Wait for ESP32 to boot

def move_servo(servo_id, angle):
    assert servo_id in [1, 2], "Servo ID must be 1 or 2"
    assert 0 <= angle <= 180, "Angle must be between 0 and 180"
    cmd = f"S{servo_id}:{angle}\n"
    ser.write(cmd.encode())
    print(f"Sent: {cmd.strip()}")

def move_zeroed(servo_id, angle):
    if servo_id == 1:
        zero_offset = 140
    elif servo_id == 2:
        zero_offset = 90
    adjusted_angle = zero_offset + angle
    move_servo(servo_id, adjusted_angle)

def move_lr(angle):
    move_zeroed(2, angle)
def move_ud(angle):
    move_zeroed(1, angle)


# # # ZERO ANGLES: 150 for servo 1, 70 for servo 2
# # move_servo(1, 140) # tilt up/down servo
# # move_servo(2, 180) # left/right servo

# # move_servo(2, 70+45) 

# move_lr(0)
# move_ud(0)
# move_lr(45)

# def angle_to_servo(angle):
#     return int((angle + 90)/2)



cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.equalizeHist(frame)
    
    thresh = np.percentile(frame, 10)
    frame_mask = frame < thresh
    cnt = cv2.findContours(frame_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    # Find most circular contour
    most_circular = None
    max_circularity = 0
    for contour in cnt:
        area = cv2.contourArea(contour)
        if area < 100:  # Skip very small contours
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter ** 2)
        if circularity > max_circularity:
            max_circularity = circularity
            most_circular = contour
    
    largest_coords = most_circular[:, 0, :] if most_circular is not None else np.array([[0,0]])
    if most_circular is not None:
        for x, y in largest_coords:
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
    cv2.imshow("Frame", frame.astype(np.uint8)*255)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    x_coord = int(np.mean(largest_coords[:, 0])) / frame.shape[1]
    h_fov = 60 # degrees

    angle = (x_coord - 0.5) * h_fov
    servo_angle = int((angle + 90)/2)
    print(f"X Coord: {x_coord:.2f}, Angle: {angle:.2f}, Servo Angle: {servo_angle}")
    move_lr(servo_angle)