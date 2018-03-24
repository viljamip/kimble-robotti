
int sensorPin = A0;    // select the input pin for the potentiometer
int pinOut = 2;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

void setup() {
  // put your setup code here, to run once:
  pinMode(pinOut, OUTPUT); 
  pinMode(sensorPin, INPUT); 
  digitalWrite( pinOut, LOW);
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);
  if (sensorValue > 800) {
      digitalWrite( pinOut, HIGH);
  }
  else {
    digitalWrite( pinOut, LOW);
  }
  // put your main code here, to run repeatedly:

}
