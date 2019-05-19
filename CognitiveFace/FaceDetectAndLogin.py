import cv2
import sys
import time
import CognitiveFace.MicrosoftFaceRecognize as MFR
import winspeech
import CognitiveFace.FaceRecognitionConfig as FRC


def CaptureFaceAndStartRecognize():

    personGroupId = FRC.personGroupId
    cascPath = 'CognitiveFace/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)


    faceCounter = 0
    faceCounterThreshhold = 20

    FaceResultMessage = "Please hold still and look at the camera!"
    messageTextColor = (255, 255, 255)
    #userName = ""

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        k = cv2.waitKey(1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags=cv2.CV_HAAR_SCALE_IMAGE
        )

        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            #print(faceCounter)
            if faceCounter == faceCounterThreshhold:
                img_name = r"currentImage.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                
                global userName
                userName = MFR.DetectFaceMyImage(personGroupId,img_name)
                if userName != None:
                    #print(userName)
                    video_capture.release()
                    cv2.destroyAllWindows()
                    return userName
                else:
                    faceCounter = 0
                    FaceResultMessage = "Cannot Recognize you! Trying Again."
                    messageTextColor = (0,0,255)
            elif faceCounter > (faceCounterThreshhold-5):
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Please wait! Authenticating you.", (x-10, y-10),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, FaceResultMessage, (x-10, y-10),cv2.FONT_HERSHEY_PLAIN, 1, messageTextColor) 
            faceCounter = faceCounter + 1
        # Display the resulting frame
        cv2.imshow('Video', frame)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            img_name = "currentImage.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            
        #time.sleep(1)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

# authenticationOutput = CaptureFaceAndStartRecognize()

# if authenticationOutput == None:
#     sayString = f"Authentication failed."
# else:
#     sayString = f"Welcome {authenticationOutput}, Authentication successful."

# print(sayString)
# winspeech.say_wait(sayString)