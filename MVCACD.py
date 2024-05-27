import cv2 as cv
import numpy as np
import time
import RPi.GPIO as GPIO
from time import sleep
import threading

PUL = 17
DIR = 27
ENA = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

print('PUL = GPIO 17 on Pin #11')
print('PUL = GPIO 27 on Pin #13')
print('PUL = GPIO 22 on Pin #15')

print('init complete')

duration =19 # this is how long the motor will spin for

delay = 0.0003


# this sets the speed

fwd = GPIO.LOW
bck = GPIO.HIGH

slow = 0.0001
med =  0.00001
fast = 0.00000001

offset = 35
position = 73

pos0 = 30
pos1 = 35
pos2 = 45

print('doneso')

''''''
font = cv.FONT_HERSHEY_SIMPLEX

Colourlist = {'green':  [0, 255, 0],
              'red':    [0, 0, 255],
              'black':  [0, 0, 0],
              'yellow': [0, 255, 255],
              'white':  [255, 255, 255]}
# BGR

boundary = {'black': [[180, 255, 30], [0, 0, 0]],
              'white': [[255, 255, 255], [0, 0, 231]],
              'red1': [[180, 255, 255], [159, 50, 70]],
              'red': [[9, 255, 255], [0, 50, 70]],
              'green': [[235, 255, 250], [90, 220, 100]],
              ''''green': [[89, 255, 255], [36, 50, 70]]'''
              'blue': [[128, 255, 255], [90, 50, 70]],
              'yellow': [[35, 255, 255], [25, 50, 70]],
              'purple': [[158, 255, 255], [129, 50, 70]],
              'orange': [[24, 255, 255], [10, 50, 70]],
              'gray': [[180, 18, 230], [0, 0, 40]]}

# Upper then Lower bounds, RGB

ARimage = cv.imread("alien")
#cv.imshow("alien", ARimage)
#cv.waitKey(20)
video = cv.VideoCapture(0)

# setup above

def drivetest(direction, speeddelay, reps, offset):
    if direction == fwd:
        offset += reps
    elif direction == bck:
        offset -= reps
    for _ in range(0, reps):
        GPIO.output(ENA, GPIO.HIGH)
        GPIO.output(DIR, direction)
        for _ in range(duration):
            GPIO.output(PUL, GPIO.HIGH)
            sleep(speeddelay)
            GPIO.output(PUL, GPIO.LOW)
            sleep(speeddelay)
        GPIO.output(ENA, GPIO.LOW)
    return offset

# function drives a set amount to the left or right
def drive(pos):
    global offset
    if pos < 0:
        direct = bck
    elif pos > 0:
        direct = fwd
    for _ in range(0, abs(pos)):
        if pos < 0:
            offset -= 1
        elif pos > 0:
            offset += 1
        GPIO.output(ENA, GPIO.HIGH)
        GPIO.output(DIR, direct)
        for _ in range(duration):
            GPIO.output(PUL, GPIO.HIGH)
            sleep(delay)
            GPIO.output(PUL, GPIO.LOW)
            sleep(delay)
        GPIO.output(ENA, GPIO.LOW)
        print(offset)
        if event.is_set():
            break

def colourid(colour):
    mask = cv.inRange(imagerot, np.array(boundary.get(colour)[1]), np.array(boundary.get(colour)[0]))
    contours, null = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    x, y = 0,0
    array = []
    if len(contours) >= 0:
        for contour in contours:
            if cv.contourArea(contour) > 50 and cv.contourArea(contour) < 3000:
                x,y,w,h = cv.boundingRect(contour)
                
                resized = cv.resize(ARimage, (w, h))
                if y>160 and y<550 and y>445-(1.91*x) and y>1.76*x-410:
                    imagerot[y:y+h, x:x+w] = resized
                    array.append((x,y))
                    
                    # add an if statement in here to put correct ar image based on colour
                    #cv.rectangle(imagerot, (x,y), (x+w, y+h), Colourlist.get('white'),2)
    return mask, array

def whichtrack(loc):
    tracks = []
    for j in loc:
        i = j[0]
        if i > 0:    
            if   i <= 100:
                tracks.append(0)
            elif i > 100 and i < 200: # statement to check at a set y coordinate for given x locations:
                tracks.append(1)
            elif i >= 200: # statement to check at a set y coordinate for given x locations:
                tracks.append(2)
            else:
                tracks.append(3) # should never happen
    return tracks

def channels(channel):
    if channel == 0:
        targetpos = pos0
    elif channel == 1:
        targetpos = pos1
    elif channel == 2:
        targetpos = pos2
    elif channel == -1:
        targetpos = position
    return targetpos

# functions above

event = threading.Event()

while True:
    route = []
    success, img = video.read()
    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    imagerot = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    # cv.rectangle(imagerot, (150,160), (152,162), Colourlist.get('red'))
    cv.rectangle(imagerot, (350,175), (352,177), Colourlist.get('red'))
    cv.rectangle(imagerot, (0,441), (2, 443), Colourlist.get('red'))
    
    maskgreen, green = colourid('green')
    maskwhite, white = colourid('white')
    
    combined = green + white
        
        # x, y
    print("x,y", combined)
    
    b = lambda a : a[::-1]
    
    for i in range(0, len(combined)):
        combined[i] = b(combined[i])
    
    # now y, x
    print("y,x",combined)    
    combinedsorted = sorted(combined, reverse=True)
        
    print("sorted", combinedsorted)
    for i in range(len(combinedsorted)):
        cv.putText(imagerot, str(i),b(combinedsorted[i]) ,font , 1, (255,255,255), 2, 2)
    
    greenarr = whichtrack(green)
    whitearr = whichtrack(white)
    
    print(greenarr)
    print(whitearr)
    
    route = greenarr + whitearr
        
    taken = []
    channel = -1
    for i in route:
        if len(taken) >= 2:
            channel = 3 - sum(taken)
        elif i not in taken:
            taken.append(i)
   
    cv.imshow("mask1", maskgreen)
    cv.imshow("mask2", maskwhite)
    cv.imshow("webcam", imagerot)
    print(route)
    
    # Move to selected channel
    # event.set()
    targetpos = channels(channel)
    print(targetpos)
    # event.clear()
    thread = threading.Thread(target=drive, args=((targetpos - offset),))
    # thread = threading.Thread(target=print, args=(1,))

    thread.run()
    
    cv.waitKey(1)

GPIO.cleanup()