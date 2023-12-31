import cv2
import time 
import os 
import handModule as htm

wCam, hCam = 640, 480

cam = cv2.VideoCapture(0)
cam.set(3, wCam ) # width of cam 
cam.set(4, hCam) # height of cam

folderPath = "api/image"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)
tipIds = [ 4, 8, 12, 16, 20 ]

while True:
    success, img = cam.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    print(lmList)

    if len(lmList) != 0:
        fingers = []
        for id in range(0, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers = fingers.Count(1)
        print(totalFingers)

    h, w, c = overlayList[totalFingers-1].shape
    img[0:h, 0:w] = overlayList[totalFingers-1]

    cv2.rectangle(img, ( 20, 225), ( 170, 425), (0, 255, 0), cv2.FILLED )
    cv2.putText(img, str(totalFingers), (45, 375 ), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0,0), 25)

    cTime = time.time()
    fps = 1 / ( cTime - pTime )
    pTime = cTime

    cv2.putText(img, f'FPS: { int(fps)}', ( 400, 70, ), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)