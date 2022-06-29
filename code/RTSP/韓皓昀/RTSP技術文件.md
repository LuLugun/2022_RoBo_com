RTSP
=======

1.樹梅派下載VLC
------
### 1-1.更新軟件包列表以及所有當前安裝的軟件包
+ sudo apt update
+ sudo apt upgrade

### 1-2.下載VLC(以下有兩種方式)
+ sudo apt install -y vlc
+ sudo apt install vlc
+ [教學網址](https://hackpi.fun/raspberry-pi/Linux/raspberry-pi-vlc/)







2.RTSP轉HTTP
------

+ 2-1.開啟終端機輸入vlc開啟vlc
+ 2-2.點擊左上角"媒體"並選擇"開啟網路串流"
+ 2-3.輸入RTSP並點擊下面"播放"旁邊的箭頭，點擊"串流"
+ 2-4.點擊下一個
+ 2-5.檔案選擇HTTP並點擊"加入"。連接埠輸入8080，路徑輸入/test(/後文字可隨意更改)，點擊下一個
+ 2-6.勾選"啟用轉碼"，設定檔選擇"Video-Theora+Vorbis(OGG)"，點擊下一個
+ 2-7.勾選"串流所有基本串流"，點擊串流
+ 2-8.之後出現有三角錐的畫面，且下面的時間條有在計時代表成功
+ 2-9.以上範例產生的HTTP為:http://localhost:8080/test
+ [RTSP轉HTTP教學](https://blog.csdn.net/weixin_47882573/article/details/118380416)

+ 2-10.cvlc rtsp://robo.com.rtsp:123456@192.168.11.170:554/stream1 :sout='#std{access=http,mux=ts,dst=:8080}'(rtsp轉http語法)
+ 2-11.cvlc rtsp://robo.com.rtsp:123456@192.168.11.170:554/stream1 :sout='#rtp{sdp=rtsp://:8554/motn}'(rtsp轉rtsp語法)
3.Ngrok
------
### 3-1.Ngrok指令

+ ./ngrok http 8080

+ [Ngrok安裝教學](https://noob.tw/ngrok/)
4.使用Python截圖程式
------
+ 4.1更改main函式的圖片路徑、影片路徑、Rtsp url
+ 4.2如果不需儲存影片， out.write(frame)  註解掉這一行即可
