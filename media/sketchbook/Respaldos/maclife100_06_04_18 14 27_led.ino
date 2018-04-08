int inputPin = 31;
int outputPin = 33;
int value = 0;

void setup() {
  Serial.begin(9600);
  pinMode(inputPin, INPUT);
  pinMode(outputPin, OUTPUT);

}

void loop() {
  value = digitalRead(inputPin);
  
  if (value == HIGH){
      digitalWrite(outputPin, HIGH);
      Serial.println("Encendido");
      delay(250);		
   }
   else{
      digitalWrite(outputPin, LOW);
      Serial.println("Apagado");
      delay(250);
   } 
}