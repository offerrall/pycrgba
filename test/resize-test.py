import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, nearest_neighbor_resize, nearest_neighbor_resize_avx2

def test_resize(src_width, src_height, iterations=100):
    src = create_image_rgba(src_width, src_height)
    fill_image_rgba(src, src_width, src_height, 255, 255, 0, 255)

    dst_width, dst_height = src_width // 2, src_height // 2
    dst = create_image_rgba(dst_width, dst_height)

    total_resize_time = 0
    total_resize_avx2_time = 0

    for _ in range(iterations):
        # Test nearest_neighbor_resize
        start_time = time.time()
        nearest_neighbor_resize(src, dst, src_width, src_height, dst_width, dst_height)
        resize_time = time.time() - start_time
        total_resize_time += resize_time

        # Test nearest_neighbor_resize_avx2
        start_time = time.time()
        nearest_neighbor_resize_avx2(src, dst, src_width, src_height, dst_width, dst_height)
        resize_avx2_time = time.time() - start_time
        total_resize_avx2_time += resize_avx2_time

    avg_resize_time = total_resize_time / iterations
    avg_resize_avx2_time = total_resize_avx2_time / iterations

    resize_fps = 1 / avg_resize_time if avg_resize_time > 0 else float('inf')
    resize_avx2_fps = 1 / avg_resize_avx2_time if avg_resize_avx2_time > 0 else float('inf')

    print(f"Source Resolution: {src_width}x{src_height}")
    print(f"Destination Resolution: {dst_width}x{dst_height}")
    print(f"nearest_neighbor_resize: {resize_fps:.2f} FPS")
    print(f"nearest_neighbor_resize_avx2: {resize_avx2_fps:.2f} FPS")
    print(f"Speed-up: {resize_avx2_fps / resize_fps:.2f}x")
    print()

    free_image_rgba(src)
    free_image_rgba(dst)

if __name__ == "__main__":
    resolutions = [
        (640, 480),    # VGA
        (1280, 720),   # HD
        (1920, 1080),  # Full HD
        (3840, 2160),  # 4K
    ]

    for width, height in resolutions:
        test_resize(width, height)
