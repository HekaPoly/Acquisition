/**
 * @file sendData.h
 * @author Équipe Acquisition - Heka
 * @brief 
 * This file is meant to define all variables used to collect electrode and encoder data.
 * @version 0.1
 * @date 2022-06-11
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include <Arduino.h>
#include <Encoder.h>

unsigned long CURRENT_MICROS;
uint32_t WAIT_TIME_MICROS = 500;

/* Values to change depending on tests to be made */
const uint8_t NUMBER_OF_ELECTRODES = 8;
const uint8_t NUMBER_OF_ENCODERS = 4;

/* Total number of bytes to send over serial port */
const uint8_t TOTAL_BYTES_TO_SEND = NUMBER_OF_ELECTRODES*2 + NUMBER_OF_ENCODERS*4;

/* Pin assignement for reading electrode signals */
const uint8_t ELECTRODE_1 = 15;
const uint8_t ELECTRODE_2 = 16;
const uint8_t ELECTRODE_3 = 17;
const uint8_t ELECTRODE_4 = 18;
const uint8_t ELECTRODE_5 = 19;
const uint8_t ELECTRODE_6 = 20;
const uint8_t ELECTRODE_7 = 21;
const uint8_t ELECTRODE_8 = 22;

/* Pin assignement for reading encoder signals */
const uint8_t ENCODER_1_RED     = 2;
const uint8_t ENCODER_1_GREEN   = 3;
const uint8_t ENCODER_2_RED     = 4;
const uint8_t ENCODER_2_GREEN   = 5;
const uint8_t ENCODER_3_RED     = 6;
const uint8_t ENCODER_3_GREEN   = 7;
const uint8_t ENCODER_4_RED     = 8;
const uint8_t ENCODER_4_GREEN   = 9;

/* Create Encoder objects for each encoder used */
Encoder encod1(ENCODER_1_RED, ENCODER_1_GREEN);
Encoder encod2(ENCODER_2_RED, ENCODER_2_GREEN);
Encoder encod3(ENCODER_3_RED, ENCODER_3_GREEN);
Encoder encod4(ENCODER_4_RED, ENCODER_4_GREEN);

/* Create arrays to contain values of electrodes and encoders*/
uint32_t electrodePin[8] = {ELECTRODE_1, ELECTRODE_2, ELECTRODE_3, ELECTRODE_4, 
                            ELECTRODE_5, ELECTRODE_6, ELECTRODE_7, ELECTRODE_8};
Encoder encoder[4] = {encod1, encod2, encod3, encod4};

/* Count values to indicate when to stop sending data */
uint8_t counterElectrode = 0;
uint8_t counterEncoder = 0;

/* 
Arrays to send on serial port torwards .py program 
Encoder returns long which is 32 bits on TeensyLC (not 64)
*/
uint16_t valueElectrode[NUMBER_OF_ELECTRODES];
uint32_t valueEncoder[NUMBER_OF_ENCODERS];

/* 2 bytes for electrodes - 4 bytes for encoders */
uint8_t valuesToSend[TOTAL_BYTES_TO_SEND];