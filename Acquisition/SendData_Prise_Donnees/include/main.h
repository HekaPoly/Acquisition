/**
 * @file 
 * sendData.h
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file is meant to define all variables used to collect electrode and encoder data
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#ifndef _MAIN_H_
#define _MAIN_H_

#include <Arduino.h>
#include <Encoder.h>

/* CONSTANTS */
unsigned long CURRENT_MICROS;
#define WAIT_TIME_MICROS 2000

/* Values to change depending on tests to be made */
#define NUMBER_OF_ELECTRODES 8
#define NUMBER_OF_ENCODERS 4

/* Total number of bytes to send over serial port */
#define TOTAL_BYTES_TO_SEND ((NUMBER_OF_ELECTRODES * 2) + (NUMBER_OF_ENCODERS * 4))

/* Pin assignement for reading electrode signals */
#define ELECTRODE_1 15
#define ELECTRODE_2 16
#define ELECTRODE_3 17
#define ELECTRODE_4 18
#define ELECTRODE_5 19
#define ELECTRODE_6 20
#define ELECTRODE_7 21
#define ELECTRODE_8 22

/* Pin assignement for reading encoder signals */
#define ENCODER_1_RED     2
#define ENCODER_1_GREEN   3
#define ENCODER_2_RED     4
#define ENCODER_2_GREEN   5
#define ENCODER_3_RED     6
#define ENCODER_3_GREEN   7
#define ENCODER_4_RED     8
#define ENCODER_4_GREEN   9

/* Reference value for encoders */
#define ENCODER_REF_VALUE 0


/* ARRAYS AND STRUCTURES */
/* Create Encoder objects for each encoder used */
Encoder encod_1(ENCODER_1_RED, ENCODER_1_GREEN);
Encoder encod_2(ENCODER_2_RED, ENCODER_2_GREEN);
Encoder encod_3(ENCODER_3_RED, ENCODER_3_GREEN);
Encoder encod_4(ENCODER_4_RED, ENCODER_4_GREEN);

/* Create arrays to contain values of electrodes and encoders */
uint32_t electrode_pin[NUMBER_OF_ELECTRODES] = {ELECTRODE_1, ELECTRODE_2, ELECTRODE_3, ELECTRODE_4, 
                            ELECTRODE_5, ELECTRODE_6, ELECTRODE_7, ELECTRODE_8};
Encoder encoders[NUMBER_OF_ENCODERS] = {encod_1, encod_2, encod_3, encod_4};

/* 
    Arrays to send on serial port torwards .py program 
    Encoder returns long which is 32 bits on TeensyLC (not 64)
*/
uint16_t values_electrode[NUMBER_OF_ELECTRODES];
uint32_t values_encoder[NUMBER_OF_ENCODERS];

/* 2 bytes for electrodes - 4 bytes for encoders */
uint8_t values_to_send[TOTAL_BYTES_TO_SEND];


/* FUNCTION PROTOTYPES */
void check_serial_read_buffer(void);

#endif /* _MAIN_H_ */