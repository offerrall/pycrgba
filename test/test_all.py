import time
import platform
from pycrgba import (
    create_image_rgba, free_image_rgba, fill_image_rgba, blend, blend_avx2, blend_neon,
    blit_same_size, blit, blit_avx2, blit_neon,
    fill_image_rgba_avx2, fill_image_rgba_neon,
    nearest_neighbor_resize, nearest_neighbor_resize_avx2, nearest_neighbor_resize_neon
)

def run_blend_test(iterations=100):
    width, height = 1920, 1080
    background = create_image_rgba(width, height)
    overlay = create_image_rgba(width, height)
    fill_image_rgba(background, width, height, 255, 0, 0, 255)
    fill_image_rgba(overlay, width, height, 0, 255, 0, 128)

    fps_results = {}
    for func in [blend, blend_avx2, blend_neon]:
        total_time = 0
        for _ in range(iterations):
            start_time = time.time()
            func(background, overlay, width, height, width, height, 0, 0)
            total_time += time.time() - start_time
        fps = iterations / total_time
        fps_results[func.__name__] = fps

    free_image_rgba(background)
    free_image_rgba(overlay)
    return fps_results

def run_blit_test(iterations=100):
    width, height = 1920, 1080
    src = create_image_rgba(width, height)
    dst = create_image_rgba(width, height)
    fill_image_rgba(src, width, height, 0, 255, 0, 255)

    fps_results = {}
    for func in [blit, blit_avx2, blit_neon]:
        total_time = 0
        for _ in range(iterations):
            fill_image_rgba(dst, width, height, 255, 0, 0, 255)
            start_time = time.time()
            func(dst, width, height, src, width, height, 0, 0)
            total_time += time.time() - start_time
        fps = iterations / total_time
        fps_results[func.__name__] = fps

    free_image_rgba(src)
    free_image_rgba(dst)
    return fps_results

def run_fill_test(iterations=100):
    width, height = 1920, 1080
    image = create_image_rgba(width, height)

    fps_results = {}
    for func in [fill_image_rgba, fill_image_rgba_avx2, fill_image_rgba_neon]:
        total_time = 0
        for _ in range(iterations):
            start_time = time.time()
            func(image, width, height, 255, 0, 0, 255)
            total_time += time.time() - start_time
        fps = iterations / total_time
        fps_results[func.__name__] = fps

    free_image_rgba(image)
    return fps_results

def run_resize_test(iterations=100):
    src_width, src_height = 1920, 1080
    dst_width, dst_height = 1920, 1080
    src_image = create_image_rgba(src_width, src_height)
    dst_image = create_image_rgba(dst_width, dst_height)

    fps_results = {}
    for func in [nearest_neighbor_resize, nearest_neighbor_resize_avx2, nearest_neighbor_resize_neon]:
        total_time = 0
        for _ in range(iterations):
            start_time = time.time()
            func(src_image, dst_image, src_width, src_height, dst_width, dst_height)
            total_time += time.time() - start_time
        fps = iterations / total_time
        fps_results[func.__name__] = fps

    free_image_rgba(src_image)
    free_image_rgba(dst_image)
    return fps_results

def run_all_tests():
    print(f"Running tests on {platform.machine()} platform")
    print(f"Python version: {platform.python_version()}")
    print("Resolution: 1920x1080")

    all_results = {}
    all_results.update(run_blend_test())
    all_results.update(run_blit_test())
    all_results.update(run_fill_test())
    all_results.update(run_resize_test())

    print("\nResults:")
    for func, fps in all_results.items():
        print(f"{func}: {fps:.2f} FPS")

    avg_fps = sum(all_results.values()) / len(all_results)
    print(f"\nAverage FPS across all tests: {avg_fps:.2f}")

if __name__ == "__main__":
    run_all_tests()