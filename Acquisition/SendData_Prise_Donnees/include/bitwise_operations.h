/**
 * @file
 * bitwise_operations.h
 * 
 * @author
 * Équipe Acquisition - Heka
 * 
 * @brief
 * This file is meant to define functions for bitwise operations
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#ifndef _BITWISE_OPERATIONS_H_
#define _BITWISE_OPERATIONS_H_

#include <stdio.h>
#include <stdint.h>

/* FUNCTION PROTOTYPES */
/* Mask functions */
uint8_t  mask_uint8(uint8_t number, uint8_t mask);
uint16_t mask_uint16(uint16_t number, uint16_t mask);
uint32_t mask_uint32(uint32_t number, uint32_t mask);
uint64_t mask_uint64(uint64_t number, uint64_t mask);

/* Left bitwise shifting operations */
uint8_t  left_shift_uint8(uint8_t number, uint8_t bits_to_shift);
uint16_t left_shift_uint16(uint16_t number, uint16_t bits_to_shift);
uint32_t left_shift_uint32(uint32_t number, uint32_t bits_to_shift);
uint64_t left_shift_uint64(uint64_t number, uint64_t bits_to_shift);

/* Right bitwise shifting operations */
uint8_t  right_shift_uint8(uint8_t number, uint8_t bits_to_shift);
uint16_t right_shift_uint16(uint16_t number, uint16_t bits_to_shift);
uint32_t right_shift_uint32(uint32_t number, uint32_t bits_to_shift);
uint64_t right_shift_uint64(uint64_t number, uint64_t bits_to_shift);

#endif /* _BITWISE_OPERATIONS_H */