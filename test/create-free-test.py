import time
from pycrgba import create_image_rgba, free_image_rgba

def test_create_free(iterations=1000):
    width, height = 1920, 1080
    total_create_time = 0
    total_free_time = 0

    for _ in range(iterations):
        start_time = time.time()
        image = create_image_rgba(width, height)
        create_time = time.time() - start_time
        total_create_time += create_time

        start_time = time.time()
        free_image_rgba(image)
        free_time = time.time() - start_time
        total_free_time += free_time

    avg_create_time = total_create_time / iterations
    avg_free_time = total_free_time / iterations

    create_fps = 1 / avg_create_time if avg_create_time > 0 else float('inf')
    free_fps = 1 / avg_free_time if avg_free_time > 0 else float('inf')

    print(f"Resolution: {width}x{height}")
    print(f"create_image_rgba: {create_fps:.2f} FPS")
    print(f"free_image_rgba: {free_fps:.2f} FPS")

if __name__ == "__main__":
    test_create_free()
