import cv2
import simpleaudio as sa

camera=cv2.VideoCapture(1)
address="https://192.168.43.1:8080/video"
camera.open(address)

while camera.isOpened():

    #2 frames to detect movement
    ret,frame1=camera.read()
    ret,frame2=camera.read()
    diff=cv2.absdiff(frame1,frame2)
    gray=cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)

    #bluring image
    blur=cv2.GaussianBlur(gray,(5,5),0)

    #threshold for noise(distraction) elimantion
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilation=cv2.dilate(thresh,None,iterations=3)
    contours,_=cv2.cv2.findContours(dilation,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1,contours,-1,(0,255,0),2)

    for c in contours:
        if cv2.contourArea(c)<5000:
            continue
        x,y,w,h=cv2.boundingRect(c)
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        filename = 'Red Alert-SoundBible.com-108009997.wav'
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()


    if cv2.waitKey(2)==27:
        break;
    cv2.imshow('CCTV',frame1)
