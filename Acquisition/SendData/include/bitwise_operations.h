/**
 * @file bitwise_operations.h
 * @author Équipe Acquisition - Heka
 * @brief 
 * This file is meant to define functions for bitwise operations.
 * @version 0.1
 * @date 2022-06-11
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "stdio.h"
#include "stdint.h"

/* Mask functions */
uint8_t  mask_8_bit(uint8_t n1, uint8_t mask);
uint16_t mask_16_bit(uint16_t n1, uint16_t mask);
uint32_t mask_32_bit(uint32_t n1, uint32_t mask);
uint64_t mask_64_bit(uint64_t n1, uint64_t mask);

/* Left bitwise shifting operations */
uint8_t  left_shift_8_bit(uint8_t n1, uint8_t left_shit);
uint16_t left_shift_16_bit(uint16_t n1, uint16_t left_shit);
uint32_t left_shift_32_bit(uint32_t n1, uint32_t left_shit);
uint64_t left_shift_64_bit(uint64_t n1, uint64_t left_shit);

/* Right bitwise shifting operations */
uint8_t  right_shift_8_bit(uint8_t n1, uint8_t right_shift);
uint16_t right_shift_16_bit(uint16_t n1, uint16_t right_shift);
uint32_t right_shift_32_bit(uint32_t n1, uint32_t right_shift);
uint64_t right_shift_64_bit(uint64_t n1, uint64_t right_shift);