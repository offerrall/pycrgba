import os
from PIL import Image
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba
from pycrgba_cffi import ffi, lib

def save_image(data, width, height, filename):
    buffer = ffi.buffer(data, width * height * 4)
    img = Image.frombytes('RGBA', (width, height), buffer)
    img.save(filename)
    print(f"Saved: {filename}")

def test_blit_visual_comprehensive():
    width, height = 400, 300
    small_size = 100
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    # Create background image (light blue)
    background = create_image_rgba(width, height)
    fill_image_rgba(background, width, height, 173, 216, 230, 255)
    save_image(background, width, height, os.path.join(output_dir, "background.png"))

    # Create small object (red square)
    small_obj = create_image_rgba(small_size, small_size)
    fill_image_rgba(small_obj, small_size, small_size, 255, 0, 0, 255)

    # Test cases
    test_cases = [
        ("center", width//2 - small_size//2, height//2 - small_size//2),
        ("left", -small_size//2, height//2 - small_size//2),
        ("right", width - small_size//2, height//2 - small_size//2),
        ("top", width//2 - small_size//2, -small_size//2),
        ("bottom", width//2 - small_size//2, height - small_size//2),
        ("top_left", -small_size//2, -small_size//2),
        ("top_right", width - small_size//2, -small_size//2),
        ("bottom_left", -small_size//2, height - small_size//2),
        ("bottom_right", width - small_size//2, height - small_size//2),
        ("completely_off_left", -small_size, height//2 - small_size//2),
        ("completely_off_right", width, height//2 - small_size//2),
        ("completely_off_top", width//2 - small_size//2, -small_size),
        ("completely_off_bottom", width//2 - small_size//2, height),
    ]

    for case_name, x, y in test_cases:
        # Test normal blit
        result_normal = create_image_rgba(width, height)
        fill_image_rgba(result_normal, width, height, 173, 216, 230, 255)
        lib.blit(result_normal, width, height, small_obj, small_size, small_size, x, y)
        save_image(result_normal, width, height, os.path.join(output_dir, f"blit_{case_name}.png"))

        # Test AVX2 blit
        result_avx2 = create_image_rgba(width, height)
        fill_image_rgba(result_avx2, width, height, 173, 216, 230, 255)
        lib.blit_avx2(result_avx2, width, height, small_obj, small_size, small_size, x, y)
        save_image(result_avx2, width, height, os.path.join(output_dir, f"blit_avx2_{case_name}.png"))

        free_image_rgba(result_normal)
        free_image_rgba(result_avx2)

    # Clean up
    free_image_rgba(background)
    free_image_rgba(small_obj)

if __name__ == "__main__":
    test_blit_visual_comprehensive()
    print("Comprehensive blit visual test images have been generated in the 'test_output' directory.")