/**
 * @file 
 * main.cpp
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file contains the setup for the uC program running to collect data from electrodes and encoders.
 * It also contains the main loop of the program. This main loop runs every WAIT_TIME_MICROS microseconds.
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "sendData.h"
#include "bitwise_operations.h"

/**
 * @brief
 * Checks for a serial command sent by the GUI
 * 
 * @return
 * int32_t Reference value for encoder
 */
void check_serial_read_buffer(void)
{
  if (Serial.available() > 0)
  {
    int32_t command = Serial.read();
    
    if (command == 'A')
    {
      encod1.write(0u);
      encod2.write(0u);
      encod3.write(0u);
      encod4.write(0u);
    }
  }
}

/**
 * @brief
 * Setup function for looping code. 
 * Sets baudrate to 1M bits/second and analog resolution to 12 bits (values go from 0 to (2^12 - 1))
 * 
 */
void setup()
{
  Serial.begin(1000000u);
  analogReadResolution(12u);
}

/**
 * @brief 
 * Main loop for the data acquisition uC.
 * @note 
 * We decompose electrode value in 2 bytes: 
 *  First value is for the LSB - Simply truncate valueElectrode
 *  Second value is for the MSB - Right shift of 8 bits and then truncate valueElectrode
 * We decompose encoder value in 4: 
 *  First value is for the LSB - Simply truncate valueEncoder
 *  Second value is obtained by a 8 bit right shift
 *  Third value is obtained by a 16 bit right shift
 *  Fourth value is for the MSB - 24 bit right shift
 * 
 * The execution time of the whole loop is approximtely 100us (not counting the wait time).
 * 
 */
void loop()
{
  /* Check for specific instructions */
  check_serial_read_buffer();

  /* Set reference timer */
  CURRENT_MICROS = micros();

  /* Reset all counters */
  counterElectrode = 0;
  counterEncoder = 0;

  /* Read all electrode signals and encoder values */
  for (int i = 0; i < NUMBER_OF_ELECTRODES; i++) 
  {
    valueElectrode[i] = analogRead(electrodePin[i]);
  }

  

  valueEncoder[0] = abs(encod1.read());
  valueEncoder[1] = abs(encod2.read());
  valueEncoder[2] = abs(encod3.read());
  valueEncoder[3] = abs(encod4.read());


  /* Decomposition loop */
  for (int i = 0; i < TOTAL_BYTES_TO_SEND; i++) 
  {
    /* Decompose all electrode values */
    if (counterElectrode < NUMBER_OF_ELECTRODES) 
    {
      valuesToSend[i]     = valueElectrode[counterElectrode];
      valuesToSend[i + 1] = right_shift_uint16(valueElectrode[counterElectrode], 8u);
      
      i = i + 1;
      counterElectrode++;
    }

    /* Decompose all values from encoders */
    else if (counterEncoder < NUMBER_OF_ENCODERS) 
    {
      valuesToSend[i] = valueEncoder[counterEncoder];
      valuesToSend[i + 1] = right_shift_uint32(valueEncoder[counterEncoder], 8u);
      valuesToSend[i + 2] = right_shift_uint32(valueEncoder[counterEncoder], 16u);
      valuesToSend[i + 3] = right_shift_uint32(valueEncoder[counterEncoder], 24u);

      i = i + 3;
      counterEncoder++;
    }
  }

  /* Send package of bytes to .py script every interval */
  Serial.write(valuesToSend, TOTAL_BYTES_TO_SEND);
  Serial.send_now();

  /* Wait [interval]us */
  while (micros() < (CURRENT_MICROS + WAIT_TIME_MICROS)) 
  {
    /* Waiting while doing nothing */
  }
}

