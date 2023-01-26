#include "rectify_signal.h"
#include "sendData.h"
void read_and_rectify(uint32_t index)
{
    uint32_t array[10];

    for(uint32_t i = 0; i < 11; i++)
    {
        array[i] = analogRead(electrodePin[index]);
    }

    apply_rms(array);
}

int apply_rms(uint32_t array[], uint32_t n)
{ 
    int square = 0;
    float mean = 0.0; 
    float root = 0.0;
    int x = 0;
    // Calculate square.
   for  (int x = 0; x < n; x++) ;
   {
        square += pow(array[x], 2);}
      
   // Calculate Mean.
    mean = (square / n);
 
    // Calculate Root.
    root = sqrt(mean);
    root = round(root);
 
    return root;
    }
