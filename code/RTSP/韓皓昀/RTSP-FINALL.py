#!/usr/bin/env python
# coding: utf-8

# In[1]:




import numpy as np
import cv2

from datetime import datetime

def video_save(url,outputFile,videoFile):
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(url.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(url.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("width:",width, "height:", height)
    
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))


    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 1)
            #out.write(frame)                                 #是否會有影片
            
            
            cv2.imshow('frame2',frame)
            if(int(datetime.now().strftime('%M'))%5==0 and int(datetime.now().strftime('%S'))==0):
                
                cv2.imwrite(outputFile+str(datetime.now().strftime('%H-%M-%S')) +'.jpg', frame)   #圖片名稱
            if cv2.waitKey(1) & 0xFF == ord('q'):               #結束影片按q
                break
                
        else:
            break

    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    


    
if __name__ == '__main__':
    outputFile= "D:\\phototest\\"   #圖片路徑

    videoFile = 'C:\\Users\\Stanley_Han\\output.avi' #影片路徑
    cap = cv2.VideoCapture('rtsp://syscom5g.fortiddns.com/live?cam=16&stream=1') #rtsp
    
    
    video_save(cap,outputFile,videoFile)
    

