void setup() {
pinMode(15, OUTPUT);
pinMode(4, INPUT);
Serial.begin(9600);
}


void loop() {
int light;
light = analogRead(4);
Serial.println(light);
if (light < 200) {
digitalWrite(15, HIGH);
} else {
digitalWrite(15, LOW);
}
delay(100);
}