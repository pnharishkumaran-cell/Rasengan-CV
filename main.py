import cv2
import mediapipe as mp
import math
import random
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
            radius=40+int(5*math.sin(time))

            cv2.circle(frame,(cx,cy),radius+10,(120,60,0),-1)
            cv2.circle(frame,(cx,cy),radius+6,(180,120,50),-1)
            cv2.circle(frame,(cx,cy),radius+2,(255,200,100),-1)
            cv2.circle(frame,(cx,cy),radius,(255,120,40),-1)
            cv2.circle(frame,(cx,cy),int(radius*0.75),(255,180,120),-1)
            cv2.circle(frame,(cx,cy),int(radius*0.4),(255,255,220),-1)



            colors=[
                (255,180,60),
                (255,150,40),
                (240,120,20),
                (220,90,10),
                (200,60,0),

            ]

            for arm in range(4):
                for i in range(60):
                    inner_radius=radius+2+i*0.4
                    middle_radius=radius+8+i*0.45
                    outer_radius=radius+14+i*0.5
                
                    particle_size=max(1,4-i//10)

                    particle_color = colors[i%len(colors)]
                    arm_offset=arm*(2*math.pi/4)
                    inner_angle = (
                        time*2.2+arm_offset+i*0.35
                    )

                    inner_x=int(cx+inner_radius*math.cos(inner_angle))
                    inner_y=int(cy+inner_radius*math.sin(inner_angle))

                    inner_x+=random.randint(-1,1)
                    inner_y+=random.randint(-1,1)

                    trial_x = int(inner_x -10*math.cos(inner_angle))
                    trial_y = int(inner_y -10*math.sin(inner_angle))

                    cv2.line(frame,(trial_x,trial_y),(inner_x,inner_y),particle_color,1)
                    cv2.circle(frame,(inner_x,inner_y),particle_size,particle_color,-1) 

                    middle_angle=(time*1.5+arm_offset+i*0.35)

                    middle_x=int(cx+middle_radius*math.cos(middle_angle))
                    middle_y=int(cy+middle_radius*math.sin(middle_angle))

                    middle_x+=random.randint(-1,1)
                    middle_y+=random.randint(-1,1)

                    trial_x=int(middle_x-10*math.cos(middle_angle))
                    trial_y=int(middle_y-10*math.sin(middle_angle))

                    cv2.line(frame,(trial_x,trial_y),(middle_x,middle_y),particle_color,1)
                    cv2.circle(frame,(middle_x,middle_y),particle_size,particle_color,-1)

                    outer_angle=(time*0.9+arm_offset+i*0.35)

                    outer_x=int(cx+outer_radius*math.cos(outer_angle))
                    outer_y=int(cy+outer_radius*math.sin(outer_angle))

                    outer_x+=random.randint(-1,1)
                    outer_y+=random.randint(-1,1)

                    cv2.circle(frame,(outer_x,outer_y),particle_size,particle_color,-1)

                    for angle in range(0,360,15):
                        theta = math.radians(angle)+time*2

                        ring_x = int(cx+(radius+18)*math.cos(theta))
                        ring_y = int(cy+(radius+8)*math.sin(theta))

                        cv2.circle(frame,(ring_x,ring_y),2,(255,170,60),-1)

                    

            
    cv2.imshow("Rasengan CV",frame)

    if cv2.waitKey(1) == ord("q"):
        break     


camera.release()
cv2.destroyAllWindows()