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

/* FUNCTION PROTOTYPES */
uint32_t read_and_rectify(uint8_t index);
uint32_t apply_rms(uint32_t array[]);

#endif /* _RECTIFY_SIGNAL_H_ */