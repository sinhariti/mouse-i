import cv2
import mediapipe as mp
import pyautogui
#mediapipe used for detecting the face
#cv2 helps in image processing
cam = cv2.VideoCapture(1)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks= True)
screen_w, screen_h = pyautogui.size()
while (True):
    _, frame = cam.read()
    frame= cv2.flip(frame,1)
    #frame the camera output area
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #^ it will change the video color to a different color
    output = face_mesh.process(rgb_frame)
    landmarks_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        #loop through the landmarks to draw points

        #we enumerated the landmarks to index the 4 points detected in the eye and now only one id
        #will be responsibile for the mouse moments, if all four landmarks are used then the mouse would be shaky
        for id,landmark in enumerate(landmarks[474:478]) :
            x= int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame,(x,y),2, (255,255,0))
            #cv2(where, center, radius of the circle, circle color )
            #initially without multiplying the frame width and height print(x,y)  fraction numbers are show
            # to draw on the image we need the pixel numbers

            #pyautogui work - to move the cursor according the commands given
            if id==1:
                #screen size and landmark point size wrt to the the video frame size should be proportionate
                screen_x = int(landmark.x * screen_w)
                screen_y = int(landmark.y * screen_h)
                pyautogui.moveTo(screen_x,screen_y)
            left = [landmarks[145],landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y-left[1].y)<0.005:
                pyautogui.click()
                pyautogui.sleep(1)
    cv2.imshow('Eye controlled Mouse', frame)
    cv2.waitKey(3)