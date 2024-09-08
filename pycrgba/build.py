from cffi import FFI
import shutil
from os import remove, listdir

ffibuilder = FFI()

ffibuilder.cdef("""
    uint8_t* create_image_rgba(uint32_t width, uint32_t height);
    void free_image_rgba(uint8_t* image_data);
    void copy_image(uint8_t* dest_image, uint8_t* src_image, uint32_t width, uint32_t height);
    void fill_image_rgba(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
    void fill_image_rgba_avx2(uint8_t* image_data, uint32_t width, uint32_t height, uint8_t r, uint8_t g, uint8_t b, uint8_t a);
    void overlay_image_with_coords(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int start_x, int start_y);
    void overlay_image_with_coords_avx2(uint8_t* background, uint8_t* overlay, uint32_t bg_width, uint32_t bg_height, uint32_t ov_width, uint32_t ov_height, int start_x, int start_y);
    void copy_image_diff_size_no_alpha(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int start_x, int start_y);
    void copy_image_diff_size_no_alpha_avx2(uint8_t* dest_image, uint32_t dest_width, uint32_t dest_height, uint8_t* src_image, uint32_t src_width, uint32_t src_height, int start_x, int start_y);
    void nearest_neighbor_resize(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);
    void nearest_neighbor_resize_avx2(uint8_t* src, uint8_t* dst, uint32_t src_width, uint32_t src_height, uint32_t dst_width, uint32_t dst_height);
""")

ffibuilder.set_source(
    "pycrgba_cffi",
    """
    #include "basic_image_lib.h"
    """,
    sources=["./c_src/basic_image_lib.c"],
    include_dirs=["./c_src"],
)

if __name__ == "__main__":

    list_files = listdir(".")
    for file in list_files:
        if file.endswith(".pyc") or file.endswith(".pyo") or file.endswith(".pyd"):
            remove(file)

    ffibuilder.compile(verbose=True)

    remove("pycrgba_cffi.c")
    shutil.rmtree("Release", ignore_errors=True)
    shutil.rmtree("c_src", ignore_errors=True)