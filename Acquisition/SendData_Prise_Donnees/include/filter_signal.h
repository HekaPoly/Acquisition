/**
 * @file 
 * rectify_signal.h
 * 
 * @author
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file is meant to define all useful information for signal filtering
 * 
 * @copyright Copyright Heka (c) 2023
 * 
 */

#ifndef _FILTER_SIGNAL_H_
#define _FILTER_SIGNAL_H_

#include <Arduino.h>

/* CONSTANTS */
#define CUTOFF 1000
#define SAMPLE_RATE 100

/* FUNCTION PROTOTYPES */
uint32_t filter_and_rectify_signal(uint8_t index);

#endif /* _FILTER_SIGNAL_H_ */
