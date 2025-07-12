#include <AFMotor.h>
#include <Wire.h>

#define SLAVE_ADDRESS 8  // You can change this as needed

// Initialize motors
AF_DCMotor motor1(1); // Turning
AF_DCMotor motor2(2); // Forward/Backward & Turning
AF_DCMotor motor3(3); // Forward/Backward

void setup() {
    Serial.begin(9600);
    Serial.println("Motor control initialized over I2C.");

    Wire.begin(SLAVE_ADDRESS);          // Join I2C bus as slave
    Wire.onReceive(receiveCommand);     // Register receive event
}

void stopMotors() {
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    Serial.println("Motors Stopped");
}

void moveForward() {
    motor1.run(RELEASE);
    motor2.setSpeed(45);
    motor2.run(FORWARD);
    motor3.setSpeed(60);
    motor3.run(FORWARD);
    Serial.println("Moving Forward");
    delay(2000);
    stopMotors();
}

void moveBackward() {
    motor1.run(RELEASE);
    motor2.setSpeed(45);
    motor2.run(BACKWARD);
    motor3.setSpeed(60);
    motor3.run(BACKWARD);
    Serial.println("Moving Backward");
    delay(2000);
    stopMotors();
}

void turnLeft() {
    motor1.setSpeed(60);
    motor1.run(BACKWARD);
    motor2.setSpeed(45);
    motor2.run(FORWARD);
    motor3.run(RELEASE);
    Serial.println("Turning Left");
    delay(1000);
    stopMotors();
}

void turnRight() {
    motor1.setSpeed(60);
    motor1.run(FORWARD);
    motor2.setSpeed(45);
    motor2.run(BACKWARD);
    motor3.run(RELEASE);
    Serial.println("Turning Right");
    delay(1000);
    stopMotors();
}

void receiveCommand(int byteCount) {
    while (Wire.available()) {
        char command = Wire.read();
        switch (command) {
            case 'f':
                moveForward();
                break;
            case 'b':
                moveBackward();
                break;
            case 'l':
                turnLeft();
                break;
            case 'r':
                turnRight();
                break;
            case 's':
                stopMotors();
                break;
            default:
                Serial.println("Invalid Command Received via I2C");
                break;
        }
    }
}

void loop() {
    // Nothing here; commands come from I2C
}