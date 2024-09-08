import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba
from pycrgba_cffi import ffi, lib

def test_copy_image(width, height, iterations=100, use_avx2=False):
    src_image = create_image_rgba(width, height)
    dest_image = create_image_rgba(width, height)
    
    # Fill source image with a color pattern
    fill_image_rgba(src_image, width, height, 255, 0, 0, 255)
    
    # Copy dimensions slightly smaller to ensure we're not just doing a straight memcpy
    copy_width = width - 2
    copy_height = height - 2
    
    copy_func = lib.copy_image_diff_size_no_alpha_avx2 if use_avx2 else lib.copy_image_diff_size_no_alpha
    
    start_time = time.time()
    for _ in range(iterations):
        copy_func(dest_image, width, height, src_image, copy_width, copy_height, 1, 1)
    end_time = time.time()
    
    free_image_rgba(src_image)
    free_image_rgba(dest_image)
    
    total_time = end_time - start_time
    fps = iterations / total_time
    return fps

def run_copy_image_tests():
    print("Performance Tests for copy_image_diff_size_no_alpha (Same Size)")
    print("--------------------------------------------------------------")
    
    sizes = [
        (640, 480),    # VGA
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160)   # 4K
    ]
    
    for width, height in sizes:
        print(f"\nImage size: {width}x{height}")
        
        fps_normal = test_copy_image(width, height)
        fps_avx2 = test_copy_image(width, height, use_avx2=True)
        
        print(f"  Normal:  {fps_normal:.2f} FPS")
        print(f"  AVX2:    {fps_avx2:.2f} FPS")
        print(f"  Speedup: {fps_avx2/fps_normal:.2f}x")

if __name__ == "__main__":
    run_copy_image_tests()
    input("Press Enter to exit...")