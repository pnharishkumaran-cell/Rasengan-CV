import cv2
import mediapipe as mp
import math
time=0

mp_hands=mp.solutions.hands
hands=mp_hands.Hands()

mp_draw=mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)
while True:
    time+=0.2
    success, frame=camera.read()
    if not success:
        break
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h,w,_=frame.shape
            palm_points=[0,5,9,13,17]
            sum_x =0
            sum_y =0
            for point in palm_points:
                landmark=hand_landmarks.landmark[point]

                sum_x+=landmark.x
                sum_y+=landmark.y
            cx =int((sum_x/len(palm_points))*w)
            cy =int((sum_y/len(palm_points))*h)
            radius=25+int(5*math.sin(time))

            cv2.circle(frame,(cx,cy),radius+15,(255,150,50),2)
            cv2.circle(frame,(cx,cy),radius+8,(255,50,0),2)


            cv2.circle(frame,(cx,cy),radius,(255,0,0),-1)
            
            orbit_radius=radius+12

            for i in range(60):
                angle=time+(i*(2*math.pi/40))

                particle_x=int(cx+orbit_radius*math.cos(angle))
                particle_y=int(cy+orbit_radius*math.sin(angle))
                cv2.circle(frame,(particle_x,particle_y),1,(255,255,255))
    
            
    cv2.imshow("Rasengan CV",frame)

    if cv2.waitKey(1) == ord("q"):
        break     


camera.release()
cv2.destroyAllWindows()