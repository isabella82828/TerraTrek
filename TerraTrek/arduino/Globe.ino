#include <Arduino.h>
#include <AccelStepper.h>
#include <digitalWriteFast.h>
#include <time.h>

#define PHOTO_INTERRUPT_PIN 4
#define DIR_PIN 2
#define STEP_PIN 3
#define STEPS 200

#define STEPPER_ACCEL 100
#define STEPPER_VEL 300
#define SERVO_EASE_TIME 2000

// Define motor interface type
#define MOTOR_INTERFACE_TYPE 1

// Creates an instance
AccelStepper myStepper(MOTOR_INTERFACE_TYPE, STEP_PIN, DIR_PIN);

// Must specify this before the include of "ServoEasing.hpp"
//#define USE_PCA9685_SERVO_EXPANDER    // Activating this enables the use of the PCA9685 I2C expander chip/board.
//#define USE_SOFT_I2C_MASTER           // Saves 1756 bytes program memory and 218 bytes RAM compared with Arduino Wire
//#define USE_SERVO_LIB                 // If USE_PCA9685_SERVO_EXPANDER is defined, Activating this enables force additional using of regular servo library.
//#define USE_LEIGHTWEIGHT_SERVO_LIB    // Makes the servo pulse generating immune to other libraries blocking interrupts for a longer time like SoftwareSerial, Adafruit_NeoPixel and DmxSimple.
//#define PROVIDE_ONLY_LINEAR_MOVEMENT  // Activating this disables all but LINEAR movement. Saves up to 1540 bytes program memory.
#define DISABLE_COMPLEX_FUNCTIONS     // Activating this disables the SINE, CIRCULAR, BACK, ELASTIC, BOUNCE and PRECISION easings. Saves up to 1850 bytes program memory.
#define MAX_EASING_SERVOS 1
//#define DISABLE_MICROS_AS_DEGREE_PARAMETER // Activating this disables microsecond values as (target angle) parameter. Saves 128 bytes program memory.
//#define DISABLE_MIN_AND_MAX_CONSTRAINTS    // Activating this disables constraints. Saves 4 bytes RAM per servo but strangely enough no program memory.
//#define DISABLE_PAUSE_RESUME               // Activating this disables pause and resume functions. Saves 5 bytes RAM per servo.
//#define DEBUG                              // Activating this enables generate lots of lovely debug output for this library.

//#define PRINT_FOR_SERIAL_PLOTTER           // Activating this enables generate the Arduino plotter output from ServoEasing.hpp.

/*
 * Specify which easings types should be available.
 * If no easing is defined, all easings are active.
 * This must be done before the #include "ServoEasing.hpp"
 */
//#define ENABLE_EASE_QUADRATIC
#define ENABLE_EASE_CUBIC
//#define ENABLE_EASE_QUARTIC
//#define ENABLE_EASE_SINE
//#define ENABLE_EASE_CIRCULAR
//#define ENABLE_EASE_BACK
//#define ENABLE_EASE_ELASTIC
//#define ENABLE_EASE_BOUNCE
//#define ENABLE_EASE_PRECISION
//#define ENABLE_EASE_USER

#include "ServoEasing.hpp"
#include "PinDefinitionsAndMore.h"

/*
 * Pin mapping table for different platforms - used by all examples
 *
 * Platform         Servo1      Servo2      Servo3      Analog     Core/Pin schema
 * -------------------------------------------------------------------------------
 * (Mega)AVR + SAMD    9          10          11          A0
 */

ServoEasing Servo1;
void blinkLED();

#define START_DEGREE_VALUE  90 // The degree value written to the servo at time of attach.
float servoPosition;
long stepperSteps;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    pinModeFast(PHOTO_INTERRUPT_PIN, INPUT);
    Serial.begin(115200);
    
    /********************************************************
     * Attach servo to pin and set servos to start position.
     * This is the position where the movement starts.
     *******************************************************/
#if !defined(PRINT_FOR_SERIAL_PLOTTER)
    Serial.println(F("Attach servo at pin " STR(SERVO1_PIN)));
#  endif

    if (Servo1.attach(SERVO1_PIN, START_DEGREE_VALUE) == INVALID_SERVO) {
        Serial.println(F("Error attaching servo"));
        while (true) {
            blinkLED();
        }
    }

    // Wait for servo to reach start position.
    Servo1.setEasingType(EASE_CUBIC_IN_OUT);

    myStepper.setMaxSpeed(1000);
    myStepper.setAcceleration(STEPPER_ACCEL);
    
    myStepper.setSpeed(100); // temporarily run slower during position zeroing
    
    time_t start_reset_time;
    start_reset_time = time(NULL);
  
    while(digitalReadFast(PHOTO_INTERRUPT_PIN)) { // Wait for photointerrupter to no longer be interrupted
        myStepper.runSpeed(); // non-blocking, runs stepper at constant speed
        if((time(NULL) - start_reset_time) > 15){
          Serial.println(F("Error localizing position. Please check for sensor obstruction"));
          while (true) {
            blinkLED();
          }          
        }
    }

    myStepper.setCurrentPosition(0); // Sets steppers home position
    myStepper.setSpeed(STEPPER_VEL);
    Serial.println(F("Zeroed position"));
    delay(1000); // Wait for servo to reach 90 degree position
}

void loop() {
    if(Serial.available() > 0) {
        // Parse latitude and longitude from Raspberry Pi
        String inputString = Serial.readStringUntil('\n'); 
        String substrings[2];
    
        int comma_idx = inputString.indexOf(','); 
        if(comma_idx == -1){
          Serial.println(F("Invalid coordinates"));
          return;
        }

        substrings[0] = inputString.substring(0, comma_idx); 
        substrings[1] = inputString.substring(comma_idx+1, -1);
    
        float longitude, latitude;
        // This conversion is always successful, even for strings which don't represent floats
        latitude = substrings[0].toFloat(); 
        longitude = substrings[1].toFloat();
    
        Serial.print("Longitude: ");
        Serial.println(longitude);
        Serial.print("Latitude: ");
        Serial.println(latitude);

        stepperSteps = (long) (longitude*STEPS/360); // convert from degrees to steps: 1.8 DEG per STEP
        servoPosition = -latitude + 90; // Latitude is from -90 to 90 degrees, servo accepts input from 0 to 180 degrees

        if(stepperSteps > STEPS || abs(servoPosition) > 80){
          Serial.println("Invalid motor input");
          return;
        }

        Serial.print(F("Move stepper to "));
        Serial.print(stepperSteps);
        Serial.print(F(" at speed "));
        Serial.print(STEPPER_VEL);
        Serial.print(F(" steps/s with acceleration "));
        Serial.print(STEPPER_ACCEL);
        Serial.println(F(" steps/s^2"));
        
        Serial.print(F("Move servo to "));
        Serial.print(servoPosition);
        Serial.print(F(" in "));
        Serial.print(SERVO_EASE_TIME);
        Serial.println(F(" ms"));
        Serial.flush(); // Just in case interrupts do not work

        Servo1.startEaseToD(servoPosition, SERVO_EASE_TIME); // start servo easing
        myStepper.moveTo(stepperSteps); // set desired stepper position
        
        while (Servo1.isMoving()) {
            myStepper.run(); // move stepper and servo in tandem
        }
        while (myStepper.distanceToGo() > 0) {
            myStepper.run(); // Keep moving stepper if servo finishes early
        }
    }
}

void blinkLED() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
}
