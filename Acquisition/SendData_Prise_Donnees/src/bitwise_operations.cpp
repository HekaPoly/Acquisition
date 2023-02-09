/**
 * @file 
 * bitwise_operations.cpp
 * 
 * @author 
 * Équipe Acquisition - Heka
 * 
 * @brief 
 * This file implements bitwise operations to comply with MISRA-C 2012 standard
 * 
 * @copyright Copyright Heka (c) 2022
 * 
 */

#include "bitwise_operations.h"

/* Functions */
/**
 * @brief Performs a mask operation on a uint8_t
 * 
 * @param[in] number Byte sized number
 * @param[in] mask Byte sized mask
 * @return uint8_t The result of the mask operation
 */
uint8_t mask_uint8(uint8_t number, uint8_t mask)
{
    return (uint8_t)(number & mask);
}

/**
 * @brief Performs a mask operation on a uint16_t
 * 
 * @param[in] number 2 byte sized number
 * @param[in] mask 2 byte sized mask
 * @return uint16_t The result of the mask operation
 */
uint16_t mask_uint16(uint16_t number, uint16_t mask)
{
    return (uint16_t)(number & mask);
}

/**
 * @brief Performs a mask operation on a uint32_t
 * 
 * @param[in] number 4 byte sized number
 * @param[in] mask 4 byte sized mask
 * @return uint32_t The result of the mask operation
 */
uint32_t mask_uint32(uint32_t number, uint32_t mask)
{
    return (uint32_t)(number & mask);
}

/**
 * @brief Performs a mask operation on a uint64_t
 * 
 * @param[in] number 8 byte sized number
 * @param[in] mask 8 byte sized mask
 * @return uint64_t The result of the mask operation
 */
uint64_t mask_uint64(uint64_t number, uint64_t mask)
{
    return (uint64_t)(number & mask);
}

/**
 * @brief Performs a left shift on a uint8_t
 * 
 * @param[in] number Byte sized number
 * @param[in] bits_to_shift Byte sized places to shift
 * @return uint8_t The result of the left shift
 */
uint8_t left_shift_uint8(uint8_t number, uint8_t bits_to_shift)
{
    return (uint8_t)(number << bits_to_shift);
}

/**
 * @brief Performs a left shift on a uint16_t
 * 
 * @param[in] number 2 byte sized number
 * @param[in] bits_to_shift 2 byte sized places to shift
 * @return uint16_t The result of the left shift
 */
uint16_t left_shift_uint16(uint16_t number, uint16_t bits_to_shift)
{
    return (uint16_t)(number << bits_to_shift);
}

/**
 * @brief Performs a left shift on a uint32_t
 * 
 * @param[in] number 4 byte sized number
 * @param[in] bits_to_shift 4 byte sized places to shift
 * @return uint32_t The result of the left shift
 */
uint32_t left_shift_uint32(uint32_t number, uint32_t bits_to_shift)
{
    return (uint32_t)(number << bits_to_shift);
}

/**
 * @brief Performs a left shift on a uint64_t
 * 
 * @param[in] number 8 byte sized number
 * @param[in] bits_to_shift 8 byte sized places to shift
 * @return uint64_t The result of the left shift
 */
uint64_t left_shift_uint64(uint64_t number, uint64_t bits_to_shift)
{
    return (uint64_t)(number << bits_to_shift);
}

/**
 * @brief Performs a right shift on a uint8_t
 * 
 * @param[in] number Byte sized number
 * @param[in] bits_to_shift Byte sized places to shift
 * @return uint8_t The result of the right shift
 */
uint8_t right_shift_uint8(uint8_t number, uint8_t bits_to_shift)
{
    return (uint8_t)(number >> bits_to_shift);
}

/**
 * @brief Performs a right shift on a uint16_t
 * 
 * @param[in] number 2 byte sized number
 * @param[in] bits_to_shift 2 byte sized places to shift
 * @return uint16_t The result of the right shift
 */
uint16_t right_shift_uint16(uint16_t number, uint16_t bits_to_shift)
{
    return (uint16_t)(number >> bits_to_shift);
}

/**
 * @brief Performs a right shift on a uint32_t
 * 
 * @param[in] number 4 byte sized number
 * @param[in] bits_to_shift 4 byte sized places to shift
 * @return uint32_t The result of the right shift
 */
uint32_t right_shift_uint32(uint32_t number, uint32_t bits_to_shift)
{
    return (uint32_t)(number >> bits_to_shift);
}

/**
 * @brief Performs a right shift on a uint64_t
 * 
 * @param[in] number 8 byte sized number
 * @param[in] bits_to_shift 8 byte sized places to shift
 * @return uint64_t The result of the right shift
 */
uint64_t right_shift_uint64(uint64_t number, uint64_t bits_to_shift)
{
    return (uint64_t)(number >> bits_to_shift);
}
