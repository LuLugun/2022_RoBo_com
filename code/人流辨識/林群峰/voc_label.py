# xml解析包
import xml.etree.ElementTree as ET
import pickle
import os
# os.listdir() 方法用於返回指定的資料夾包含的檔案或資料夾的名字的列表
from os import listdir, getcwd
from os.path import join


sets = ['train', 'test', 'val']
classes = ['Pedestrian']


# 進行歸一化操作
def convert(size, box): # size:(原圖w,原圖h) , box:(xmin,xmax,ymin,ymax)
    dw = 1./size[0]     # 1/w
    dh = 1./size[1]     # 1/h
    x = (box[0] + box[1])/2.0   # 物體在圖中的中心點x座標
    y = (box[2] + box[3])/2.0   # 物體在圖中的中心點y座標
    w = box[1] - box[0]         # 物體實際畫素寬度
    h = box[3] - box[2]         # 物體實際畫素高度
    x = x*dw    # 物體中心點x的座標比(相當於 x/原圖w)
    w = w*dw    # 物體寬度的寬度比(相當於 w/原圖w)
    y = y*dh    # 物體中心點y的座標比(相當於 y/原圖h)
    h = h*dh    # 物體寬度的寬度比(相當於 h/原圖h)
    return (x, y, w, h)    # 返回 相對於原圖的物體中心點的x座標比,y座標比,寬度比,高度比,取值範圍[0-1]


# year ='2012', 對應圖片的id（檔名）
def convert_annotation(image_id):
    '''
    將對應檔名的xml檔案轉化為label檔案，xml檔案包含了對應的bunding框以及圖片長款大小等資訊，
    通過對其解析，然後進行歸一化最終讀到label檔案中去，也就是說
    一張圖片檔案對應一個xml檔案，然後通過解析和歸一化，能夠將對應的資訊儲存到唯一一個label檔案中去
    labal檔案中的格式：calss x y w h　　同時，一張圖片對應的類別有多個，所以對應的ｂｕｎｄｉｎｇ的資訊也有多個
    '''
    # 對應的通過year 找到相應的資料夾，並且開啟相應image_id的xml檔案，其對應bund檔案
    in_file = open('D:\\yolov5\\data\\Annotations/%s.txt' % (image_id), encoding='utf-8')
    # 準備在對應的image_id 中寫入對應的label，分別為
    # <object-class> <x> <y> <width> <height>
    out_file = open('data/labels/%s.txt' % (image_id), 'w', encoding='utf-8')
    # 解析xml檔案
    tree = ET.parse(in_file)
    # 獲得對應的鍵值對
    root = tree.getroot()
    # 獲得圖片的尺寸大小
    size = root.find('size')
    # 如果xml內的標記為空，增加判斷條件
    if size != None:
        # 獲得寬
        w = int(size.find('width').text)
        # 獲得高
        h = int(size.find('height').text)
        # 遍歷目標obj
        for obj in root.iter('object'):
            # 獲得difficult ？？
            difficult = obj.find('difficult').text
            # 獲得類別 =string 型別
            cls = obj.find('name').text
            # 如果類別不是對應在我們預定好的class檔案中，或difficult==1則跳過
            if cls not in classes or int(difficult) == 1:
                continue
            # 通過類別名稱找到id
            cls_id = classes.index(cls)
            # 找到bndbox 物件
            xmlbox = obj.find('bndbox')
            # 獲取對應的bndbox的陣列 = ['xmin','xmax','ymin','ymax']
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            print(image_id, cls, b)
            # 帶入進行歸一化操作
            # w = 寬, h = 高， b= bndbox的陣列 = ['xmin','xmax','ymin','ymax']
            bb = convert((w, h), b)
            # bb 對應的是歸一化後的(x,y,w,h)
            # 生成 calss x y w h 在label檔案中
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


# 返回當前工作目錄
wd = getcwd()
print(wd)


for image_set in sets:
    '''
    對所有的檔案資料集進行遍歷
    做了兩個工作：
　　　　１．將所有圖片檔案都遍歷一遍，並且將其所有的全路徑都寫在對應的txt檔案中去，方便定位
　　　　２．同時對所有的圖片檔案進行解析和轉化，將其對應的bundingbox 以及類別的資訊全部解析寫到label 檔案中去
    　　　　　最後再通過直接讀取檔案，就能找到對應的label 資訊
    '''
    # 先找labels資料夾如果不存在則建立
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')
    # 讀取在ImageSets/Main 中的train、test..等檔案的內容
    # 包含對應的檔名稱
    image_ids = open('D:\\yolov5\\data\\ImageSets\\%s.txt' % (image_set)).read().strip().split()
    # 開啟對應的2012_train.txt 檔案對其進行寫入準備
    list_file = open('D:\\yolov5\\data\\%s.txt' % (image_set), 'w')
    # 將對應的檔案_id以及全路徑寫進去並換行
    for image_id in image_ids:
        list_file.write('D:\\yolov5\\data\\images/%s.jpg\n' % (image_id))
        # 呼叫  year = 年份  image_id = 對應的檔名_id
        convert_annotation(image_id)
    # 關閉檔案
    list_file.close()

# os.system(‘comand’) 會執行括號中的命令，如果命令成功執行，這條語句返回0，否則返回1
# os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
# os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")