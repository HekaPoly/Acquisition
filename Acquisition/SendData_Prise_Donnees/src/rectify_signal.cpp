#include "rectify_signal.h"
#include "sendData.h"

#define NUM_VALUES_TO_POLL 10

/**
 * @brief 
 * 
 * @param index 
 * @return uint32_t 
 */
uint32_t read_and_rectify(uint8_t index)
{
    uint32_t array[NUM_VALUES_TO_POLL];

    for(uint32_t i = 0; i < NUM_VALUES_TO_POLL; i++)
    {
        array[i] = analogRead(electrodePin[index]);
    }

    uint32_t rectified_value = apply_rms(array);

    return rectified_value;
}

uint32_t apply_rms(uint32_t array[])
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
