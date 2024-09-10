import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, blit_same_size

def test_blit_same_size(iterations=100):
    width, height = 1920, 1080
    channels = 4
    src = create_image_rgba(width, height)
    dst = create_image_rgba(width, height)

    fill_image_rgba(src, width, height, 255, 0, 0, 255)

    total_blit_time = 0

    for _ in range(iterations):
        start_time = time.time()
        blit_same_size(src, dst, width, height, channels)
        blit_time = time.time() - start_time
        total_blit_time += blit_time


    avg_blit_time = total_blit_time / iterations

    blit_fps = 1 / avg_blit_time if avg_blit_time > 0 else float('inf')

    print(f"Resolution: {width}x{height}")
    print(f"blit_same_size: {blit_fps:.2f} FPS")

    free_image_rgba(src)
    free_image_rgba(dst)

if __name__ == "__main__":
    test_blit_same_size()
