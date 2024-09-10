import pycrgba_cffi as _ffi
from typing import Any
import platform

Image = Any

def create_image_rgba(width: int, height: int) -> Image:
    """Creates an RGBA image (4 bytes per pixel)."""
    return _ffi.lib.create_image_rgba(width, height)

def free_image_rgba(image_data: Image):
    """Frees the memory allocated for an image."""
    _ffi.lib.free_image_rgba(image_data)

def fill_image_rgba(image_data: Image, width: int, height: int, r: int, g: int, b: int, a: int):
    """Fills an image with a solid RGBA color."""
    _ffi.lib.fill_image_rgba(image_data, width, height, r, g, b, a)

def fill_image_rgba_avx2(image_data: Image, width: int, height: int, r: int, g: int, b: int, a: int):
    """Fills an image with a solid RGBA color using AVX2."""
    _ffi.lib.fill_image_rgba_avx2(image_data, width, height, r, g, b, a)

def fill_image_rgba_neon(image_data: Image, width: int, height: int, r: int, g: int, b: int, a: int):
    """Fills an image with a solid RGBA color using NEON optimizations."""
    _ffi.lib.fill_image_rgba_neon(image_data, width, height, r, g, b, a)

def blend(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Blends an image on top of another image with coordinates."""
    _ffi.lib.blend(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def blend_avx2(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Blends an image on top of another image with coordinates using AVX2."""
    _ffi.lib.blend_avx2(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def blend_neon(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Blends an image on top of another image with coordinates using NEON optimizations."""
    _ffi.lib.blend_neon(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def blit(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Blits an image to another image with different sizes."""
    _ffi.lib.blit(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def blit_neon(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Blits an image to another image with different sizes using NEON optimizations."""
    _ffi.lib.blit_neon(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def blit_same_size(src: Image, dst: Image, width: int, height: int, channels: int):
    """Blits an image of the same size."""
    _ffi.lib.blit_same_size(src, dst, width, height, channels)

def blit_avx2(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Blits an image to another image with different sizes using AVX2."""
    _ffi.lib.blit_avx2(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def nearest_neighbor_resize(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Resizes an image using nearest neighbor interpolation."""
    _ffi.lib.nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height)

def nearest_neighbor_resize_avx2(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Resizes an image using nearest neighbor interpolation with AVX2."""
    _ffi.lib.nearest_neighbor_resize_avx2(src, dst, src_width, src_height, dst_width, dst_height)

def nearest_neighbor_resize_neon(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Resizes an image using nearest neighbor interpolation with NEON optimizations."""
    _ffi.lib.nearest_neighbor_resize_neon(src, dst, src_width, src_height, dst_width, dst_height)

def _is_arm():
    return platform.machine().startswith('arm') or platform.machine().startswith('aarch')

def _is_x86_64():
    return platform.machine() == 'x86_64' or platform.machine() == 'AMD64'

def auto_fill_image_rgba(image_data: Image, width: int, height: int, r: int, g: int, b: int, a: int):
    """Automatically selects the best fill_image_rgba function based on hardware."""
    if _is_arm():
        fill_image_rgba_neon(image_data, width, height, r, g, b, a)
    elif _is_x86_64():
        fill_image_rgba_avx2(image_data, width, height, r, g, b, a)
    else:
        fill_image_rgba(image_data, width, height, r, g, b, a)

def auto_blend(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Automatically selects the best blend function based on hardware."""
    if _is_arm():
        blend_neon(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)
    elif _is_x86_64():
        blend_avx2(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)
    else:
        blend(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def auto_blit(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Automatically selects the best blit function based on hardware."""
    if _is_arm():
        blit_neon(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)
    elif _is_x86_64():
        blit_avx2(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)
    else:
        blit(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def auto_nearest_neighbor_resize(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Automatically selects the best nearest neighbor resize function based on hardware."""
    if _is_arm():
        nearest_neighbor_resize_neon(src, dst, src_width, src_height, dst_width, dst_height)
    elif _is_x86_64():
        nearest_neighbor_resize_avx2(src, dst, src_width, src_height, dst_width, dst_height)
    else:
        nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height)
