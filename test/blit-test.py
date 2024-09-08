import time
import numpy as np
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, blit, blit_avx2
from pycrgba_cffi import ffi

def image_to_numpy(data, width, height):
    buffer = ffi.buffer(data, width * height * 4)
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

def compare_images(img1, img2, width, height):
    np_img1 = image_to_numpy(img1, width, height)
    np_img2 = image_to_numpy(img2, width, height)
    return np.array_equal(np_img1, np_img2)

def test_blit(iterations=100):
    width, height = 1920, 1080
    dest = create_image_rgba(width, height)
    fill_image_rgba(dest, width, height, 255, 0, 0, 255)  # Red background

    src = create_image_rgba(width, height)
    fill_image_rgba(src, width, height, 0, 255, 0, 255)  # Green source

    dest_blit = create_image_rgba(width, height)
    dest_blit_avx2 = create_image_rgba(width, height)

    total_blit_time = 0
    total_blit_avx2_time = 0

    for _ in range(iterations):
        fill_image_rgba(dest_blit, width, height, 255, 0, 0, 255)
        fill_image_rgba(dest_blit_avx2, width, height, 255, 0, 0, 255)

        start_time = time.time()
        blit(dest_blit, width, height, src, width, height, 0, 0)
        total_blit_time += time.time() - start_time

        start_time = time.time()
        blit_avx2(dest_blit_avx2, width, height, src, width, height, 0, 0)
        total_blit_avx2_time += time.time() - start_time

    results_match = compare_images(dest_blit, dest_blit_avx2, width, height)

    avg_blit_time = total_blit_time / iterations
    avg_blit_avx2_time = total_blit_avx2_time / iterations

    blit_fps = 1 / avg_blit_time if avg_blit_time > 0 else float('inf')
    blit_avx2_fps = 1 / avg_blit_avx2_time if avg_blit_avx2_time > 0 else float('inf')

    print(f"Resolution: {width}x{height}")
    print(f"blit: {blit_fps:.2f} FPS")
    print(f"blit_avx2 (optimized): {blit_avx2_fps:.2f} FPS")
    print(f"Results match: {results_match}")
    print(f"Speed-up: {blit_avx2_fps / blit_fps:.2f}x")

    free_image_rgba(dest)
    free_image_rgba(src)
    free_image_rgba(dest_blit)
    free_image_rgba(dest_blit_avx2)

if __name__ == "__main__":
    test_blit()
