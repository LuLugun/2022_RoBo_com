/*#include <SoftwareSerial.h>   // 引用程式庫

// 定義連接藍牙模組的序列埠
SoftwareSerial BT(8, 9); // 接收腳(TXD/RX -->), 傳送腳(RXD/TX <--)
//Specifically for the Arduino Mega 2560 (or 1280 on the original Arduino Mega)
// Only pins available for RECEIVE (TRANSMIT can be on any pin):
// Pins: 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69
char val;  // 儲存接收資料的變數
String text="";

void setup() {
  Serial.begin(9600);   // 與電腦序列埠連線
  Serial.println("BT is ready!");

  // 設定藍牙模組的連線速率
  // 如果是HC-05，請改成38400
  BT.begin(9600);
}

void loop() {
  // 若收到「序列埠監控視窗」的資料，則送到藍牙模組
  if (Serial.available()) {
    val = Serial.read();
    BT.print(val);
    
  }
  // 若收到藍牙模組的資料，則送到「序列埠監控視窗」
  delay(2000);
  if (BT.available()) {
    
    while(BT.available()){
      text += (char)BT.read();      
    }
    Serial.print(text);
    text="";
  }
  
}*/

/*
 One Shot
 Kudos to marguskohv - he sowed the seed....
Serial monitor is just aide memoire
 */
#include <SoftwareSerial.h>
SoftwareSerial BT(10, 11); // RX | TX
String command = ""; // Stores response from HC-06 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);       //monitor
  BT.begin(9600);       //monitor
  //Serial1.begin(115200);      //bluetooth 
    
  Serial.print("AT     ");  
  BT.print("AT");                  //PING
  delay(2000);
  if (BT.available()) {
    while(BT.available()) { // While there is more to be read, keep reading.
      //delay(10);
      command += (char)BT.read();    
    }
  }
  //delay(2000);
  Serial.println(command);//""
  command = ""; // No repeats
  
  Serial.print("AT+NAMEFosters      "); 
  Serial1.print("AT+NAMEHC-06");        //CHANGE NAME
  delay(2000);
  if (Serial1.available()) {
    while(Serial1.available()) { // While there is more to be read, keep reading.
      //delay(10);
      command += (char)Serial1.read();  
    }
  }
  //delay(2000);
  Serial.println(command);//ok""
  command = ""; // No repeats

  Serial.print("AT+PIN1234          ");
  Serial1.print("AT+PIN0000");        //CHANGE PASSWORD
  delay(2000); 
  if (Serial1.available()) {
    while(Serial1.available()) { // While there is more to be read, keep reading.
      //delay(10);
      command += (char)Serial1.read();  
    }
  }
  //delay(2000);   
  Serial.println(command);
  command = ""; // No repeats

  Serial.print("AT+VERSION          ");  
  Serial1.print("AT+VERSION");               //CHANGE SPEED TO 115K
  delay(2000); 
  if (Serial1.available()) {
    while(Serial1.available()) { // While there is more to be read, keep reading.
        //delay(10);
      command += (char)Serial1.read();    
    } 
  } 
  //delay(2000);       
  Serial.println(command);
}

void loop(){
}   //one-shot - nothing here
