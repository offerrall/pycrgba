#ifndef BASIC_IMAGE_LIB_H
#define BASIC_IMAGE_LIB_H

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <immintrin.h>
#include <malloc.h>

#define ALIGNMENT 32


uint8_t* create_image_rgba(uint32_t width, uint32_t height);
void free_image_rgba(uint8_t* image_data);
void fill_image_rgba(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
void fill_image_rgba_avx2(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
void blend_coords(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int start_x, int start_y);
void blend_avx2(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int start_x, int start_y);
void blit_image(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int start_x, int start_y);
void blit_image_avx2(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int start_x, int start_y);
void nearest_neighbor_resize(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);
void nearest_neighbor_resize_avx2(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);

#endif