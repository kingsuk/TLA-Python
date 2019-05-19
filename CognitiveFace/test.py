import cv2
cap = cv2.VideoCapture(0)
while True:
    cv2.waitKey(10)

    ret, frame = cap.read()
    cap.set(3, 800)
    cap.set(4, 600)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) 
    print(cap.get(3)) # return default 1280       

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()