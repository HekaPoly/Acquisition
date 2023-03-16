/**
 * @file 
 * main.cpp
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file contains the setup for the uC program running to collect data from electrodes and encod_ers.
 * It also contains the main loop of the program. This main loop runs every WAIT_TIME_MICROS microseconds.
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "main.h"
#include "bitwise_operations.h"
#include "rectify_signal.h"
#include "filter_signal.h"

/* FUNCTIONS */
/**
 * @brief
 * Checks for a serial command sent by the GUI
 * 
 * @return
 * int32_t Reference value for encod_er
 */
void check_serial_read_buffer(void)
{
  if (Serial.available() > 0)
  {
    int32_t command = Serial.read();
    
    if (command == 'A')
    {
      encod_1.write(0u);
      encod_2.write(0u);
      encod_3.write(0u);
      encod_4.write(0u);
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
 *  First value is for the LSB - Simply truncate values_electrode
 *  Second value is for the MSB - Right shift of 8 bits and then truncate values_electrode
 * We decompose encod_er value in 4: 
 *  First value is for the LSB - Simply truncate values_encoder
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

  uint8_t counter_electrode = 0;
  uint8_t counter_encoder = 0;

  /* Read all electrode signals and encod_er values */
  for (int i = 0; i < NUMBER_OF_ELECTRODES; i++) 
  {
    for (int j = 0; j<NUM_VALUES_TO_FILTER; j++)
    {
      values_to_filter[j] = analogRead(electrode_pin[i]);
      filter_input[0]=values_to_filter[j];
      filter(filter_input,filter_output);

      filtered_signal[j]=filter_output[0];
    }
    values_electrode[i] = rectify(filtered_signal);
  }

  // for (int j = 0; j<NUM_VALUES_TO_FILTER; j++){

  // values_to_filter[NUM_VALUES_TO_FILTER] = analogRead(electrode_pin[j]);
  
  // }


  values_encoder[0] = abs(encod_1.read());
  values_encoder[1] = abs(encod_2.read());
  values_encoder[2] = abs(encod_3.read());
  values_encoder[3] = abs(encod_4.read());


  /* Decomposition loop */
  for (int i = 0; i < TOTAL_BYTES_TO_SEND; i++) 
  {
    /* Decompose all electrode values */
    if (counter_electrode < NUMBER_OF_ELECTRODES) 
    {
      values_to_send[i]     = values_electrode[counter_electrode];
      values_to_send[i + 1] = right_shift_uint16(values_electrode[counter_electrode], 8u);
      
      i = i + 1;
      counter_electrode++;
    }

    /* Decompose all values from encod_ers */
    else if (counter_encoder < NUMBER_OF_ENCODERS) 
    {
      values_to_send[i] = values_encoder[counter_encoder];
      values_to_send[i + 1] = right_shift_uint32(values_encoder[counter_encoder], 8u);
      values_to_send[i + 2] = right_shift_uint32(values_encoder[counter_encoder], 16u);
      values_to_send[i + 3] = right_shift_uint32(values_encoder[counter_encoder], 24u);

      i = i + 3;
      counter_encoder++;
    }
  }

  /* Send package of bytes to .py script every interval */
  Serial.write(values_to_send, TOTAL_BYTES_TO_SEND);
  Serial.send_now();

  /* Wait [interval]us */
  while (micros() < (CURRENT_MICROS + WAIT_TIME_MICROS)) 
  {
    /* Waiting while doing nothing */
  }
}