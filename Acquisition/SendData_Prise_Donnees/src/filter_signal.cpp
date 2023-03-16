/**
 * @file 
 * filter_signal.cpp
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file implements the discrete transfer functions of the numerical filters applied
 * to the raw EMG signals
 * 
 * @copyright Copyright Heka (c) 2023
 * 
 */

#include "filter_signal.h"
#include "rectify_signal.h"

/* CONSTANTS */

/* FUNCTIONS */

void filter(float* input, float* output)
{

   output[0]=1.56450399*output[1]+ -0.64366232*output[2]+0.01978958*input[0]+0.03957917*input[1];



   output[2]=output[1];
   output[1]=output[0];
   input[1]=input[0];



    
}


