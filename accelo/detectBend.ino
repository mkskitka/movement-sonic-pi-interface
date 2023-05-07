
void detectBend(float roll) {
  if(roll > 40 && lastAction != LEFT_BEND) {
    if(millis() - lastActionMillis > ACTION_TIME_BUFFER) {
      Serial.println(LEFT_BEND);
      lastAction = LEFT_BEND;
      lastActionMillis = millis();
    }
  }
  if (roll < -40 && lastAction != RIGHT_BEND) {
     if(millis() - lastActionMillis > ACTION_TIME_BUFFER) {
       Serial.println(RIGHT_BEND);
       lastAction = RIGHT_BEND;
       lastActionMillis = millis();
     }
  }
}
