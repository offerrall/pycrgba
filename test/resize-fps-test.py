import time
from pycrgba import (
    create_image_rgba,
    free_image_rgba,
    nearest_neighbor_resize,
    nearest_neighbor_resize_avx2,
    bilinear_resize,
    bilinear_resize_avx2
)

def test_resize_fps(resize_func, src_image, dst_image, width, height, num_frames=100):
    start_time = time.time()
    for _ in range(num_frames):
        resize_func(src_image, dst_image, width, height, width, height)
    end_time = time.time()
    fps = num_frames / (end_time - start_time)
    return fps

def main():
    width, height = 1920, 1080  # 1080p resolution
    src_image = create_image_rgba(width, height)
    dst_image = create_image_rgba(width, height)

    # Fill source image with some test data
    for y in range(height):
        for x in range(width):
            index = (y * width + x) * 4
            src_image[index] = x % 256
            src_image[index + 1] = y % 256
            src_image[index + 2] = (x + y) % 256
            src_image[index + 3] = 255

    resize_functions = [
        ("Nearest Neighbor", nearest_neighbor_resize),
        ("Nearest Neighbor AVX2", nearest_neighbor_resize_avx2),
        ("Bilinear", bilinear_resize),
        ("Bilinear AVX2", bilinear_resize_avx2)
    ]

    print("Testing resize performance from 1080p to 1080p:")
    for name, func in resize_functions:
        fps = test_resize_fps(func, src_image, dst_image, width, height)
        print(f"{name}: {fps:.2f} FPS")

    free_image_rgba(src_image)
    free_image_rgba(dst_image)

if __name__ == "__main__":
    main()
