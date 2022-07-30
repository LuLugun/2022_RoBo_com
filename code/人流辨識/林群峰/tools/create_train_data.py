import os
import shutil

file_list = os.listdir('Z:')
for i in range(len(file_list) // 30):
    f1 = 'Z:\\'+ file_list[i*30]
    f2 = 'D:\\AI Image recognition\\robo com\\dataset\\'+ file_list[i*30]
    shutil.copyfile(f1,f2)
