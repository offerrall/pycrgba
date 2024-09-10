#ifndef BASIC_IMAGE_LIB_H
#define BASIC_IMAGE_LIB_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifdef _WIN32
#include <malloc.h>
#endif

#if defined(__x86_64__) || defined(_M_X64)
#include <immintrin.h>
#endif

#define ALIGNMENT 32

#if defined(__ARM_NEON)
#include <arm_neon.h>
#endif

#if defined(__AVX2__)
#define HAS_AVX2 1
#else
#define HAS_AVX2 0
#endif

uint8_t* create_image_rgba(uint32_t width, uint32_t height);
void free_image_rgba(uint8_t* image_data);
void fill_image_rgba(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
void fill_image_rgba_avx2(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
void fill_image_rgba_neon(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
void blend(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y);
void blend_avx2(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y);
void blend_neon(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y);
void blit(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int32_t start_x, int32_t start_y);
void blit_avx2(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int32_t start_x, int32_t start_y);
void blit_neon(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int32_t start_x, int32_t start_y);
void blit_same_size(uint8_t* src, uint8_t* dst, uint32_t width, uint32_t height, uint32_t channels);
void nearest_neighbor_resize(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);
void nearest_neighbor_resize_avx2(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);
void nearest_neighbor_resize_neon(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);

#endif