/*Nokia Project - Team 1 : Smart IoT based Online Class System
   Arduino IDE version 1.8.14
   Software serial 2.5.8
   */
#include<SoftwareSerial.h>
SoftwareSerial XBee(6,7);

void setup(){
  Serial.begin(9600);
  XBee.begin(9600);                                                //baud rate for xbee
}

const int flexPin = A0;  
const int flexPin1 = A1;
const int flexPin2 = A2;
const int flexPin3 = A3;
// Pins connected from flex sensors

int state;

void flex() {
  Serial.begin(9600);                                                      //To begin debugging at serial monitor and specify the rate at which output has to be printed 
    pinMode(flexPin,INPUT);                                                   
    pinMode(flexPin1,INPUT); 
    pinMode(flexPin2,INPUT); 
    pinMode(flexPin3,INPUT); 
}

void loop() {
  // Read the ADC resistance
  int ADCflex = analogRead(flexPin);                                                //reads the input value at pin A0                                            
  Serial.println("Resistance: " + String(ADCflex) + " ohms");                          //debugging
    if(ADCflex<950){                                                                  //If the flex sensor1 is bent over 90 degrees or crosses the threshold
      state= 1;                                                              //conveys to perform task1 by displaying it alongside of output 
    }
   
  
  int ADCflex1 = analogRead(flexPin1);                                                //reads the input value at pin A1                                               
  Serial.println("Resistance: " + String(ADCflex1) + " ohms");                           // debugging 
     if(ADCflex1<960){                                                                  //If the flex sensor2 is bent over 90 degrees or crosses the threshold
       state= 2;                                                              //conveys to perform task2 by displaying it alongside of output
    } 
    
  
  int ADCflex2 = analogRead(flexPin2);                                             //reads the input value at pin A2
    Serial.println("Resistance: " + String(ADCflex2) + " ohms");                        // debugging 
    if(ADCflex2<980){                                                                  //If the flex sensor3 is bent over 90 degrees or crosses the threshold
    state = 3;                                                               //conveys to perform task3 by displaying it alongside of output
    }
    
  
  int ADCflex3 = analogRead(flexPin3);                                             //reads the input value at pin A3
    Serial.println("Resistance: " + String(ADCflex3) + " ohms");                       // debugging 
   if(ADCflex3<900){                                                                 //If the flex sensor4 is bent over 90 degrees or crosses the threshold
      state=4;                                                              //conveys to perform task4 by displaying it alongside of output
    } 
  if((ADCflex>950)&(ADCflex1>960)&(ADCflex2>980)&(ADCflex3>900)){
    state=0;                                                               // no task
    }
    
  Serial.println(state);                                                   // debugging 
  XBee.write(state);                                                       //Write the gesture data onto xbee using zigbee protocol
  delay(500);
}
