import cv2 
import poseModule as pm
import time

def main():
    cap = cv2.VideoCapture("")
    pTime = 0
    detector = pm.poseDetector()
    while True:
        success, img = cap.read()
        detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList !=0 ):
          print(lmList)
          cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0,0, 250), cv2.FILLED )
        cTime = time.time()
        fps = 1 / ( cTime - pTime )
        pTime = cTime 

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, ( 255, 0, 0), 3 )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()