import serial
import time
import requests

Port = "/dev/ttyACM0"  # 串口
baudRate = 9600  # 波特率
ser = serial.Serial(Port, baudRate, timeout=1)
bluetoothSerial = serial.Serial("/dev/rfcomm0",baudrate=38400)

while True:
    str = ser.readline().decode()  # 获取arduino发送的数据
    if(str != ""):
        if(str == 'btnOn\r\n'): # 发送一次便退出
            url = "http://86e0-27-52-33-129.ngrok.io/put/robo_state/2"
            response = requests.request("PUT", url)
            response = response.json()
            if response['robo_state'] == 2:
                print('狀態改變成功:working')
                bluetoothSerial.write(b'btnOn\r\n')
            else:
                print('狀態改變失敗')
            
        if(str == 'btnOff\r\n'): # 发送一次便退出
            url = "http://86e0-27-52-33-129.ngrok.io/put/robo_state/1"
            response = requests.request("PUT", url)
            response = response.json()
            if response['robo_state'] == 1 or response['robo_state'] == 0:
                print('狀態改變成功:maintain')
                bluetoothSerial.write(b'btnOff\r\n')
            else:
                print('狀態改變失敗')
ser.close()


