#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// Archived Smart Bin v1.7 controller from student hackathon.
// Hardware must be retested: motor requires a suitable driver circuit.
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo doorServo;

const int POT_PIN = A0;
const int TRIG1_PIN = 9;   // Fill-level sensor
const int ECHO1_PIN = 10;
const int TRIG2_PIN = 7;   // Bottle-entry sensor
const int ECHO2_PIN = 6;
const int SERVO_PIN = 8;
const int MOTOR_PIN = 5;

const float BIN_EMPTY_CM = 70.0;
const float BIN_FULL_CM = 12.5;
const float ENTRY_EMPTY_CM = 30.0;
const float ENTRY_FULL_CM = 10;
const int WEIGHT_THRESH = 350;
const unsigned long DOOR_OPEN_MS = 1500;
const unsigned long WAIT_AFTER_CLOSE = 3000;
const unsigned long MOTOR_ON_MS = 2500;

bool systemReady = true;
bool doorOpen = false;
bool motorOn = false;
bool motorOnceFull = false;
bool motorOnceEntry = false;
bool waitingAfterClose = false;
int lastAcceptedWeight = -1;
const int ACCEPT_DIFF = 30;
unsigned long ts = 0;
unsigned long doorCloseTime = 0;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("SmartBin v1.7");
  lcd.setCursor(0, 1);
  lcd.print("Init system...");
  delay(2000);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ready");
  lcd.setCursor(0, 1);
  lcd.print("Waiting...");
  delay(1500);

  pinMode(POT_PIN, INPUT);
  pinMode(TRIG1_PIN, OUTPUT);
  pinMode(ECHO1_PIN, INPUT);
  pinMode(TRIG2_PIN, OUTPUT);
  pinMode(ECHO2_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  digitalWrite(MOTOR_PIN, LOW);
  doorServo.attach(SERVO_PIN);
  stopDoorServo();
}

void loop() {
  int potVal = analogRead(POT_PIN);
  float dist1 = measureDistance(TRIG1_PIN, ECHO1_PIN);
  float dist2 = measureDistance(TRIG2_PIN, ECHO2_PIN);

  float pct = ((BIN_EMPTY_CM - dist1) / (BIN_EMPTY_CM - BIN_FULL_CM)) * 100.0;
  pct = constrain(pct, 0, 100);
  updateStatusDisplay(pct, potVal);

  if (pct < 20) {
    motorOnceFull = false;
    systemReady = true;
  }
  if (motorOnceEntry && dist2 >= ENTRY_EMPTY_CM) {
    motorOnceEntry = false;
  }
  if (!motorOn && !motorOnceEntry && dist2 <= ENTRY_FULL_CM) {
    showMessage("Btl OK - Motor ON");
    digitalWrite(MOTOR_PIN, HIGH);
    motorOn = true;
    motorOnceEntry = true;
    ts = millis();
  }
  if (!motorOn && !motorOnceFull && pct >= 100) {
    showMessage("Full! Motor ON");
    digitalWrite(MOTOR_PIN, HIGH);
    motorOn = true;
    motorOnceFull = true;
    systemReady = false;
    ts = millis();
  }
  if (motorOn && millis() - ts >= MOTOR_ON_MS) {
    digitalWrite(MOTOR_PIN, LOW);
    motorOn = false;
    showMessage("Motor OFF");
    delay(500);
  }
  if (pct >= 100) return;

  if (systemReady && !doorOpen && !motorOn &&
      potVal > 20 && potVal <= WEIGHT_THRESH) {
    if (abs(potVal - lastAcceptedWeight) > ACCEPT_DIFF) {
      showMessage("Opening door");
      doorServo.attach(SERVO_PIN);
      doorServo.write(90);
      doorOpen = true;
      systemReady = false;
      lastAcceptedWeight = potVal;
      ts = millis();
    }
  }
  if (doorOpen && millis() - ts >= DOOR_OPEN_MS) {
    stopDoorServo();
    showMessage("Door closed");
    doorOpen = false;
    doorCloseTime = millis();
    waitingAfterClose = true;
  }
  if (waitingAfterClose && millis() - doorCloseTime >= WAIT_AFTER_CLOSE) {
    systemReady = true;
    waitingAfterClose = false;
  }
  delay(100);
}

void updateStatusDisplay(float fillPercent, int weight) {
  lcd.setCursor(0, 0);
  char line1[17];
  snprintf(line1, 17, "V:%d%% W:%dg", (int)fillPercent, weight);
  lcd.print("                ");
  lcd.setCursor(0, 0);
  lcd.print(line1);
}

void showMessage(const char* msg) {
  lcd.setCursor(0, 1);
  lcd.print("                ");
  lcd.setCursor(0, 1);
  lcd.print(msg);
}

float measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long dur = pulseIn(echoPin, HIGH, 25000);
  float cm = (dur * 0.0343) / 2.0;
  return (cm <= 0 || cm > 300) ? 300 : cm;
}
void stopDoorServo() {
  doorServo.write(0);
  delay(300);
  doorServo.detach();
  doorOpen = false;
}
