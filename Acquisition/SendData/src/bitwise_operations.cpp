/**
 * @file bitwise_operations.cpp
 * @author Équipe Acquisition - Heka
 * @brief 
 * @version 0.1
 * @date 2022-06-11
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "bitwise_operations.h"

uint8_t mask_8_bit(uint8_t n1, uint8_t mask)
{
    return (uint8_t)(n1 & mask);
}

uint16_t mask_16_bit(uint16_t n1, uint16_t mask)
{
    return (uint16_t)(n1 & mask);
}

uint32_t mask_32_bit(uint32_t n1, uint32_t mask)
{
    return (uint32_t)(n1 & mask);
}

uint64_t mask_64_bit(uint64_t n1, uint64_t mask)
{
    return (uint64_t)(n1 & mask);
}

uint8_t left_shift_8_bit(uint8_t n1, uint8_t left_shift)
{
    return (uint8_t)(n1 << left_shift);
}

uint16_t left_shift_16_bit(uint16_t n1, uint16_t left_shift)
{
    return (uint16_t)(n1 << left_shift);
}

uint32_t left_shift_32_bit(uint32_t n1, uint32_t left_shift)
{
    return (uint32_t)(n1 << left_shift);
}

uint64_t left_shift_64_bit(uint64_t n1, uint64_t left_shift)
{
    return (uint64_t)(n1 << left_shift);
}

uint8_t right_shift_8_bit(uint8_t n1, uint8_t right_shift)
{
    return (uint8_t)(n1 >> right_shift);
}

uint16_t right_shift_16_bit(uint16_t n1, uint16_t right_shift)
{
    return (uint16_t)(n1 >> right_shift);
}

uint32_t right_shift_32_bit(uint32_t n1, uint32_t right_shift)
{
    return (uint32_t)(n1 >> right_shift);
}

uint64_t right_shift_64_bit(uint64_t n1, uint64_t right_shift)
{
    return (uint64_t)(n1 >> right_shift);
}
