import cv2
x=320
y=240

camera = cv2.VideoCapture(0)
while True:
    success, frame=camera.read()
    if not success:
        break
    cv2.circle(frame,(x,y),50,(255,0,0),-1)
 
    cv2.imshow("Rasengan",frame)
    key = cv2.waitKey(1)
    if key == ord("a"):
        x-=10
    elif key == ord("d"):
        x+=10
    elif key == ord("s"):
        y+=10
    elif key == ord("w"):
        y-=10
    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()