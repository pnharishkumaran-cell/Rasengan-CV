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
smooth_cx =None
smooth_cy=None
charge_start_time = None
rasenshuriken=False

mp_draw=mp.solutions.drawing_utils
rotation_time=0

camera = cv2.VideoCapture(0)
while True:
    rotation_time+=0.15
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

            if smooth_cx is None:
                smooth_cx=cx
                smooth_cy=cy
            else:

                smooth_cx=smooth_cx*0.8+cx*0.2
                smooth_cy=smooth_cy*0.8+cy*0.2


            thumb_x=int(hand_landmarks.landmark[4].x*frame.shape[1])
            thumb_y=int(hand_landmarks.landmark[4].y*frame.shape[0])
                        
            index_x=int(hand_landmarks.landmark[8].x*frame.shape[1])
            index_y=int(hand_landmarks.landmark[8].y*frame.shape[0])
                        
            hand_distance=math.hypot(index_x-thumb_x,index_y-thumb_y)
                        
            charge=1-np.clip(hand_distance/100,0,1)
            smooth_charge=smooth_charge*0.8+charge*0.2
            charge=smooth_charge

            if charge > 0.65:
                if charge_start_time is None:
                    charge_start_time=time

                if time-charge_start_time >=7:
                    rasenshuriken=True
            else:
                charge_start_time=None
                rasenshuriken=False

            fully_charged = charge>0.75

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

            if rasenshuriken:
                shuruken_radius=radius+25
                tilt=0.45
                side_angle=math.radians(8)
                orbit_angle=math.radians(15)
                glow_layer=np.zeros_like(frame)

                for i in range(4):
                    depth=math.cos(angle)
                    angle=rotation_time*6+i*(math.pi/2)
                    fast_angle=rotation_time*10+i*(math.pi/2)

                    fast_x=math.cos(fast_angle)*(radius+160)
                    fast_y=math.sin(fast_angle)*(radius+160)*tilt

                    fast_rot_x=fast_x*math.cos(orbit_angle)-fast_y*math.sin(orbit_angle)
                    fast_rot_y=fast_x*math.sin(orbit_angle)-fast_y*math.cos(orbit_angle)

                    fast_tip_x=int(cx+fast_rot_x)
                    fast_tip_y=int(cy+fast_rot_y)

                  

                    cv2.line(frame,(cx,cy),(fast_tip_x,fast_tip_y),(255,200,100),3)

                   

                    brightness=0.45+0.55*((depth+1)/2)


                    x=math.cos(angle)*(radius+220)
                    y=math.sin(angle)*(radius+220)*tilt

                    rot_x=x*math.cos(orbit_angle)-y*math.sin(orbit_angle)
                    rot_y=x*math.sin(orbit_angle)+y*math.cos(orbit_angle)

                    tip_x = int(cx+rot_x)
                    tip_y = int(cy+rot_y)

                    side_angle = 0.35

                    x=math.cos(angle+side_angle)*(radius+8)
                    y=math.sin(angle+side_angle)*(radius+8)*tilt

                    rot_x=x*math.cos(orbit_angle)-y*math.sin(orbit_angle)
                    rot_y=x*math.sin(orbit_angle)+y*math.cos(orbit_angle)

                    left_x=int(cx+rot_x)
                    left_y=int(cy+rot_y)

                    x=math.cos(angle-side_angle)*(radius+8)
                    y=math.sin(angle-side_angle)*(radius+8)*tilt

                    rot_x=x*math.cos(orbit_angle)-y*math.sin(orbit_angle)
                    rot_y=x*math.sin(orbit_angle)+y*math.cos(orbit_angle)

                    right_x=int(cx+rot_x)
                    right_y=int(cy+rot_y)

                    x=math.cos(angle)*(radius+45)
                    y=math.sin(angle)*(radius+45)*tilt

                    rot_x=x*math.cos(orbit_angle)-y*math.sin(orbit_angle)
                    rot_y=x*math.sin(orbit_angle)+y*math.cos(orbit_angle)

                    inner_x=int(cx+rot_x)
                    inner_y=int(cy+rot_y)

                    points=np.array([
                        (tip_x,tip_y),
                        (left_x,left_y),
                        (inner_x,inner_y),
                        (right_x,right_y)
                    ],np.int32)

                  

                    cv2.fillPoly(frame,[points],(int(255*brightness),int(220*brightness),int(120*brightness)))
                    cv2.polylines(frame,[points],True,(255,240,180),2)
                 


                glow=np.zeros_like(frame)
                cv2.fillPoly(glow,[points],[255,140,30])
                glow=cv2.GaussianBlur(glow,(15,15),0)
                frame=cv2.addWeighted(frame,1.0,glow,0.18,0)
                
                    
             


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
                
                    particle_size=max(1,int((4-i//10)+charge*2+math.sin(time*5+i)*0.7))

                    particle_color = colors[i%len(colors)]
                    if i>int(20+charge*40):
                        continue
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

                    middle_angle=(-time*1.5+arm_offset+i*0.35)

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
            if fully_charged:
                for i in range(20):
                    burst_angle = ( 2*math.pi* i/120) + time*2
                    burst_radius=radius+10+(i%5)*3+int(6*math.sin(time*4+i))
                    burst_x=int(cx+burst_radius*math.cos(burst_angle))
                    burst_y=int(cy+burst_radius*math.sin(burst_angle))
                    cv2.circle(frame,(burst_x,burst_y),1,(255,180,80),-1)



    

                    

                    

            
    cv2.imshow("Rasengan CV",frame)

    if cv2.waitKey(1) == ord("q"):
        break     


camera.release()
cv2.destroyAllWindows()