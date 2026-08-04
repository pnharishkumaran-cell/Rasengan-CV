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
            radius=35+int(5*math.sin(time))

            cv2.circle(frame,(cx,cy),radius+15,(255,150,50),2)
            cv2.circle(frame,(cx,cy),radius+8,(255,50,0),2)


            cv2.circle(frame,(cx,cy),radius,(255,0,0),-1)
            
            inner_radius=radius+8
            middle_radius=radius+16
            outer_radius=radius+24

            for i in range(60):
                particle_size=1+(i%3)
                inner_angle=(time*(1+i*0.05))+i*(2*math.pi/60)

                inner_x=int(cx+inner_radius*math.cos(inner_angle))
                inner_y=int(cy+inner_radius*math.sin(inner_angle))
                cv2.circle(frame,(inner_x,inner_y),particle_size,(255,255,255))

                middle_angle=(time*0.7)+i*(2*math.pi/60)

                middle_x=int(cx+middle_radius*math.cos(middle_angle))
                middle_y=int(cy+middle_radius*math.sin(middle_angle))

                cv2.circle(frame,(middle_x,middle_y),particle_size,(255,200,100),-1)

                outer_angle=(time*0.4)+i*(2*math.pi/60)

                outer_x=int(cx+outer_radius*math.cos(outer_angle))
                outer_y=int(cy+outer_radius*math.sin(outer_angle))

                cv2.circle(frame,(outer_x,outer_y),particle_size,(255,150,50),-1)
    
            
    cv2.imshow("Rasengan CV",frame)

    if cv2.waitKey(1) == ord("q"):
        break     


camera.release()
cv2.destroyAllWindows()