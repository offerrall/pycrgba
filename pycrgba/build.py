from cffi import FFI
import shutil
from os import remove, listdir
import platform
from time import sleep

ffibuilder = FFI()

ffibuilder.cdef("""
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
""")

if platform.system() == "Windows":
    print("Windows detected")
    extra_compile_args = ["/O2", "/arch:AVX2"]
elif platform.machine() == "x86_64":
    extra_compile_args = ["-O3", "-march=native", "-mavx2"]
    print("x86_64 detected")
elif platform.machine().startswith('arm'):
    extra_compile_args = ["-O3", "-march=armv8-a+simd"]
    print("ARM detected")
else:
    extra_compile_args = ["-O3", "-march=native"]

print(f"Extra compile args: {extra_compile_args}")
sleep(2)

ffibuilder.set_source(
    "pycrgba_cffi",
    """
    #include "basic_image_lib.h"
    """,
    sources=["./c_src/basic_image_lib.c"],
    include_dirs=["./c_src"],
    extra_compile_args=extra_compile_args,
)

if __name__ == "__main__":
    list_files = listdir(".")
    for file in list_files:
        if file.endswith(".pyc") or file.endswith(".pyo") or file.endswith(".pyd"):
            remove(file)

    ffibuilder.compile(verbose=True)

    remove("pycrgba_cffi.c")
    shutil.rmtree("Release", ignore_errors=True)