## Line_tracking Code ##
# capture_image_HSV_segmented_dilate_Hough_line
# Final vision add output wiringPi and close the trackbar windows

import cv2
import numpy as np
import wiringpi
import time
import io
from picamera import PiCamera

stream = io.BytesIO()
camera = PiCamera()
#camera.start_preview()
camera.resolution=(160,120)
time.sleep(2)

def photoCap():
    camera.capture(stream,'jpeg')
    data = np.fromstring(stream.getvalue(),dtype=np.uint8)
    image = cv2.imdecode(data,1)
    image = image[:,:,::-1]
    stream.seek(0)
    stream.truncate(0)
    image = np.array(image,dtype = np.uint8)
    return image

# set output pins
wiringpi.wiringPiSetup()
wiringpi.pinMode (23,1)
wiringpi.pinMode (24,1)	
wiringpi.pinMode (25,1)
wiringpi.digitalWrite(23, 0)
wiringpi.digitalWrite(24, 0)
wiringpi.digitalWrite(25, 0)

while(1):
    
    frame = photoCap()
    print(frame.shape)
    cv2.imshow("capture",frame) # capture image 
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
    lower_hsv=np.array([15,50,150])
    upper_hsv=np.array([255,255,255])
    mask=cv2.inRange(hsv,lower_hsv,upper_hsv)
    cv2.imshow("hsv",mask) # HSV segmented image

    # open and close operation
    element=cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
    threshold=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,element)
    threshold=cv2.morphologyEx(threshold,cv2.MORPH_OPEN,element)
    canny=cv2.Canny(threshold,0,50,3)
    gaussian=cv2.GaussianBlur(canny,(5,5),0)
    cv2.imshow('edges',gaussian) 
    
    # Hough line detection
    lines=cv2.HoughLines(gaussian,1,np.pi/180,80)
    n=0
    avgAngle=0
    if lines == None :
        avgAngle = 888 
    else :
        for line in lines:
            rho,theta=line[0]
            a=np.cos(theta)
            b=np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(frame, (x1,y1),(x2,y2),(0,0,255), 2)
            Angle=theta*57.3
            if Angle<90 :
                Angle=Angle
            elif Angle>90 :
                Angle=-180+Angle
            else :
                n=n+1
                Angle=0
            avgAngle = avgAngle+Angle
        avgAngle = avgAngle/(len(lines)-n)
    print("avgAngle", avgAngle);
    cv2.imshow("houghlines", frame)
        
    # output 0 1 to communication with Arduino 
    if avgAngle>15 and avgAngle<=30 :
        wiringpi.digitalWrite(23, 1)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
        
    elif avgAngle>30 and avgAngle<=60 :
        wiringpi.digitalWrite(23, 1)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(24, 1)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
        
    elif avgAngle>60 and avgAngle<=90 :
        wiringpi.digitalWrite(23, 1)
        wiringpi.digitalWrite(24, 1)
        wiringpi.digitalWrite(25, 0)
        wiringpi.delay(500)
        
    elif avgAngle>-15 and avgAngle<=15 :
        wiringpi.digitalWrite(23, 1)
        wiringpi.digitalWrite(24, 1)
        wiringpi.digitalWrite(25, 1)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
            
    elif avgAngle>-30 and avgAngle<=-15 :
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 1)
        wiringpi.digitalWrite(25, 1)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
            
    elif avgAngle>-60 and avgAngle<=-30 :
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 1)
        wiringpi.digitalWrite(25, 0)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
       
    elif avgAngle>-90 and avgAngle<=-60 :
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 1)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
            
    else :
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
        wiringpi.delay(500)
        wiringpi.digitalWrite(23, 0)
        wiringpi.digitalWrite(24, 0)
        wiringpi.digitalWrite(25, 0)
    
    if cv2.waitKey(1)&0xFF==ord('q'):
        break 
        
    # time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()
