import time
from pycrgba import create_image_rgba, free_image_rgba

def test_create_image(width, height, iterations=100):
    start_time = time.time()
    for _ in range(iterations):
        image = create_image_rgba(width, height)
        free_image_rgba(image)
    end_time = time.time()
    
    total_time = end_time - start_time
    fps = iterations / total_time
    return fps

def run_create_image_tests():
    print("Performance Tests for create_image_rgba")
    print("---------------------------------------")
    
    # Test different image sizes
    sizes = [
        (640, 480),    # VGA
        (1280, 720),   # 720p
        (1920, 1080),  # 1080p
        (3840, 2160),  # 4K
    ]
    
    for width, height in sizes:
        fps = test_create_image(width, height)
        print(f"Create Image ({width}x{height}): {fps:.2f} FPS")

if __name__ == "__main__":
    run_create_image_tests()
    input("Press Enter to exit...")