import cv2
import mediapipe as mp 
import time 

class FaceMesh():
    def __init__(self, staticMode=False, maxFaces=5, minDetection=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetection = minDetection
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils 
        self.mpFaceMesh = mp.solutions.face_mesh 
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces )
        self.drawSpec = self.mpDraw.DrawingSpec( thickness=1, circle_radius=2 )

    def findMeshFaces(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec )
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    face.append([x,y])
                faces.append(face)
        return img, faces



def main():
    cap = cv2.VideoCapture("api/video/trump_ye_dinner.mp4")
    # cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceMesh()
    while True:
        success, img = cap.read()
        img, faces = detector.findMeshFaces(img)
        if len(faces)!= 0:
            print(len(faces))
        cTime = time.time()
        fps = 1 / ( cTime - pTime )
        cv2.putText(img, f'FPS: { int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3 )
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()