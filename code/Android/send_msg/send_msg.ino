#include <SoftwareSerial.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  //下面有設定lcd位置
SoftwareSerial BT(10, 9);// RX | TX
String test,temp;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  lcd.init();//初始化LCD
  lcd.backlight();//是否開啟背光  lcd.noBacklight(); // 關閉背光
  lcd.clear();
  lcd.setCursor(0,0);//設定游標位置
  lcd.print("Get Ready");//寫入字串
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
      digitalWrite(4, 1);
      digitalWrite(5, 0);
      lcd.clear();
      lcd.setCursor(0,0);//設定游標位置
      lcd.print("btn1");//寫入字串
    }
    else if(test=="run;"){
       Serial.println(" btn2");
       test="";
       digitalWrite(4, 0);
       digitalWrite(5, 1);
       lcd.clear();
       lcd.setCursor(0,0);//設定游標位置
       lcd.print("btn2");//寫入字串
    }
    else{
      Serial.print(data);
    }
  }
 
}
