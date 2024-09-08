import pycrgba_cffi as _ffi
from typing import Any

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

def blend_coords(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Blends an image on top of another image with coordinates."""
    _ffi.lib.blend_coords(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def blend_avx2(background: Image, overlay: Image, bg_width: int, bg_height: int, ov_width: int, ov_height: int, start_x: int, start_y: int):
    """Blends an image on top of another image with coordinates using AVX2."""
    _ffi.lib.blend_avx2(background, overlay, bg_width, bg_height, ov_width, ov_height, start_x, start_y)

def blit_image(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Blits an image to another image with different sizes."""
    _ffi.lib.blit_image(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def blit_image_avx2(dest_image: Image, dest_width: int, dest_height: int, src_image: Image, src_width: int, src_height: int, start_x: int, start_y: int):
    """Blits an image to another image with different sizes using AVX2."""
    _ffi.lib.blit_image_avx2(dest_image, dest_width, dest_height, src_image, src_width, src_height, start_x, start_y)

def nearest_neighbor_resize(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Resizes an image using nearest neighbor interpolation."""
    _ffi.lib.nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height)

def nearest_neighbor_resize_avx2(src: Image, dst: Image, src_width: int, src_height: int, dst_width: int, dst_height: int):
    """Resizes an image using nearest neighbor interpolation with AVX2."""
    _ffi.lib.nearest_neighbor_resize_avx2(src, dst, src_width, src_height, dst_width, dst_height)