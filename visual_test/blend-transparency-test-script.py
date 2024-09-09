import os
from PIL import Image
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba
from pycrgba_cffi import ffi, lib

def save_image(data, width, height, filename):
    buffer = ffi.buffer(data, width * height * 4)
    img = Image.frombytes('RGBA', (width, height), buffer)
    img.save(filename)
    print(f"Saved: {filename}")

def create_gradient_image(width, height):
    image = create_image_rgba(width, height)
    for y in range(height):
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = 128
            a = int(255 * (x + y) / (width + height))
            fill_image_rgba(image, 1, 1, r, g, b, a)
            lib.blit(image, width, height, image, 1, 1, x, y)
    return image

def test_blend_visual_comprehensive():
    width, height = 400, 300
    small_size = 200
    output_dir = "test_output_blend"
    os.makedirs(output_dir, exist_ok=True)

    # Create background image (light blue)
    background = create_image_rgba(width, height)
    fill_image_rgba(background, width, height, 173, 216, 230, 255)
    save_image(background, width, height, os.path.join(output_dir, "background.png"))

    # Create overlay image (gradient with transparency)
    overlay = create_gradient_image(small_size, small_size)
    save_image(overlay, small_size, small_size, os.path.join(output_dir, "overlay.png"))

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
        # Test normal blend
        result_normal = create_image_rgba(width, height)
        fill_image_rgba(result_normal, width, height, 173, 216, 230, 255)
        lib.blend(result_normal, overlay, width, height, small_size, small_size, x, y)
        save_image(result_normal, width, height, os.path.join(output_dir, f"blend_{case_name}.png"))

        # Test AVX2 blend
        result_avx2 = create_image_rgba(width, height)
        fill_image_rgba(result_avx2, width, height, 173, 216, 230, 255)
        lib.blend_avx2(result_avx2, overlay, width, height, small_size, small_size, x, y)
        save_image(result_avx2, width, height, os.path.join(output_dir, f"blend_avx2_{case_name}.png"))

        free_image_rgba(result_normal)
        free_image_rgba(result_avx2)

    # Clean up
    free_image_rgba(background)
    free_image_rgba(overlay)

if __name__ == "__main__":
    test_blend_visual_comprehensive()
    print("Comprehensive blend visual test images have been generated in the 'test_output_blend' directory.")
