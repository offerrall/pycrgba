import time
from pycrgba import (
    create_image_rgba,
    free_image_rgba,
    nearest_neighbor_resize,
    nearest_neighbor_resize_avx2
)

def test_resize_fps(resize_func, src_image, dst_image, src_width, src_height, dst_width, dst_height, num_frames=100):
    start_time = time.time()
    for _ in range(num_frames):
        resize_func(src_image, dst_image, src_width, src_height, dst_width, dst_height)
    end_time = time.time()
    fps = num_frames / (end_time - start_time)
    return fps

def main():
    src_width, src_height = 1920, 1080
    dst_width, dst_height = 1920, 1080
    src_image = create_image_rgba(src_width, src_height)
    dst_image = create_image_rgba(dst_width, dst_height)

    for y in range(src_height):
        for x in range(src_width):
            index = (y * src_width + x) * 4
            src_image[index] = x % 256
            src_image[index + 1] = y % 256
            src_image[index + 2] = (x + y) % 256
            src_image[index + 3] = 255

    resize_functions = [
        ("Nearest Neighbor", nearest_neighbor_resize),
        ("Nearest Neighbor AVX2", nearest_neighbor_resize_avx2)
    ]

    print(f"Testing resize performance from {src_width}x{src_height} to {dst_width}x{dst_height}:")
    for name, func in resize_functions:
        fps = test_resize_fps(func, src_image, dst_image, src_width, src_height, dst_width, dst_height)
        print(f"{name}: {fps:.2f} FPS")

    free_image_rgba(src_image)
    free_image_rgba(dst_image)

if __name__ == "__main__":
    main()
