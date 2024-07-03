#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_R 4    // Red pin of RGB LED
#define LED_G 5    // Green pin of RGB LED
#define LED_B 6    // Blue pin of RGB LED
#define BUZZER 2   // Buzzer pin

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

void setup() {
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  noTone(BUZZER);
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  String content = "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  content.toUpperCase();
  
  bool authorized = false; // Flag to indicate authorization status
  
  if (content.substring(1) == "D3 B4 30 A8") // Change here the UID of the card/cards that you want to give access
  {
    authorized = true;
    delay(500);
    digitalWrite(LED_G, HIGH); // Turn on green LED
    tone(BUZZER, 500);
    delay(300);
    noTone(BUZZER);
    digitalWrite(LED_R, LOW); // Turn off red LED
    digitalWrite(LED_B, LOW); // Turn off blue LED
    delay(300);
    digitalWrite(LED_G, LOW); // Turn off green LED

    // Send UID and authorization flag via SPI
    SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
    for (byte i = 0; i < 4; i++) { // Only send the UID "D3 B4 30 A8"
      SPI.transfer(mfrc522.uid.uidByte[i]); // Sending the UID byte values
    }
    SPI.transfer(authorized); // Send authorization flag
    SPI.endTransaction();
  } else {
    digitalWrite(LED_R, HIGH); // Turn on red LED
    tone(BUZZER, 300);
    delay(1000);
    noTone(BUZZER);
    digitalWrite(LED_G, LOW); // Turn off green LED
    digitalWrite(LED_B, LOW); // Turn off blue LED
    delay(1000);
    digitalWrite(LED_R, LOW); // Turn off red LED
    
    // Send UID and authorization flag via SPI
    SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      SPI.transfer(mfrc522.uid.uidByte[i]); // Sending the UID byte values
    }
    SPI.transfer(authorized); // Send authorization flag
    SPI.endTransaction();
  }
  delay(3000);
}