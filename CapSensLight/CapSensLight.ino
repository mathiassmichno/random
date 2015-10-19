#include <CapacitiveSensor.h>
#define TRIGGER_VAL 2000
#define RECV_PIN 2
#define SEND_PIN 4
#define OUTP_PIN 13

CapacitiveSensor   capSens = CapacitiveSensor(SEND_PIN, RECV_PIN);        // 1M resistor between pins 4 & 2, pin 2 is sensor pin, add a wire and or foil
bool isPressed = false;
bool state = false;

void setup()                    
{
  pinMode(OUTP_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop()                    
{
  long capSensVal =  capSens.capacitiveSensor(30);
  if(!isPressed && capSensVal > TRIGGER_VAL){
    isPressed = true;
    switchState();  
  } else if(capSensVal <= TRIGGER_VAL) {
    isPressed = false;
  }
  delay(20);                             // arbitrary delay to limit data to serial port 
}

void switchState()
{
  state = !state;      
  digitalWrite(OUTP_PIN, state);
}
