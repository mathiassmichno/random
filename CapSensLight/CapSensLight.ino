#include <CapacitiveSensor.h>
#include <Timer.h>
#define TRIGGER_VAL 220
#define RECV_PIN 2
#define SEND_PIN 4
#define LED_PIN 9
#define LONG_PRESS_MILLIS 200

CapacitiveSensor   capSens = CapacitiveSensor(SEND_PIN, RECV_PIN);        // 1M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
bool isPressed = false;
bool state = false;
int brightness = 0;    // how bright the LED is
int fadeAmount = 1;    // how many points to fade the LED by
unsigned long pressedDelta = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
#ifdef DEBUG
  Serial.begin(9600);
#endif
}

void loop() {
  long capSensVal =  capSens.capacitiveSensor(30);
  if(!isPressed && capSensVal >= TRIGGER_VAL){
    isPressed = true;
    pressedDelta = millis(); 
  }else if(isPressed && millis() - pressedDelta >= LONG_PRESS_MILLIS) {
    fade();
    isPressed = !(capSensVal < TRIGGER_VAL);  
  }else if(isPressed && capSensVal < TRIGGER_VAL) {
    switchState();
    isPressed = false;
    pressedDelta = 0;
  }
}

void switchState() {
  state = !brightness;      
  digitalWrite(LED_PIN, state);
  brightness  = state ? 255 : 0;
  fadeAmount *= (state && fadeAmount < 0) ? -1 : 1;
#ifdef DEBUG
  Serial.print("SWITCH\t");
  Serial.println(state ? "on" : "off");
#endif
  delay(400);
}

void fade(){
  analogWrite(LED_PIN, brightness);
  brightness  = brightness + fadeAmount;
  fadeAmount *= (brightness == 0 || brightness == 255) ? -1  : 1;
#ifdef DEBUG
  Serial.print("FADE\t");
  Serial.print(fadeAmount < 0 ? "-" : "+");
  Serial.print("\t");
  Serial.print(brightness);
  Serial.print("\t");
  for(int i = 0; i < brightness / 10; i++){
    Serial.print("-");  
  }
  Serial.println("");
#endif
  if(brightness < 0 || brightness > 255){
    fadeAmount *= (brightness < 0 ? (fadeAmount < 0 ? -1 : 1) : (fadeAmount > 0 ? -1 : 1));
    brightness  = brightness < 0 ? 0 : 255;   
  }
  delay(20);  
}
