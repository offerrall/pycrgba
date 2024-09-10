import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, blend, blend_avx2, blend_neon

def test_blend(iterations=100):
    width, height = 1920, 1080
    background = create_image_rgba(width, height)
    fill_image_rgba(background, width, height, 255, 0, 0, 255)

    overlay = create_image_rgba(width, height)
    fill_image_rgba(overlay, width, height, 0, 255, 0, 128)

    total_blend_time = 0
    total_blend_avx2_time = 0
    total_blend_neon_time = 0

    for _ in range(iterations):
        # Test blend
        start_time = time.time()
        blend(background, overlay, width, height, width, height, 0, 0)
        blend_time = time.time() - start_time
        total_blend_time += blend_time

        # Test blend_avx2
        start_time = time.time()
        blend_avx2(background, overlay, width, height, width, height, 0, 0)
        blend_avx2_time = time.time() - start_time
        total_blend_avx2_time += blend_avx2_time

        # Test blend_neon
        start_time = time.time()
        blend_neon(background, overlay, width, height, width, height, 0, 0)
        blend_neon_time = time.time() - start_time
        total_blend_neon_time += blend_neon_time

    avg_blend_time = total_blend_time / iterations
    avg_blend_avx2_time = total_blend_avx2_time / iterations
    avg_blend_neon_time = total_blend_neon_time / iterations

    blend_fps = 1 / avg_blend_time if avg_blend_time > 0 else float('inf')
    blend_avx2_fps = 1 / avg_blend_avx2_time if avg_blend_avx2_time > 0 else float('inf')
    blend_neon_fps = 1 / avg_blend_neon_time if avg_blend_neon_time > 0 else float('inf')

    print(f"Resolution: {width}x{height}")
    print(f"blend: {blend_fps:.2f} FPS")
    print(f"blend_avx2: {blend_avx2_fps:.2f} FPS")
    print(f"blend_neon: {blend_neon_fps:.2f} FPS")
    print(f"AVX2 Speed-up: {blend_avx2_fps / blend_fps:.2f}x")
    print(f"NEON Speed-up: {blend_neon_fps / blend_fps:.2f}x")

    free_image_rgba(background)
    free_image_rgba(overlay)

if __name__ == "__main__":
    test_blend()