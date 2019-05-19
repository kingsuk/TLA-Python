import numpy as np
import cv2
import os

cap = cv2.VideoCapture(0)
img_counter = 0


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    k = cv2.waitKey(1)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        path = r"C:\Users\accenture.robotics\Desktop\Python\Touchless-Automation\CognitiveFace\datasets\Kingsuk"
        if not os.path.exists(path):
            os.makedirs(path)
        img_name = r"opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(os.path.join(path , img_name), frame)
        print("{} written!".format(img_name))
        img_counter += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()