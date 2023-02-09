/**
 * @file
 * rectify_signal.h
 * 
 * @author
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file is meant to define all useful information for signal rectification
 * 
 * @copyright Copyright Heka (c) 2023
 * 
 */

#ifndef _RECTIFY_SIGNAL_H_
#define _RECTIFY_SIGNAL_H_

#include <Arduino.h>

/* CONSTANTS */
#define NUM_VALUES_TO_POLL 10
#define POWER_TWO 2

/* FUNCTION PROTOTYPES */
uint32_t rectify(uint8_t index, uint32_t filtered_signal_sample[NUM_VALUES_TO_POLL]);

#endif /* _RECTIFY_SIGNAL_H_ */