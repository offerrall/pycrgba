import time
from pycrgba import create_image_rgba, free_image_rgba, copy_image, fill_image_rgba

def test_copy_image(width, height, iterations=100):
    # Create source and destination images
    src_image = create_image_rgba(width, height)
    dst_image = create_image_rgba(width, height)

    # Fill source image with a color
    fill_image_rgba(src_image, width, height, 255, 0, 0, 255)  # Red color

    start_time = time.time()
    for _ in range(iterations):
        copy_image(dst_image, src_image, width, height)
    end_time = time.time()

    # Free the allocated memory
    free_image_rgba(src_image)
    free_image_rgba(dst_image)

    total_time = end_time - start_time
    fps = iterations / total_time
    return fps

def run_copy_image_tests():
    print("Performance Tests for copy_image")
    print("--------------------------------")

    # Test different image sizes
    sizes = [
        (640, 480),    # VGA
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160),  # 4K
    ]



    for width, height in sizes:
        fps = test_copy_image(width, height)
        print(f"Copy Image ({width}x{height}): {fps:.2f} FPS")

if __name__ == "__main__":
    run_copy_image_tests()
    input("Press Enter to exit...")