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
#define NUM_VALUES_TO_POLL 3
#define POWER_TWO 2

/* FUNCTION PROTOTYPES */
uint16_t rectify(float* filtered_signal_sample);

#endif /* _RECTIFY_SIGNAL_H_ */