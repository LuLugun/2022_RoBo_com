#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import cv2
import os
from datetime import datetime
import requests

def video_save(url,outputFile,videoFile,time):
    while True:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width = int(url.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(url.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("width:",width, "height:", height)

        out = cv2.VideoWriter(videoFile, fourcc, 20.0, (width, height))
        print('0')

        while(cap.isOpened()):
            print('1')
            ret, frame = cap.read()
            if ret == True:
                print('2')
                frame = cv2.flip(frame, 1)
                #out.write(frame)                                 #是否會有影片


                #cv2.imshow('frame2',frame)
                if(int(datetime.now().strftime('%M'))%time==0 and int(datetime.now().strftime('%S'))%5==0):
                    print('3')
                    cv2.imwrite(outputFile+str(datetime.now().strftime('%H-%M-%S')) +'.jpg', frame)  #圖片名稱
                    url1 = "http://419b-2001-b011-4010-309e-c3f2-86a9-be31-b96d.ngrok.io/jpg"
                    payload={}
                    nowtime=str(datetime.now().strftime('%H-%M-%S')) +'.jpg'
                    files=[
                    ('files',(nowtime,open(outputFile+nowtime,'rb'),'image/jpeg'))
                    ]
                    headers = {}

                    response = requests.request("POST", url1, headers=headers, data=payload, files=files)

                    print(response.text)

                        #if cv2.waitKey(1) & 0xFF == ord('q'):   
                            #print("break") #結束影片按q
                            #break


            #else:
                #cap.release()
                #out.release()
                #cv2.destroyAllWindows()



    
if __name__ == '__main__':
    
    time=int(1)   #間隔幾分鐘截取一次
    outputFile= "D:\\phototest\\"   #圖片路徑
    
    videoFile = 'D:\\videotest\\output.avi' #影片路徑
    cap = cv2.VideoCapture('rtsp://syscom5g.fortiddns.com/live?cam=16&stream=1') #rtsp
    
 
        
    while True:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #print("width:",width, "height:", height)

        out = cv2.VideoWriter(videoFile, fourcc, 20.0, (width, height))
        #print('0')

        while(cap.isOpened()):
            #print('1')
            ret, frame = cap.read()
            if ret == True:
                #print('2')
                frame = cv2.flip(frame, 1)
                #out.write(frame)                                 #是否會有影片


                #cv2.imshow('frame2',frame)
                if(int(datetime.now().strftime('%M'))%time==0 and int(datetime.now().strftime('%S'))==0):
                    #print('3')
                    nowtime=str(datetime.now().strftime('%H-%M-%S')) +'.jpg'
                    cv2.imwrite(outputFile+nowtime, frame)  #圖片名稱
                    url1 = "http://419b-2001-b011-4010-309e-c3f2-86a9-be31-b96d.ngrok.io/jpg"
                    payload={}
            
                    files=[
                    ('files',(nowtime,open(outputFile+nowtime,'rb'),'image/jpeg'))
                    ]
                    headers = {}

                    response = requests.request("POST", url1, headers=headers, data=payload, files=files)

                    #print(response.text)

                        #if cv2.waitKey(1) & 0xFF == ord('q'):   
                            #print("break") #結束影片按q
                            #break


            else:
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                time=int(1)   #間隔幾分鐘截取一次
                outputFile= "D:\\phototest\\"   #圖片路徑
    
                videoFile = 'D:\\videotest\\output.avi' #影片路徑
                cap = cv2.VideoCapture('rtsp://syscom5g.fortiddns.com/live?cam=16&stream=1') #rtsp
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                

                out = cv2.VideoWriter(videoFile, fourcc, 20.0, (width, height))
                #print('0')

