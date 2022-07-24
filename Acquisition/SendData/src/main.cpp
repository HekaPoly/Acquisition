/**
 * @file main.cpp
 * @author Équipe Acquisition - Heka
 * @brief 
 * This file contains the setup for the uC program running to collect data from electrodes and encoders.
 * It also contains the main loop of the program. This main loop runs every WAIT_TIME_MICROS.
 * @version 0.1
 * @date 2022-06-11
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "sendData.h"
#include "bitwise_operations.h"


/* TODO: Implement interrupts to see if it is faster to use than simply reading pins */
/*
void interrupt_Encod1() {
  char i;
  i = digitalRead(encoder1_Pin2);
  if (i == 1)
    valueEncoder[0] += 1;
  else
    valueEncoder[0] -= 1;
}


void interrupt_Encod2() {
  char i;
  i = digitalRead(encoder2_Pin2);
  if (i == 1)
    valueEncoder[1] += 1;
  else
    valueEncoder[1] -= 1;
}
*/


void setup() 
{
  /* 
    Set baud rate 
    1M is an arbitrary value, could be more or could be less - will depend on tests
  */
  Serial.begin(1000000u);

  /* 
    Set ADC resolution - 12 bits brings us to an interval of 0 to 4095 (2^12 - 1)
  */
  analogReadResolution(12u);

  /* 
    TODO : Implement encoder array - writing with a for loop in an encoder array does not seem to work
    Temporary patch underneath
    TODO : Values are set at 5000 arbitrarily but it does not reflect one full turn of encoder 
           - value of one full turn has to be determined
  */
  /*
  for(int i = 0; i < numberOfEncoder; i++) {
    encoder[i].write(1600);
  }
  */
  encod1.write(5000u);
  encod2.write(5000u);
  encod3.write(5000u);
  encod4.write(5000u);
}


void loop() 
{
  //Set reference timer
  CURRENT_MICROS = micros();
  
  //Execution time of all of this is approximately 100micros
  //Reset all counters
  counterElectrode = 0;
  counterEncoder = 0;

  //Read all electrode signals
  for(int i = 0; i < NUMBER_OF_ELECTRODES; i++) 
  {
    valueElectrode[i] = analogRead(electrodePin[i]);
  }

  //TODO : Implement encoder array
  /*
  for(int i = 0; i < numberOfEncoder; i++) {
    //valueEncoder[i] = abs(encoder[i].read());
  }
  */
  //Vraisemblablement il accepte pas les tableaux d'encodeurs donc le code suivant est un patch temporaire
  valueEncoder[0] = abs(encod1.read());
  valueEncoder[1] = abs(encod2.read());
  valueEncoder[2] = abs(encod3.read());
  valueEncoder[3] = abs(encod4.read());


  /* Decomposition loop */
  for(int i = 0; i < TOTAL_BYTES_TO_SEND; i++) 
  {
    /* Decompose all electrode values */
    if(counterElectrode < NUMBER_OF_ELECTRODES) 
    {
      /* 
        We decompose valueElectrode in 2 : 
          First value (valuesToSend[i]) is for the LSB - Simply truncate valueElectrode
          Second value (valuesToSend[i+1]) is for the MSB - Right shift of 8 bits and then truncate valueElectrode
      */
      valuesToSend[i]     = static_cast<uint8_t>(valueElectrode[counterElectrode]);
      valuesToSend[i + 1] = static_cast<uint8_t>(right_shift_16_bit(valueElectrode[counterElectrode], 8u));
      
      i = i + 1;
      counterElectrode++;
    }

    /* Decompose all values from encoders */
    else if(counterEncoder < NUMBER_OF_ENCODERS) 
    {
      /* 
        We decompose valueEncoder in 4 : 
          First value is for the LSB - Simply truncate valueEncoder
          Second value is obtained by a 8 bit right shift
          Third value is obtained by a 16 bit right shift
          Fourth value is for the MSB - 24 bit right shift  
      */
      valuesToSend[i] = static_cast<uint8_t>(valueEncoder[counterEncoder]);
      valuesToSend[i + 1] = static_cast<uint8_t>(right_shift_32_bit(valueEncoder[counterEncoder], 8));
      valuesToSend[i + 2] = static_cast<uint8_t>(right_shift_32_bit(valueEncoder[counterEncoder], 16));
      valuesToSend[i + 3] = static_cast<uint8_t>(right_shift_32_bit(valueEncoder[counterEncoder], 24));
  
      i = i + 3;
      counterEncoder++;
    }
  }

    /* Send package of bytes to .py script every interval */
    Serial.write(valuesToSend, TOTAL_BYTES_TO_SEND);
    Serial.send_now();

  /* Wait for a certain interval of time */
  while(micros() < CURRENT_MICROS + WAIT_TIME_MICROS) {} /* Wait [interval]us */
}

