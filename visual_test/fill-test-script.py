import os
from PIL import Image
from pycrgba import create_image_rgba, free_image_rgba, fill_image_rgba, fill_image_rgba_avx2
from pycrgba_cffi import ffi

def save_image(data, width, height, filename):
    buffer = ffi.buffer(data, width * height * 4)
    img = Image.frombytes('RGBA', (width, height), buffer)
    img.save(filename)
    print(f"Saved: {filename}")

def test_fill():
    width, height = 400, 300
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    # Test normal fill
    img1 = create_image_rgba(width, height)
    fill_image_rgba(img1, width, height, 255, 0, 0, 255)  # Red
    save_image(img1, width, height, os.path.join(output_dir, "red_fill.png"))

    # Test AVX2 fill
    img2 = create_image_rgba(width, height)
    fill_image_rgba_avx2(img2, width, height, 0, 255, 0, 255)  # Green
    save_image(img2, width, height, os.path.join(output_dir, "green_fill_avx2.png"))

    # Clean up
    free_image_rgba(img1)
    free_image_rgba(img2)

if __name__ == "__main__":
    test_fill()
    print("Fill test images have been generated in the 'test_output' directory.")
