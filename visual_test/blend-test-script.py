import os
from PIL import Image
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba
from pycrgba_cffi import ffi, lib

def save_image(data, width, height, filename):
    buffer = ffi.buffer(data, width * height * 4)
    img = Image.frombytes('RGBA', (width, height), buffer)
    img.save(filename)
    print(f"Saved: {filename}")

def test_blend():
    width, height = 400, 300
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    # Create background image (red)
    background = create_image_rgba(width, height)
    fill_image_rgba(background, width, height, 255, 0, 0, 255)
    save_image(background, width, height, os.path.join(output_dir, "background.png"))

    # Create overlay image (semi-transparent green)
    overlay = create_image_rgba(width, height)
    fill_image_rgba(overlay, width, height, 0, 255, 0, 128)
    save_image(overlay, width, height, os.path.join(output_dir, "overlay.png"))

    # Test normal blend
    blended = create_image_rgba(width, height)
    fill_image_rgba(blended, width, height, 255, 0, 0, 255)  # Copy background
    lib.blend(blended, overlay, width, height, width, height, 0, 0)
    save_image(blended, width, height, os.path.join(output_dir, "blend_result.png"))

    # Test AVX2 blend
    blended_avx2 = create_image_rgba(width, height)
    fill_image_rgba(blended_avx2, width, height, 255, 0, 0, 255)  # Copy background
    lib.blend_avx2(blended_avx2, overlay, width, height, width, height, 0, 0)
    save_image(blended_avx2, width, height, os.path.join(output_dir, "blend_avx2_result.png"))

    # Clean up
    free_image_rgba(background)
    free_image_rgba(overlay)
    free_image_rgba(blended)
    free_image_rgba(blended_avx2)

if __name__ == "__main__":
    test_blend()
    print("Blend test images have been generated in the 'test_output' directory.")
