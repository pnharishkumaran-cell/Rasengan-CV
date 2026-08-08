import cv2
import mediapipe as mp
import math
import random
import numpy as np
time=0
charge=0
smooth_charge=0
mp_hands=mp.solutions.hands
hands=mp_hands.Hands()

mp_draw=mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)
while True:
    time+=0.15 + charge*0.15
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

            thumb_x=int(hand_landmarks.landmark[4].x*frame.shape[1])
            thumb_y=int(hand_landmarks.landmark[4].y*frame.shape[0])
                        
            index_x=int(hand_landmarks.landmark[8].x*frame.shape[1])
            index_y=int(hand_landmarks.landmark[8].y*frame.shape[0])
                        
            hand_distance=math.hypot(index_x-thumb_x,index_y-thumb_y)
                        
            charge=1-np.clip(hand_distance/100,0,1)
            smooth_charge=smooth_charge*0.8+charge*0.2
            charge=smooth_charge

            radius=40+int(5*math.sin(time))
            pulse_radius = radius + 6 +int(charge*8+3*math.sin(time*3))
            
            base_radius=radius
            radius=int(base_radius+charge*20)
    
            core_radius=radius+int(charge*6+2*math.sin(time+6))

            cv2.circle(frame,(cx,cy),radius+10,(120,60,0),-1)
            cv2.circle(frame,(cx,cy),radius+6,(180,120,50),-1)
            cv2.circle(frame,(cx,cy),core_radius+2,(255,200,100),-1)
            cv2.circle(frame,(cx,cy),core_radius,(255,120,40),-1)
            cv2.circle(frame,(cx,cy),int(radius*0.75),(255,180,120),-1)
            cv2.circle(frame,(cx,cy),int(radius*0.4),(255,255,220),-1)

            cv2.circle(frame,(cx,cy),pulse_radius,(25,180,80),1)



            colors=[
                (255,180,60),
                (255,150,40),
                (240,120,20),
                (220,90,10),
                (200,60,0),

            ]
            thumb_x=int(hand_landmarks.landmark[4].x*frame.shape[1])
            thumb_y=int(hand_landmarks.landmark[4].y*frame.shape[0])
            
            index_x=int(hand_landmarks.landmark[8].x*frame.shape[1])
            index_y=int(hand_landmarks.landmark[8].y*frame.shape[0])
            
            hand_distance=math.hypot(index_x-thumb_x,index_y-thumb_y)
            
            charge=1-np.clip(hand_distance/100,0,1)

            rotation_speed=2+charge*3

            trial_length=4+int(charge*8)

            base_radius=radius
            radius=int(base_radius+charge*20)
            


            for arm in range(3):
                for i in range(60):
                    inner_radius=radius+2+i*0.4
                    middle_radius=radius+8+i*0.45
                    outer_radius=radius+14+i*0.5
                
                    particle_size=max(1,int((4-i//10)+charge*2))

                    particle_color = colors[i%len(colors)]
                    arm_offset=arm*(2*math.pi/3)
                    inner_angle = (
                        time*(2.2+arm+0.08)+arm_offset+i*0.18
                    )

                    for i in range(3):
                        angle=time*rotation_speed+i*(2*math.pi/3)
                        for t in range(0,100,7):
                            r=(t/100)*radius
                            theta = angle +t * 0.08
                            x=int(cx+r*math.cos(theta))
                            y=int(cy+r*math.sin(theta))

                            cv2.circle(frame,(x,y),1,(255,170,70),-1)

                    inner_x=int(cx+inner_radius*math.cos(inner_angle))
                    inner_y=int(cy+inner_radius*math.sin(inner_angle))

                    inner_x+=random.randint(-1,1)
                    inner_y+=random.randint(-1,1)

                    trial_x = int(inner_x -trial_length*math.cos(inner_angle))
                    trial_y = int(inner_y -trial_length*math.sin(inner_angle))

                    cv2.line(frame,(trial_x,trial_y),(inner_x,inner_y),particle_color,1)
                    cv2.circle(frame,(inner_x,inner_y),particle_size,particle_color,-1) 

                    middle_angle=(time*1.5+arm_offset+i*0.35)

                    middle_x=int(cx+middle_radius*math.cos(middle_angle))
                    middle_y=int(cy+middle_radius*math.sin(middle_angle))

                    middle_x+=random.randint(-1,1)
                    middle_y+=random.randint(-1,1)

                    trial_x=int(middle_x-trial_length*math.cos(middle_angle))
                    trial_y=int(middle_y-trial_length*math.sin(middle_angle))

                    cv2.line(frame,(trial_x,trial_y),(middle_x,middle_y),particle_color,1)
                    cv2.circle(frame,(middle_x,middle_y),particle_size,particle_color,-1)

                    outer_angle=(time*0.9+arm_offset+i*0.35)

                    outer_x=int(cx+outer_radius*math.cos(outer_angle))
                    outer_y=int(cy+outer_radius*math.sin(outer_angle))

                    outer_x+=random.randint(-1,1)
                    outer_y+=random.randint(-1,1)

                    trial_x=int(outer_x-trial_length*math.cos(outer_angle))
                    trial_y=int(outer_y-trial_length*math.sin(outer_angle))
                    
                    cv2.line(frame,(trial_x,trial_y),(outer_x,outer_y),particle_color,1)
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