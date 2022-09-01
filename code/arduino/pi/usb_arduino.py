import serial

ser1 = serial.Serial('/dev/ttyACM0', 9600)

ser1.write('work'.encode()) # 對arduino輸入work
output = ser1.readline().decode('utf-8').rstrip() #讀取樹梅派輸出


# 網路範例
# https://zhuanlan.zhihu.com/p/165107539

import serial

Port = "/dev/ttyUSB1"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(Port, baudRate, timeout=1)

while True:
    send = '1'  # 发送给arduino的数据
    ser.write(send.encode())
    str = ser.readline().decode()  # 获取arduino发送的数据
    if(str != ""):
        print(str)
        if(str == 'ok\r\n'): # 发送一次便退出
            print('收到')
            break

ser.close()
