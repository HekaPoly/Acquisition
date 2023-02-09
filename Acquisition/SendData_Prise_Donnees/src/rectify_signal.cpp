/**
 * @file 
 * rectify_signal.cpp
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file implements the filtered EMG signal rectification functions
 * 
 * @copyright Copyright Heka (c) 2023
 * 
 */

#include "rectify_signal.h"

/* FUNCTIONS */
uint32_t rectify(uint8_t index, uint32_t filtered_signal_sample[NUM_VALUES_TO_POLL])
{
    double square = 0;

    for (int i = 0; i < NUM_VALUES_TO_POLL; i++)
    {
        square += pow(filtered_signal_sample[i], POWER_TWO);
    }

    float mean = (square / NUM_VALUES_TO_POLL);
    float root = sqrt(mean);

    uint32_t rms_value = round(root);

    return rms_value;
}


