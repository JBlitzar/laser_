import serial
import time
import numpy as np
import cv2

# # Replace with your ESP32 serial port
# ser = serial.Serial("/dev/cu.usbserial-0001", 115200, timeout=1)
# time.sleep(2)  # Wait for ESP32 to boot

# def move_servo(servo_id, angle):
#     assert servo_id in [1, 2], "Servo ID must be 1 or 2"
#     assert 0 <= angle <= 180, "Angle must be between 0 and 180"
#     cmd = f"S{servo_id}:{angle}\n"
#     ser.write(cmd.encode())
#     print(f"Sent: {cmd.strip()}")

# def move_zeroed(servo_id, angle):
#     if servo_id == 1:
#         zero_offset = 140
#     elif servo_id == 2:
#         zero_offset = 90
#     adjusted_angle = zero_offset + angle
#     move_servo(servo_id, adjusted_angle)

# def move_lr(angle):
#     move_zeroed(2, angle)
# def move_ud(angle):
#     move_zeroed(1, angle)


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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=10,
        maxRadius=100
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        darkest_circle = None
        min_brightness = float('inf')
        
        for (x, y, r) in circles:
            roi = gray[max(0, y-r//2):min(gray.shape[0], y+r//2), 
                max(0, x-r//2):min(gray.shape[1], x+r//2)]
            
            brightness = np.mean(roi) if roi.size > 0 else 255
            
            if roi.size > 0 and brightness < min_brightness:
                min_brightness = brightness
                darkest_circle = (x, y, r)
        
        if darkest_circle is not None:
            x, y, r = darkest_circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

