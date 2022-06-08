#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
#调用多摄像头画面
#采用rtsp实时流传输协议
#用以下模板调用其他摄像头，下面的#cam_url是大华摄像头的，根据上面提供的rtsp地址自己修改即可。
cam_url='rtsp://han10301073@gmail.com:9400882121Hh@192.168.1.119:554/stream1'
cap=cv2.VideoCapture(cam_url)                         #调用IP摄像头

if cap.isOpened(): 
    print("1")
    rval, frame = cap.read() #读取视频流
else:
    print("2")
    cap.open(cam_url)                                 #打开读取的视频流
    rval = False
    print("error")
while rval:

    frame=cv2.resize(frame,(720,720))                 #调节输出图像的大小
    cv2.imshow("cam_num1", frame)                     #显示视频流
    rval, frame = cap.read()
    key = cv2.waitKey(1)
    if key == 27:                                     #按ESC键退出
        break
cap.release()
print("4")#释放摄像头
cv2.destroyAllWindows()                               #关闭窗口
print("5")

