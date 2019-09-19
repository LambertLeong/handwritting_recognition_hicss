#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <stdio.h>
#include <stdlib.h>

//#include <SD.h>
//Table table;

/* 
 *  For SPI Setup...
 */
#define LSM9DS1_AG_CS 15
#define LSM9DS1_M_CS 33


//#define fp=fopen("~/Arduino/test","w");

//////////////////////////
// LSM9DS1 Library Init //
// https://learn.sparkfun.com/tutorials/lsm9ds1-breakout-hookup-guide#using-the-arduino-library
//////////////////////////
// Use the LSM9DS1 class to create an object. [imu] can be
// named anything, we'll refer to that throught the sketch.

LSM9DS1 imu;

//int LED_pin = 27;
const int buttonPin = 13;     // the number of the pushbutton pin
int buttonState = 0;
String tmp = "";
int trial = 0;
int record = 0;
unsigned long t1 = millis();
unsigned long t2 = millis();

void setup() {

  Serial.begin(9600);

  delay(1); 
  pinMode(buttonPin, INPUT);
  
  imu.settings.device.commInterface = IMU_MODE_SPI;
  imu.settings.device.mAddress = LSM9DS1_M_CS;
  imu.settings.device.agAddress = LSM9DS1_AG_CS;

  if (!imu.begin()) {
    Serial.println("Failed to communicate with LSM9DS1.");
    Serial.println("Looping to infinity.");
    while (1);
  }

}

void loop() {
//////////////////////////////
// python will handle i/o //
// just print to screen ////
////////////////////////////
  while(digitalRead(buttonPin) == HIGH){
    //digitalWrite(LED_pin, HIGH);

    if(record == 0){
      Serial.print("START ");
      Serial.println(trial);
      record = 1;
      t1 = millis();
      }
    
    imu.readAccel();
    imu.readGyro();
    t2 = millis();
    Serial.print(millis()-t1);
    Serial.print(", ");
    Serial.print(imu.ax); // Print x-axis data
    Serial.print(", ");
    Serial.print(imu.ay); // print y-axis data
    Serial.print(", ");
    Serial.print(imu.az); 
    Serial.print(", ");

    Serial.print(imu.calcGyro(imu.gx)); // Print x-axis rotation in DPS
    Serial.print(", ");
    Serial.print(imu.calcGyro(imu.gy)); // Print y-axis rotation in DPS
    Serial.print(", ");
    Serial.print(imu.calcGyro(imu.gz)); // Print z-axis rotation in DPS
    Serial.print(", \n");
        
    delay(1);
  }
  if(record == 1){
    trial++;
    Serial.println("STOP \n");
    record = 0;
    }
  delay(1000);
}
