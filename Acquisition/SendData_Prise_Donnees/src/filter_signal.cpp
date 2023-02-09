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
uint32_t filter_and_rectify_signal(uint8_t index)
{
    uint32_t values_sample[NUM_VALUES_TO_POLL];

    /* Créer une fonction de lecture de valeur d'une électrode ici */

    /* Filtrer le signal ici */

    /* Appeler fonction de rectification de signal ici */

    /* Retourner la valeur lue pour l'électrode */
}