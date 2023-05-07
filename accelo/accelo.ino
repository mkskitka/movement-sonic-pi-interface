#include "Arduino_LSM6DS3.h"
#include "MadgwickAHRS.h"

/**************************************************
 * 
 *                ACTIONS (6)
 * 
 *************************************************/

String RIGHT_BEND = "right_bend";
String LEFT_BEND = "left_bend"; 

// CIRCLE UP !  make meter length circles - n times live loop 
String CIRCLE = "circle";

String UP_JUMP = "up_jump";
String SIDE_JUMP = "side_jump"; 
String FORWARD_JUMP = "forward_jump";

// boolean to start program on raspberry pi side
bool start_sonic_pi = false; 



// initialize a Madgwick filter:
Madgwick filter;
// sensor's sample rate is fixed at 104 Hz:
const float sensorRate = 104.00;
 
// values for orientation:
float roll = 0.0;
float pitch = 0.0;
float heading = 0.0;
float lastActionMillis = 0;
String lastAction = "";
int ACTION_TIME_BUFFER = 2000;

/**************************************************
 * 
 *                    SETUP
 * 
 *************************************************/

void  setup() {
  // start the filter to run at the sample rate:
  filter.begin(sensorRate);
  Serial.begin(9600);
  Serial.flush();
  
  // attempt to start the IMU:
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
  }
}


/**************************************************
 * 
 *                    LOOP
 * 
 *************************************************/

void loop() {
  // values for acceleration and rotation:
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;
  
  // check if the IMU is ready to read:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    // read accelerometer and gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);
 
    // update the filter, which computes orientation:
    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);
 
    // print the heading, pitch and roll
    roll = filter.getRoll();
    pitch = filter.getPitch();
    heading = filter.getYaw();
 }

    detectBend(roll);
    detectJump(xAcc, yAcc, zAcc);
    detectCircle(heading);
   
}
