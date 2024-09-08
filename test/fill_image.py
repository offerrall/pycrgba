import time
import ctypes
from pycrgba import create_image_rgba, free_image_rgba
from pycrgba_cffi import ffi, lib

def test_fill_image(width, height, iterations=1000, use_avx2=False):
    image = create_image_rgba(width, height)
    
    fill_func = lib.fill_image_rgba_avx2 if use_avx2 else lib.fill_image_rgba
    
    start_time = time.time()
    for _ in range(iterations):
        fill_func(image, width, height, 255, 0, 0, 255)  # Fill with red
    end_time = time.time()
    
    free_image_rgba(image)
    
    total_time = end_time - start_time
    fps = iterations / total_time
    return fps

def run_fill_image_tests():
    print("Performance Tests for fill_image_rgba")
    print("-------------------------------------")
    
    sizes = [
        (64, 64),      # Small LED panel
        (128, 128),    # Medium LED panel
        (256, 256),    # Large LED panel
        (640, 480),    # VGA
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160),  # 4K
    ]
    
    for width, height in sizes:
        fps_normal = test_fill_image(width, height)
        fps_avx2 = test_fill_image(width, height, use_avx2=True)
        
        print(f"Fill Image ({width}x{height}):")
        print(f"  Normal: {fps_normal:.2f} FPS")
        print(f"  AVX2:   {fps_avx2:.2f} FPS")
        print(f"  Speedup: {fps_avx2/fps_normal:.2f}x")
        print()

if __name__ == "__main__":
    run_fill_image_tests()
    input("Press Enter to exit...")