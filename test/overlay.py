import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba
from pycrgba_cffi import ffi, lib

def test_overlay_image(width, height, iterations=100, use_avx2=False, transparent=True):
    background = create_image_rgba(width, height)
    overlay = create_image_rgba(width, height)
    
    # Fill background with blue
    fill_image_rgba(background, width, height, 0, 0, 255, 255)
    
    if transparent:
        # Fill overlay with semi-transparent red
        fill_image_rgba(overlay, width, height, 255, 0, 0, 128)
    else:
        # Fill overlay with opaque red
        fill_image_rgba(overlay, width, height, 255, 0, 0, 255)
    
    overlay_func = lib.overlay_image_with_coords_avx2 if use_avx2 else lib.overlay_image_with_coords
    
    start_time = time.time()
    for _ in range(iterations):
        overlay_func(background, overlay, width, height, width, height, 0, 0)
    end_time = time.time()
    
    free_image_rgba(background)
    free_image_rgba(overlay)
    
    total_time = end_time - start_time
    fps = iterations / total_time
    return fps

def run_overlay_image_tests():
    print("Performance Tests for overlay_image_with_coords")
    print("-----------------------------------------------")
    
    sizes = [
        (640, 480),    # VGA
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160)   # 4K
    ]
    
    for width, height in sizes:
        print(f"\nImage size: {width}x{height}")
        
        for transparent in [True, False]:
            transparency_mode = "Transparent" if transparent else "Opaque"
            print(f"  {transparency_mode} overlay:")
            
            fps_normal = test_overlay_image(width, height, transparent=transparent)
            fps_avx2 = test_overlay_image(width, height, use_avx2=True, transparent=transparent)
            
            print(f"    Normal:  {fps_normal:.2f} FPS")
            print(f"    AVX2:    {fps_avx2:.2f} FPS")
            print(f"    Speedup: {fps_avx2/fps_normal:.2f}x")

if __name__ == "__main__":
    run_overlay_image_tests()
    input("Press Enter to exit...")