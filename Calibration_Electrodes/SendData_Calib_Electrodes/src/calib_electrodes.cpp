/**
   * @file calib_electrodes.cpp
   * @author Équipe Acquisition - Heka
   * @brief 
   * 
   * @copyright Copyright Heka (c) 2022
   * 
   */

#include <Arduino.h>
#include "calib_electrodes.h"

void setup() {
  Serial.begin(9600u);

  analogReadResolution(12u);
}

void loop() {
  pos_x = analogRead(VRX);
  pos_y = analogRead(VRY);

  values_to_send[0] = pos_x;
  values_to_send[1] = pos_x >> 8;

  Serial.write(values_to_send, 2);
  Serial.send_now();

  delay(30);
}