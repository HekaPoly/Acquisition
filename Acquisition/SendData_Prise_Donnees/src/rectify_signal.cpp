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
// on rentre un tableau de taille 4* Nb electrodes on veut appliquer rms  en mettant une fonction 

uint16_t rectify(float* filtered_signal_sample)
{
    double square = 0.0;

    for (int i = 0; i < NUM_VALUES_TO_POLL; i++)
    {
        square += pow(filtered_signal_sample[i], POWER_TWO);
    }

    double mean = (square / NUM_VALUES_TO_POLL);
    double root = sqrt(mean);

    uint32_t rms_value = round(root);

    return rms_value;
}


