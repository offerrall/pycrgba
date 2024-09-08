import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, blit, blit_avx2

def test_blit(dest_width, dest_height, iterations=100):
    dest = create_image_rgba(dest_width, dest_height)
    fill_image_rgba(dest, dest_width, dest_height, 255, 0, 0, 255)  # Red background

    src_width, src_height = dest_width // 2, dest_height // 2
    src = create_image_rgba(src_width, src_height)
    fill_image_rgba(src, src_width, src_height, 0, 255, 0, 255)  # Green source

    total_blit_time = 0
    total_blit_avx2_time = 0

    for _ in range(iterations):
        # Test blit
        start_time = time.time()
        blit(dest, dest_width, dest_height, src, src_width, src_height, dest_width // 4, dest_height // 4)
        blit_time = time.time() - start_time
        total_blit_time += blit_time

        # Test blit_avx2
        start_time = time.time()
        blit_avx2(dest, dest_width, dest_height, src, src_width, src_height, dest_width // 4, dest_height // 4)
        blit_avx2_time = time.time() - start_time
        total_blit_avx2_time += blit_avx2_time

    avg_blit_time = total_blit_time / iterations
    avg_blit_avx2_time = total_blit_avx2_time / iterations

    blit_fps = 1 / avg_blit_time if avg_blit_time > 0 else float('inf')
    blit_avx2_fps = 1 / avg_blit_avx2_time if avg_blit_avx2_time > 0 else float('inf')

    print(f"Destination Resolution: {dest_width}x{dest_height}")
    print(f"Source Resolution: {src_width}x{src_height}")
    print(f"blit: {blit_fps:.2f} FPS")
    print(f"blit_avx2: {blit_avx2_fps:.2f} FPS")
    print(f"Speed-up: {blit_avx2_fps / blit_fps:.2f}x")
    print()

    free_image_rgba(dest)
    free_image_rgba(src)

if __name__ == "__main__":
    resolutions = [
        (640, 480),    # VGA
        (1280, 720),   # HD
        (1920, 1080),  # Full HD
        (3840, 2160),  # 4K
    ]

    for width, height in resolutions:
        test_blit(width, height)
