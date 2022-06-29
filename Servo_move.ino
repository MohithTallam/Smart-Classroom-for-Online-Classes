/* Nokia Project - Team 1 : Smart IoT based Online Class System
   Board: Arduino UNO
   Arduino IDE version 1.8.14
   Servo.h version 1.1.7
   Software serial 2.5.8
*/

#include<Servo.h>
#include<SoftwareSerial.h>

int received = 0;                         // variable to recive the data from zigbee
int incomingByte;                         // variable to receive the data from python code
int k1=60;                                // servo can move 120 degrees, hence center at 60 for max angles on either side
                                 
Servo servo_9;                            // servo object instantiated
SoftwareSerial zigbee(13,12);             // passing pins to zigbee function

void setup() {
  Serial.begin(9600);                     // Initialize serial communication at 9600 baudrate(bits/second). 
  zigbee.begin(9600);                     // Zigbee receives data at 9600 baudrate
  servo_9.attach(9);                      // Bind pin 9 to servo_9 object.
  servo_9.write(k1);                      // Set base servo to intial values based on practical implementation of the device.
}

void loop() {
  if (zigbee.available() > 0) {      // if data is available from the zigbee receiver  
  received = zigbee.read();          // zigbee.read() returns the value received by zigbee 
  Serial.print(received);            // print the data onto serial monitor so that the python script can read it
}
  delay(50);                            // Set a loop delay so that we don't overload servo's controller currently set to 50ms.
  if (Serial.available() > 0) {         // Check if theres any data coming through serial port from the computer.
    incomingByte = Serial.read();       // Read the data coming through the serial port.
    
    if (incomingByte == '1') {         
      k1--;                            // Move base servo left to compensate.
  }
  else if(incomingByte=='2'){
    k1++;                             // Move base servo right to compensate.
  }
  else{
    k1=k1;                            // Position of subject adequately compensated stop the servos.  
  }
    
/*Saftey limits to stop servo moving over it's limits currently defined as 120 for base servo.*/
 
  if(k1>=120){
    k1=120;
    }
  else if(k1<0){
    k1=0;
    }
/* Write the angle values to the servo's through Arduino's PWM pins by using the servo_object.write() function. */
 servo_9.write(k1);
}
}
