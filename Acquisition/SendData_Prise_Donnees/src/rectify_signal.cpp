#include "rectify_signal.h"


#define NUM_VALUES_TO_POLL 10

#define CUTOFF 1000
#define SAMPLE_RATE 100

/**
 * @brief 
 * 
 * @param index 
 * @return uint32_t 
 */

uint32_t read_and_filter(uint8_t index)
{
    uint32_t signal[NUM_VALUES_TO_POLL];

    for(uint32_t i = 0; i < NUM_VALUES_TO_POLL; i++)
    {
        signal[i] = analogRead(electrodePin[index]);
    }

    uint32_t y[NUM_VALUES_TO_POLL];
    uint32_t filtered_value = apply_LowpassFilter(signal,y,NUM_VALUES_TO_POLL);

    return filtered_value;
}

uint32_t apply_LowpassFilter(uint32_t *x, uint32_t *y,
               int M) 
{
    int n ;
    
    y[0] = x[0];
    for (n=1; n < M ; n++) {
        y[n] =  -0.51709399 *y[n-1] +  0.75854699*x[n] +0.75854699*x[n-1];
    }
    return x[M-1];
}





uint32_t read_and_rectify(uint8_t index)
{
    uint32_t rectified_value = apply_rms();

    return rectified_value;
}

uint32_t apply_rms(uint32_t* array)
{
    int square = 0;
    // Calculate square.
    for  (int i = 0; i < NUM_VALUES_TO_POLL; i++)
    {
        square += pow(array[i], 2);
    }
      
    // Calculate Mean.
    float mean = (square / NUM_VALUES_TO_POLL);
 
    // Calculate Root.
    float root = sqrt(mean);
    uint32_t rms_value = round(root);
 
    return rms_value;
}


