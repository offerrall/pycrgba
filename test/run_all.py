import time
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, copy_image
from pycrgba_cffi import ffi, lib

# Importar funciones de prueba de los archivos individuales
from create_image import test_create_image
from copy_image import test_copy_image as test_copy_image_same_size
from copy_diff_size import test_copy_image as test_copy_image_diff_size
from fill_image import test_fill_image
from overlay import test_overlay_image

def run_all_tests():
    sizes = [
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160)   # 4K
    ]

    results = {}

    print("Running Performance Tests for All Functions")
    print("===========================================")

    for width, height in sizes:
        print(f"\nImage size: {width}x{height}")
        results[(width, height)] = {}

        # Create Image Test
        create_fps = test_create_image(width, height)
        results[(width, height)]['create'] = create_fps

        # Copy Image (Same Size) Test
        copy_same_fps = test_copy_image_same_size(width, height)
        results[(width, height)]['copy_same'] = copy_same_fps

        # Copy Image (Different Size) Test
        copy_diff_normal = test_copy_image_diff_size(width, height, use_avx2=False)
        copy_diff_avx2 = test_copy_image_diff_size(width, height, use_avx2=True)
        results[(width, height)]['copy_diff'] = (copy_diff_normal, copy_diff_avx2)

        # Fill Image Test
        fill_normal = test_fill_image(width, height, use_avx2=False)
        fill_avx2 = test_fill_image(width, height, use_avx2=True)
        results[(width, height)]['fill'] = (fill_normal, fill_avx2)

        # Overlay Image Test
        overlay_normal_trans = test_overlay_image(width, height, use_avx2=False, transparent=True)
        overlay_avx2_trans = test_overlay_image(width, height, use_avx2=True, transparent=True)
        overlay_normal_opaque = test_overlay_image(width, height, use_avx2=False, transparent=False)
        overlay_avx2_opaque = test_overlay_image(width, height, use_avx2=True, transparent=False)
        results[(width, height)]['overlay'] = (overlay_normal_trans, overlay_avx2_trans, overlay_normal_opaque, overlay_avx2_opaque)

    print("\nPerformance Test Results")
    print("========================")

    for size, data in results.items():
        width, height = size
        print(f"\nImage Size: {width}x{height}")
        print("---------------------------")
        print(f"Create Image:     {data['create']:.2f} FPS")
        print(f"Copy Image (Same Size): {data['copy_same']:.2f} FPS")
        print(f"Copy Image (Different Size):")
        print(f"  Normal:         {data['copy_diff'][0]:.2f} FPS")
        print(f"  AVX2:           {data['copy_diff'][1]:.2f} FPS")
        print(f"  Speedup:        {data['copy_diff'][1]/data['copy_diff'][0]:.2f}x")
        print(f"Fill Image:")
        print(f"  Normal:         {data['fill'][0]:.2f} FPS")
        print(f"  AVX2:           {data['fill'][1]:.2f} FPS")
        print(f"  Speedup:        {data['fill'][1]/data['fill'][0]:.2f}x")
        print(f"Overlay Image:")
        print(f"  Transparent:")
        print(f"    Normal:       {data['overlay'][0]:.2f} FPS")
        print(f"    AVX2:         {data['overlay'][1]:.2f} FPS")
        print(f"    Speedup:      {data['overlay'][1]/data['overlay'][0]:.2f}x")
        print(f"  Opaque:")
        print(f"    Normal:       {data['overlay'][2]:.2f} FPS")
        print(f"    AVX2:         {data['overlay'][3]:.2f} FPS")
        print(f"    Speedup:      {data['overlay'][3]/data['overlay'][2]:.2f}x")

if __name__ == "__main__":
    run_all_tests()
    input("Press Enter to exit...")