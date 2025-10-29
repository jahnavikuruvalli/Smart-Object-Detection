// --- Hybrid LDR + Camera project (no buzzer) ---

const int ldrPin = A0;
const int ledPin = 8;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char signal = Serial.read();

    if (signal == '1') {
      // Camera sees object -> LED OFF
      digitalWrite(ledPin, LOW);
      Serial.println("CAMERA_DETECTED");
    }
    else if (signal == '0') {
      // Camera sees nothing -> check LDR
      int ldrValue = analogRead(ldrPin);
      Serial.print("LDR Value: "); Serial.println(ldrValue);

      // Adjust threshold after testing (400 typical)
      if (ldrValue < 400) {
        digitalWrite(ledPin, HIGH);
        Serial.println("LDR_DETECTED");
      } else {
        digitalWrite(ledPin, LOW);
        Serial.println("LDR_CLEAR");
      }
    }
  }
  delay(200);
}