int sensorPin = 17;  // line detection sensor interface
int lightPin = 19;
int val;            // variable to store sensor reading

void setup() {
  pinMode(sensorPin,INPUT);  // define sensor as input  
  pinMode(lightPin, OUTPUT);
  Serial.begin(9600);     // initialize serial communication with PC
}

void loop() {
  val = digitalRead(sensorPin); // read value from sensor
  
  if (val == HIGH) { 
    Serial.println("Line detected");
    digitalWrite(lightPin, HIGH);
  } else { 
    Serial.println("Line NOT detected"); 
    digitalWrite(lightPin, LOW);  
  }

  delay(500);
}