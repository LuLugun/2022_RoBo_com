#include <SoftwareSerial.h> 
/*#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  //下面有設定lcd位置*/
SoftwareSerial BT(10, 9);// RX | TX

#include <TFT_HX8357.h> // Hardware-specific library
TFT_HX8357 tft = TFT_HX8357();       // Invoke custom library

String test,temp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  BT.begin(9600);
  /*lcd.init();//初始化LCD
  lcd.backlight();//是否開啟背光  lcd.noBacklight(); // 關閉背光
  lcd.clear();
  lcd.setCursor(0,0);//設定游標位置
  lcd.print("Get Ready");//寫入字串*/

  tft.init();
  tft.setRotation(1);//Rotate 90 degree
  tft.invertDisplay(1);
  tft.fillScreen(TFT_BLACK);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (BT.available()>0){
    char data = (char)BT.read();
    test += data;  
    //Serial.println(data);
    if(test=="rest;"){
      Serial.println(" btn1");
      test="";
      
      tft.fillScreen(TFT_BLACK);
      tft.setTextColor(TFT_WHITE);
      tft.setTextSize(4);
      tft.drawString("btn1",20,120,4);
    }
    else if(test=="run;"){
       Serial.println(" btn2");
       test="";

       tft.fillScreen(TFT_BLACK);
       tft.setTextColor(TFT_WHITE);
       tft.setTextSize(4);
       tft.drawString("btn1",20,120,4);
    }
    else{
      Serial.print(data);
    }
  }
 
}
