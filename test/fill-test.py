import time
import platform
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, fill_image_rgba_avx2, fill_image_rgba_neon

def test_fill(iterations=100):
    width, height = 1920, 1080
    image = create_image_rgba(width, height)

    total_fill_time = 0
    total_fill_avx2_time = 0
    total_fill_neon_time = 0

    for _ in range(iterations):
        # Test fill_image_rgba
        start_time = time.time()
        fill_image_rgba(image, width, height, 255, 0, 0, 255)
        fill_time = time.time() - start_time
        total_fill_time += fill_time

        # Test fill_image_rgba_avx2
        start_time = time.time()
        fill_image_rgba_avx2(image, width, height, 0, 255, 0, 255)
        fill_avx2_time = time.time() - start_time
        total_fill_avx2_time += fill_avx2_time

        # Test fill_image_rgba_neon
        start_time = time.time()
        fill_image_rgba_neon(image, width, height, 0, 0, 255, 255)
        fill_neon_time = time.time() - start_time
        total_fill_neon_time += fill_neon_time

    avg_fill_time = total_fill_time / iterations
    avg_fill_avx2_time = total_fill_avx2_time / iterations
    avg_fill_neon_time = total_fill_neon_time / iterations

    fill_fps = 1 / avg_fill_time if avg_fill_time > 0 else float('inf')
    fill_avx2_fps = 1 / avg_fill_avx2_time if avg_fill_avx2_time > 0 else float('inf')
    fill_neon_fps = 1 / avg_fill_neon_time if avg_fill_neon_time > 0 else float('inf')

    print(f"Platform: {platform.machine()}")
    print(f"Resolution: {width}x{height}")
    print(f"fill_image_rgba: {fill_fps:.2f} FPS")
    print(f"fill_image_rgba_avx2: {fill_avx2_fps:.2f} FPS")
    print(f"fill_image_rgba_neon: {fill_neon_fps:.2f} FPS")
    print(f"Speed-up (AVX2): {fill_avx2_fps / fill_fps:.2f}x")
    print(f"Speed-up (NEON): {fill_neon_fps / fill_fps:.2f}x")

    free_image_rgba(image)

if __name__ == "__main__":
    test_fill()