#ifndef IMAGE_PROCESSING_H
#define IMAGE_PROCESSING_H

#include <stdint.h>

/*
Basic image processing functions for RGBA images.
*/

// Create an image with RGBA format (4 bytes per pixel)
uint8_t* create_image_rgba(uint32_t width,
                           uint32_t height);

// Free memory allocated for an image
void free_image_rgba(uint8_t* image_data);

// Copy an image to another image with the same size
void copy_image(uint8_t* dest_image,
                uint8_t* src_image,
                uint32_t width,
                uint32_t height);

// Fill an image with a solid color
void fill_image_rgba(uint8_t* image_data,
                     uint32_t width,
                     uint32_t height,
                     uint8_t r,
                     uint8_t g,
                     uint8_t b,
                     uint8_t a);

// Fill an image with a solid color with AVX2
void fill_image_rgba_avx2(uint8_t* image_data,
                          uint32_t width,
                          uint32_t height,
                          uint8_t r,
                          uint8_t g,
                          uint8_t b,
                          uint8_t a);

// Overlay an image on top of another image with coordinates, blending the pixels
void overlay_image_with_coords(uint8_t* background,
                               uint8_t* overlay,
                               uint32_t bg_width,
                               uint32_t bg_height,
                               uint32_t ov_width, 
                               uint32_t ov_height,
                               int start_x,
                               int start_y);

// Overlay an image on top of another image with coordinates, blending the pixels with AVX2
void overlay_image_with_coords_avx2(uint8_t* background,
                                    uint8_t* overlay,
                                    uint32_t bg_width,
                                    uint32_t bg_height,
                                    uint32_t ov_width,
                                    uint32_t ov_height,
                                    int start_x,
                                    int start_y);

// Copy an image to another image with different sizes, no alpha blending
void copy_image_diff_size_no_alpha(uint8_t* dest_image,
                                   uint32_t dest_width,
                                   uint32_t dest_height,
                                   uint8_t* src_image,
                                   uint32_t src_width,
                                   uint32_t src_height,
                                   int start_x,
                                   int start_y);

// Copy an image to another image with different sizes, no alpha blending with AVX2
void copy_image_diff_size_no_alpha_avx2(uint8_t* dest_image,
                                        uint32_t dest_width,
                                        uint32_t dest_height,
                                        uint8_t* src_image,
                                        uint32_t src_width,
                                        uint32_t src_height,
                                        int start_x,
                                        int start_y);

// Resize an image using nearest neighbor interpolation
void nearest_neighbor_resize(uint8_t* src,
                             uint8_t* dst,
                             uint32_t src_width,
                             uint32_t src_height,
                             uint32_t dst_width,
                             uint32_t dst_height);

// Resize an image using nearest neighbor interpolation with AVX2
void nearest_neighbor_resize_avx2(uint8_t* src,
                                  uint8_t* dst,
                                  uint32_t src_width,
                                  uint32_t src_height,
                                  uint32_t dst_width,
                                  uint32_t dst_height);

#endif
