import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, blend, blend_avx2

def test_blend(bg_width, bg_height, iterations=100):
    background = create_image_rgba(bg_width, bg_height)
    fill_image_rgba(background, bg_width, bg_height, 255, 0, 0, 255)

    ov_width, ov_height = bg_width // 2, bg_height // 2
    overlay = create_image_rgba(ov_width, ov_height)
    fill_image_rgba(overlay, ov_width, ov_height, 0, 255, 0, 128)

    total_blend_time = 0
    total_blend_avx2_time = 0

    for _ in range(iterations):
        # Test blend
        start_time = time.time()
        blend(background, overlay, bg_width, bg_height, ov_width, ov_height, bg_width // 4, bg_height // 4)
        blend_time = time.time() - start_time
        total_blend_time += blend_time

        # Test blend_avx2
        start_time = time.time()
        blend_avx2(background, overlay, bg_width, bg_height, ov_width, ov_height, bg_width // 4, bg_height // 4)
        blend_avx2_time = time.time() - start_time
        total_blend_avx2_time += blend_avx2_time

    avg_blend_time = total_blend_time / iterations
    avg_blend_avx2_time = total_blend_avx2_time / iterations

    blend_fps = 1 / avg_blend_time if avg_blend_time > 0 else float('inf')
    blend_avx2_fps = 1 / avg_blend_avx2_time if avg_blend_avx2_time > 0 else float('inf')

    print(f"Resolution: {bg_width}x{bg_height}")
    print(f"blend: {blend_fps:.2f} FPS")
    print(f"blend_avx2: {blend_avx2_fps:.2f} FPS")
    print(f"Speed-up: {blend_avx2_fps / blend_fps:.2f}x")
    print()

    free_image_rgba(background)
    free_image_rgba(overlay)

if __name__ == "__main__":
    resolutions = [
        (640, 480),    # VGA
        (1280, 720),   # HD
        (1920, 1080),  # Full HD
        (3840, 2160),  # 4K
    ]

    for width, height in resolutions:
        test_blend(width, height)
