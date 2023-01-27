/**
 * @file rectify_signal.h
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

uint32_t read_and_rectify(uint8_t index);
uint32_t apply_rms(uint32_t array[]);