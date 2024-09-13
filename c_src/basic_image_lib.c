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

#if defined(__AVX2__)
#define HAS_AVX2 1
#else
#define HAS_AVX2 0
#endif

#if defined(__ARM_NEON)
#include <arm_neon.h>
#endif

uint8_t* create_image_rgba(uint32_t width, uint32_t height) {
    size_t size = width * height * 4;
    uint8_t* image_data;

    #ifdef _WIN32
    image_data = (uint8_t*)_aligned_malloc(size, ALIGNMENT);
    #else
    #if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 201112L
    image_data = aligned_alloc(ALIGNMENT, (size + ALIGNMENT - 1) & ~(ALIGNMENT - 1));
    #else
    if (posix_memalign((void**)&image_data, ALIGNMENT, size) != 0) {
        image_data = NULL;
    }
    #endif
    #endif

    return image_data;
}

void free_image_rgba(uint8_t* image_data) {
    #ifdef _WIN32
    _aligned_free(image_data);
    #else
    free(image_data);
    #endif
}

void fill_image_rgba(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
    if (image_data == NULL) {
        printf("Image data is NULL\n");
        return;
    }

    uint32_t total_pixels = width * height;
    for (uint32_t i = 0; i < total_pixels; i++) {
        image_data[i * 4] = r;
        image_data[i * 4 + 1] = g;
        image_data[i * 4 + 2] = b;
        image_data[i * 4 + 3] = a;
    }
}

#if HAS_AVX2
void fill_image_rgba_avx2(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
    if (image_data == NULL) {
        printf("Image data is NULL\n");
        return;
    }

    uint32_t total_pixels = width * height;
    uint32_t avx2_blocks = total_pixels / 8;
    uint32_t remainder = total_pixels % 8;

    __m256i rgba = _mm256_set_epi8(a, b, g, r, a, b, g, r, a, b, g, r, a, b, g, r,
                                   a, b, g, r, a, b, g, r, a, b, g, r, a, b, g, r);

    for (uint32_t i = 0; i < avx2_blocks; i++) {
        _mm256_storeu_si256((__m256i*)&image_data[i * 32], rgba);
    }

    for (uint32_t i = avx2_blocks * 8; i < total_pixels; i++) {
        image_data[i * 4]     = r;
        image_data[i * 4 + 1] = g;
        image_data[i * 4 + 2] = b;
        image_data[i * 4 + 3] = a;
    }
}
#else
void fill_image_rgba_avx2(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
    fill_image_rgba(image_data, width, height, r, g, b, a);
}
#endif

#if defined(__ARM_NEON)
void fill_image_rgba_neon(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
    if (image_data == NULL) {
        printf("Image data is NULL\n");
        return;
    }

    uint32_t total_pixels = width * height;
    uint32_t neon_blocks = total_pixels / 4;
    uint32_t remainder = total_pixels % 4;

    uint32x4_t rgba = vdupq_n_u32((a << 24) | (b << 16) | (g << 8) | r);

    for (uint32_t i = 0; i < neon_blocks; i++) {
        vst1q_u32((uint32_t*)&image_data[i * 16], rgba);
    }

    for (uint32_t i = neon_blocks * 4; i < total_pixels; i++) {
        image_data[i * 4]     = r;
        image_data[i * 4 + 1] = g;
        image_data[i * 4 + 2] = b;
        image_data[i * 4 + 3] = a;
    }
}
#else
void fill_image_rgba_neon(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a) {
    fill_image_rgba(image_data, width, height, r, g, b, a);
}
#endif

void blend(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height,
            uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y) {
    if (background == NULL || overlay == NULL) {
        printf("Background or overlay image is NULL\n");
        return;
    }

    for (uint32_t y = 0; y < ov_height; y++) {
        int bg_y = start_y + y;
        if (bg_y < 0 || bg_y >= bg_height) {
            continue;
        }

        uint32_t bg_index = (bg_y * bg_width + start_x) * 4;
        uint32_t overlay_index = y * ov_width * 4;

        for (uint32_t x = 0; x < ov_width; x++) {
            int bg_x = start_x + x;
            if (bg_x < 0 || bg_x >= bg_width) {
                continue;
            }

            uint32_t bg_pixel_index = bg_index + x * 4;
            uint32_t ov_pixel_index = overlay_index + x * 4;

            uint8_t r1 = background[bg_pixel_index];
            uint8_t g1 = background[bg_pixel_index + 1];
            uint8_t b1 = background[bg_pixel_index + 2];
            uint8_t a1 = background[bg_pixel_index + 3];

            uint8_t r2 = overlay[ov_pixel_index];
            uint8_t g2 = overlay[ov_pixel_index + 1];
            uint8_t b2 = overlay[ov_pixel_index + 2];
            uint8_t a2 = overlay[ov_pixel_index + 3];

            if (a2 == 0) {
                continue;
            } else if (a2 == 255) {
                background[bg_pixel_index] = r2;
                background[bg_pixel_index + 1] = g2;
                background[bg_pixel_index + 2] = b2;
                background[bg_pixel_index + 3] = a2;
            } else {
                uint32_t inv_alpha = 255 - a2;
                background[bg_pixel_index]     = (r2 * a2 + r1 * inv_alpha) / 255;
                background[bg_pixel_index + 1] = (g2 * a2 + g1 * inv_alpha) / 255;
                background[bg_pixel_index + 2] = (b2 * a2 + b1 * inv_alpha) / 255;
                background[bg_pixel_index + 3] = a2 + (a1 * inv_alpha) / 255;
            }
        }
    }
}

#if HAS_AVX2
void blend_avx2(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height,
                uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y) {
    if (background == NULL || overlay == NULL) {
        printf("Background or overlay image is NULL\n");
        return;
    }

    for (uint32_t y = 0; y < ov_height; y++) {
        int bg_y = start_y + y;
        if (bg_y < 0 || bg_y >= bg_height) {
            continue;
        }

        uint32_t bg_index = (bg_y * bg_width + start_x) * 4;
        uint32_t overlay_index = y * ov_width * 4;

        for (uint32_t x = 0; x < ov_width - 7; x += 8) {
            int bg_x = start_x + x;
            if (bg_x < 0 || bg_x >= bg_width) {
                bg_index += 32;
                overlay_index += 32;
                continue;
            }

            __m256i bg_pixels = _mm256_loadu_si256((__m256i*)&background[bg_index]);
            __m256i ov_pixels = _mm256_loadu_si256((__m256i*)&overlay[overlay_index]);

            __m256i alpha = _mm256_and_si256(_mm256_srli_epi32(ov_pixels, 24), _mm256_set1_epi32(0xFF));
            __m256i inv_alpha = _mm256_sub_epi32(_mm256_set1_epi32(255), alpha);

            __m256i bg_r = _mm256_and_si256(bg_pixels, _mm256_set1_epi32(0xFF));
            __m256i bg_g = _mm256_and_si256(_mm256_srli_epi32(bg_pixels, 8), _mm256_set1_epi32(0xFF));
            __m256i bg_b = _mm256_and_si256(_mm256_srli_epi32(bg_pixels, 16), _mm256_set1_epi32(0xFF));
            __m256i bg_a = _mm256_and_si256(_mm256_srli_epi32(bg_pixels, 24), _mm256_set1_epi32(0xFF));

            __m256i ov_r = _mm256_and_si256(ov_pixels, _mm256_set1_epi32(0xFF));
            __m256i ov_g = _mm256_and_si256(_mm256_srli_epi32(ov_pixels, 8), _mm256_set1_epi32(0xFF));
            __m256i ov_b = _mm256_and_si256(_mm256_srli_epi32(ov_pixels, 16), _mm256_set1_epi32(0xFF));

            __m256i r = _mm256_srli_epi32(_mm256_add_epi32(_mm256_mullo_epi32(ov_r, alpha), _mm256_mullo_epi32(bg_r, inv_alpha)), 8);
            __m256i g = _mm256_srli_epi32(_mm256_add_epi32(_mm256_mullo_epi32(ov_g, alpha), _mm256_mullo_epi32(bg_g, inv_alpha)), 8);
            __m256i b = _mm256_srli_epi32(_mm256_add_epi32(_mm256_mullo_epi32(ov_b, alpha), _mm256_mullo_epi32(bg_b, inv_alpha)), 8);
            __m256i a = _mm256_add_epi32(alpha, _mm256_srli_epi32(_mm256_mullo_epi32(bg_a, inv_alpha), 8));

            __m256i result = _mm256_or_si256(
                _mm256_or_si256(
                    _mm256_or_si256(r, _mm256_slli_epi32(g, 8)),
                    _mm256_slli_epi32(b, 16)
                ),
                _mm256_slli_epi32(a, 24)
            );

            _mm256_storeu_si256((__m256i*)&background[bg_index], result);

            bg_index += 32;
            overlay_index += 32;
        }

        for (uint32_t x = ov_width - (ov_width % 8); x < ov_width; x++) {
            int bg_x = start_x + x;
            if (bg_x < 0 || bg_x >= bg_width) {
                continue;
            }

            uint32_t bg_pixel_index = (bg_y * bg_width + bg_x) * 4;
            uint32_t ov_pixel_index = (y * ov_width + x) * 4;

            uint8_t r1 = background[bg_pixel_index];
            uint8_t g1 = background[bg_pixel_index + 1];
            uint8_t b1 = background[bg_pixel_index + 2];
            uint8_t a1 = background[bg_pixel_index + 3];

            uint8_t r2 = overlay[ov_pixel_index];
            uint8_t g2 = overlay[ov_pixel_index + 1];
            uint8_t b2 = overlay[ov_pixel_index + 2];
            uint8_t a2 = overlay[ov_pixel_index + 3];

            if (a2 == 0) {
                continue;
            } else if (a2 == 255) {
                background[bg_pixel_index] = r2;
                background[bg_pixel_index + 1] = g2;
                background[bg_pixel_index + 2] = b2;
                background[bg_pixel_index + 3] = a2;
            } else {
                uint32_t inv_alpha = 255 - a2;
                background[bg_pixel_index]     = (r2 * a2 + r1 * inv_alpha) / 255;
                background[bg_pixel_index + 1] = (g2 * a2 + g1 * inv_alpha) / 255;
                background[bg_pixel_index + 2] = (b2 * a2 + b1 * inv_alpha) / 255;
                background[bg_pixel_index + 3] = a2 + (a1 * inv_alpha) / 255;
            }
        }
    }
}
#else
void blend_avx2(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height,
                uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y) {
    blend(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y);
}
#endif

#if defined(__ARM_NEON)
void blend_neon(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height,
                uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y) {
    if (background == NULL || overlay == NULL) {
        printf("Background or overlay image is NULL\n");
        return;
    }

    for (uint32_t y = 0; y < ov_height; y++) {
        int bg_y = start_y + y;
        if (bg_y < 0 || bg_y >= bg_height) {
            continue;
        }

        uint32_t bg_index = (bg_y * bg_width + start_x) * 4;
        uint32_t overlay_index = y * ov_width * 4;

        for (uint32_t x = 0; x < ov_width - 3; x += 4) {
            int bg_x = start_x + x;
            if (bg_x < 0 || bg_x + 3 >= bg_width) {
                bg_index += 16;
                overlay_index += 16;
                continue;
            }

            uint8x16_t bg_pixels = vld1q_u8(&background[bg_index]);
            uint8x16_t ov_pixels = vld1q_u8(&overlay[overlay_index]);

            uint16x8_t alpha_high = vmovl_u8(vget_high_u8(ov_pixels));
            uint16x8_t alpha_low = vmovl_u8(vget_low_u8(ov_pixels));
            uint16x8_t inv_alpha_high = vsubq_u16(vdupq_n_u16(255), alpha_high);
            uint16x8_t inv_alpha_low = vsubq_u16(vdupq_n_u16(255), alpha_low);

            uint16x8_t bg_high = vmovl_u8(vget_high_u8(bg_pixels));
            uint16x8_t bg_low = vmovl_u8(vget_low_u8(bg_pixels));
            uint16x8_t ov_high = vmovl_u8(vget_high_u8(ov_pixels));
            uint16x8_t ov_low = vmovl_u8(vget_low_u8(ov_pixels));

            uint16x8_t blended_high = vaddq_u16(
                vmulq_u16(ov_high, alpha_high),
                vmulq_u16(bg_high, inv_alpha_high)
            );
            uint16x8_t blended_low = vaddq_u16(
                vmulq_u16(ov_low, alpha_low),
                vmulq_u16(bg_low, inv_alpha_low)
            );

            blended_high = vshrq_n_u16(blended_high, 8);
            blended_low = vshrq_n_u16(blended_low, 8);

            uint8x16_t result = vcombine_u8(vqmovn_u16(blended_low), vqmovn_u16(blended_high));

            vst1q_u8(&background[bg_index], result);

            bg_index += 16;
            overlay_index += 16;
        }

        for (uint32_t x = ov_width - (ov_width % 4); x < ov_width; x++) {
            int bg_x = start_x + x;
            if (bg_x < 0 || bg_x >= bg_width) {
                continue;
            }

            uint32_t bg_pixel_index = (bg_y * bg_width + bg_x) * 4;
            uint32_t ov_pixel_index = (y * ov_width + x) * 4;

            uint8_t r1 = background[bg_pixel_index];
            uint8_t g1 = background[bg_pixel_index + 1];
            uint8_t b1 = background[bg_pixel_index + 2];
            uint8_t a1 = background[bg_pixel_index + 3];

            uint8_t r2 = overlay[ov_pixel_index];
            uint8_t g2 = overlay[ov_pixel_index + 1];
            uint8_t b2 = overlay[ov_pixel_index + 2];
            uint8_t a2 = overlay[ov_pixel_index + 3];

            if (a2 == 0) {
                continue;
            } else if (a2 == 255) {
                background[bg_pixel_index] = r2;
                background[bg_pixel_index + 1] = g2;
                background[bg_pixel_index + 2] = b2;
                background[bg_pixel_index + 3] = a2;
            } else {
                uint32_t inv_alpha = 255 - a2;
                background[bg_pixel_index]     = (r2 * a2 + r1 * inv_alpha) / 255;
                background[bg_pixel_index + 1] = (g2 * a2 + g1 * inv_alpha) / 255;
                background[bg_pixel_index + 2] = (b2 * a2 + b1 * inv_alpha) / 255;
                background[bg_pixel_index + 3] = a2 + (a1 * inv_alpha) / 255;
            }
        }
    }
}

#else
// Fallback to non-NEON version if NEON is not available
void blend_neon(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height,
                uint32_t ov_width, uint32_t ov_height, int32_t start_x, int32_t start_y) {
    // Call the original blend function here
    blend(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y);
}
#endif

void blit(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height,
          uint8_t* src_image, uint32_t src_width, uint32_t src_height,
          int32_t start_x, int32_t start_y) {
    if (dest_image == NULL || src_image == NULL) return;

    int32_t copy_start_x = (start_x < 0) ? 0 : start_x;
    int32_t copy_start_y = (start_y < 0) ? 0 : start_y;
    int32_t copy_end_x = (start_x + (int32_t)src_width > (int32_t)dest_width) ? dest_width : (start_x + src_width);
    int32_t copy_end_y = (start_y + (int32_t)src_height > (int32_t)dest_height) ? dest_height : (start_y + src_height);

    if (copy_start_x >= copy_end_x || copy_start_y >= copy_end_y) return;

    uint32_t copy_width = copy_end_x - copy_start_x;
    uint32_t copy_height = copy_end_y - copy_start_y;
    int32_t src_offset_x = (start_x < 0) ? -start_x : 0;
    int32_t src_offset_y = (start_y < 0) ? -start_y : 0;

    uint32_t dest_stride = dest_width * 4;
    uint32_t src_stride = src_width * 4;
    uint32_t copy_stride = copy_width * 4;

    uint8_t* dest_ptr = dest_image + (copy_start_y * dest_width + copy_start_x) * 4;
    uint8_t* src_ptr = src_image + (src_offset_y * src_width + src_offset_x) * 4;

    for (uint32_t y = 0; y < copy_height; y++) {
        memcpy(dest_ptr, src_ptr, copy_stride);
        dest_ptr += dest_stride;
        src_ptr += src_stride;
    }
}

#if HAS_AVX2
void blit_avx2(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height,
               uint8_t* src_image, uint32_t src_width, uint32_t src_height,
               int32_t start_x, int32_t start_y) {
    if (dest_image == NULL || src_image == NULL) return;

    int32_t copy_start_x = (start_x < 0) ? 0 : start_x;
    int32_t copy_start_y = (start_y < 0) ? 0 : start_y;
    int32_t copy_end_x = (start_x + (int32_t)src_width > (int32_t)dest_width) ? dest_width : (start_x + src_width);
    int32_t copy_end_y = (start_y + (int32_t)src_height > (int32_t)dest_height) ? dest_height : (start_y + src_height);

    if (copy_start_x >= copy_end_x || copy_start_y >= copy_end_y) return;

    uint32_t copy_width = copy_end_x - copy_start_x;
    uint32_t copy_height = copy_end_y - copy_start_y;
    int32_t src_offset_x = (start_x < 0) ? -start_x : 0;
    int32_t src_offset_y = (start_y < 0) ? -start_y : 0;

    uint32_t avx2_blocks = copy_width / 8;
    uint32_t remainder = copy_width % 8;

    for (uint32_t y = 0; y < copy_height; y++) {
        uint8_t* dest_row = dest_image + ((copy_start_y + y) * dest_width + copy_start_x) * 4;
        uint8_t* src_row = src_image + ((src_offset_y + y) * src_width + src_offset_x) * 4;

        for (uint32_t x = 0; x < avx2_blocks; x++) {
            __m256i pixels = _mm256_loadu_si256((__m256i*)(src_row + x * 32));
            _mm256_storeu_si256((__m256i*)(dest_row + x * 32), pixels);
        }

        if (remainder > 0) {
            memcpy(dest_row + avx2_blocks * 32, src_row + avx2_blocks * 32, remainder * 4);
        }
    }
}
#else
void blit_avx2(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height,
               uint8_t* src_image, uint32_t src_width, uint32_t src_height,
               int32_t start_x, int32_t start_y) {
    blit(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y);
}
#endif

#if defined(__ARM_NEON)
void blit_neon(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height,
               uint8_t* src_image, uint32_t src_width, uint32_t src_height,
               int32_t start_x, int32_t start_y) {
    if (dest_image == NULL || src_image == NULL) return;

    int32_t copy_start_x = (start_x < 0) ? 0 : start_x;
    int32_t copy_start_y = (start_y < 0) ? 0 : start_y;
    int32_t copy_end_x = (start_x + (int32_t)src_width > (int32_t)dest_width) ? dest_width : (start_x + src_width);
    int32_t copy_end_y = (start_y + (int32_t)src_height > (int32_t)dest_height) ? dest_height : (start_y + src_height);

    if (copy_start_x >= copy_end_x || copy_start_y >= copy_end_y) return;

    uint32_t copy_width = copy_end_x - copy_start_x;
    uint32_t copy_height = copy_end_y - copy_start_y;
    int32_t src_offset_x = (start_x < 0) ? -start_x : 0;
    int32_t src_offset_y = (start_y < 0) ? -start_y : 0;

    uint32_t dest_stride = dest_width * 4;
    uint32_t src_stride = src_width * 4;

    uint8_t* dest_ptr = dest_image + (copy_start_y * dest_width + copy_start_x) * 4;
    uint8_t* src_ptr = src_image + (src_offset_y * src_width + src_offset_x) * 4;

    uint32_t neon_blocks = copy_width / 4;
    uint32_t remainder = copy_width % 4;

    for (uint32_t y = 0; y < copy_height; y++) {
        uint8_t* dest_row = dest_ptr + y * dest_stride;
        uint8_t* src_row = src_ptr + y * src_stride;

        for (uint32_t x = 0; x < neon_blocks; x++) {
            uint32x4_t pixels = vld1q_u32((uint32_t*)(src_row + x * 16));
            vst1q_u32((uint32_t*)(dest_row + x * 16), pixels);
        }

        if (remainder > 0) {
            memcpy(dest_row + neon_blocks * 16, src_row + neon_blocks * 16, remainder * 4);
        }
    }
}
#else
void blit_neon(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height,
               uint8_t* src_image, uint32_t src_width, uint32_t src_height,
               int32_t start_x, int32_t start_y) {
    blit(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y);
}
#endif

void blit_same_size(uint8_t* src, uint8_t* dst, uint32_t width, uint32_t height, uint32_t channels) {
    size_t total_bytes = width * height * channels;
    memcpy(dst, src, total_bytes);
}

void nearest_neighbor_resize(uint8_t* __restrict src, uint8_t* __restrict dst,
                             uint32_t src_width, uint32_t src_height,
                             uint32_t dst_width, uint32_t dst_height) {
    if (!src || !dst || src_width == 0 || src_height == 0 ||
        dst_width == 0 || dst_height == 0) {
        return;
    }

    const uint32_t channels = 4; // Suponiendo imagen RGBA
    uint32_t x_ratio = (uint32_t)((src_width << 16) / dst_width) + 1;
    uint32_t y_ratio = (uint32_t)((src_height << 16) / dst_height) + 1;

    for (uint32_t y = 0; y < dst_height; y++) {
        uint32_t src_y = (y * y_ratio) >> 16;
        uint8_t* dst_row = dst + y * dst_width * channels;
        uint8_t* src_row = src + src_y * src_width * channels;

        uint32_t x = 0;
        for (; x + 1 < dst_width; x += 2) {
            uint32_t src_x0 = (x * x_ratio) >> 16;
            uint32_t src_x1 = ((x + 1) * x_ratio) >> 16;

            uint8_t* dst_pixel0 = dst_row + x * channels;
            uint8_t* dst_pixel1 = dst_row + (x + 1) * channels;

            uint8_t* src_pixel0 = src_row + src_x0 * channels;
            uint8_t* src_pixel1 = src_row + src_x1 * channels;

            // Copiar píxeles completos (RGBA)
            *((uint32_t*)dst_pixel0) = *((uint32_t*)src_pixel0);
            *((uint32_t*)dst_pixel1) = *((uint32_t*)src_pixel1);
        }

        // Procesar píxel restante si el ancho es impar
        if (x < dst_width) {
            uint32_t src_x = (x * x_ratio) >> 16;
            uint8_t* dst_pixel = dst_row + x * channels;
            uint8_t* src_pixel = src_row + src_x * channels;
            *((uint32_t*)dst_pixel) = *((uint32_t*)src_pixel);
        }
    }
}
#if defined(__ARM_NEON)
void nearest_neighbor_resize_neon(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height) {
    if (src == NULL || dst == NULL) {
        return;
    }

    float x_ratio = (float)src_width / dst_width;
    float y_ratio = (float)src_height / dst_height;
    uint32_t channels = 4;

    for (uint32_t y = 0; y < dst_height; y++) {
        uint32_t nearest_y = (uint32_t)(y * y_ratio) * src_width * channels;
        uint8_t* dst_row = dst + (y * dst_width * channels);

        for (uint32_t x = 0; x < dst_width - 3; x += 4) {
            uint32_t nearest_x = (uint32_t)(x * x_ratio) * channels;
            uint8_t* src_pixel = src + nearest_y + nearest_x;

            uint32x4_t pixel = vld1q_u32((uint32_t*)src_pixel);
            vst1q_u32((uint32_t*)(dst_row + x * channels), pixel);
        }

        for (uint32_t x = dst_width - (dst_width % 4); x < dst_width; x++) {
            uint32_t nearest_x = (uint32_t)(x * x_ratio) * channels;
            uint8_t* src_pixel = src + nearest_y + nearest_x;
            memcpy(&dst_row[x * channels], src_pixel, channels);
        }
    }
}
#else
void nearest_neighbor_resize_neon(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height) {
    nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height);
}
#endif
#if HAS_AVX2
#include <immintrin.h>

void nearest_neighbor_resize_avx2(uint8_t* __restrict src, uint8_t* __restrict dst,
                                  uint32_t src_width, uint32_t src_height,
                                  uint32_t dst_width, uint32_t dst_height) {
    if (!src || !dst || src_width == 0 || src_height == 0 ||
        dst_width == 0 || dst_height == 0) {
        return;
    }

    const uint32_t channels = 4; // Asumiendo imagen RGBA
    uint64_t x_ratio = ((uint64_t)src_width << 16) / dst_width;
    uint64_t y_ratio = ((uint64_t)src_height << 16) / dst_height;

    for (uint32_t y = 0; y < dst_height; y++) {
        uint32_t src_y = (y * y_ratio) >> 16;
        uint8_t* dst_row = dst + y * dst_width * channels;
        uint8_t* src_row = src + src_y * src_width * channels;

        uint32_t x = 0;
        for (; x + 7 < dst_width; x += 8) {
            // Calcular los índices fuente correctos para cada píxel de destino
            uint32_t src_x0 = (x * x_ratio) >> 16;
            uint32_t src_x1 = ((x + 1) * x_ratio) >> 16;
            uint32_t src_x2 = ((x + 2) * x_ratio) >> 16;
            uint32_t src_x3 = ((x + 3) * x_ratio) >> 16;
            uint32_t src_x4 = ((x + 4) * x_ratio) >> 16;
            uint32_t src_x5 = ((x + 5) * x_ratio) >> 16;
            uint32_t src_x6 = ((x + 6) * x_ratio) >> 16;
            uint32_t src_x7 = ((x + 7) * x_ratio) >> 16;

            // Cargar los píxeles correctos para estos índices de origen
            __m256i pixels = _mm256_set_epi32(
                *(uint32_t*)(src_row + src_x7 * channels),
                *(uint32_t*)(src_row + src_x6 * channels),
                *(uint32_t*)(src_row + src_x5 * channels),
                *(uint32_t*)(src_row + src_x4 * channels),
                *(uint32_t*)(src_row + src_x3 * channels),
                *(uint32_t*)(src_row + src_x2 * channels),
                *(uint32_t*)(src_row + src_x1 * channels),
                *(uint32_t*)(src_row + src_x0 * channels)
            );

            // Almacenar los píxeles en el destino
            _mm256_storeu_si256((__m256i*)(dst_row + x * channels), pixels);
        }

        // Procesar píxeles restantes
        for (; x < dst_width; x++) {
            uint32_t src_x = (x * x_ratio) >> 16;
            *(uint32_t*)(dst_row + x * channels) = *(uint32_t*)(src_row + src_x * channels);
        }
    }
}
#else
void nearest_neighbor_resize_avx2(uint8_t* src, uint8_t* dst,
                                  uint32_t src_width, uint32_t src_height,
                                  uint32_t dst_width, uint32_t dst_height) {
    nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height);
}
#endif

