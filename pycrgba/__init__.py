"""
`pycrgba` provides Python bindings for basic image manipulation, leveraging optimized C functions for high-performance image processing, including AVX2 acceleration where supported. This package is ideal for tasks that require direct control over image data at a low level.

## Quick Start

```python
from pycrgba import create_image_rgba, fill_image_rgba, free_image_rgba

# Create a new RGBA image with a specified width and height
image = create_image_rgba(800, 600)

# Fill the image with a solid color (red in this case)
fill_image_rgba(image, 800, 600, 255, 0, 0, 255)

# Always remember to free the memory allocated by the C functions
free_image_rgba(image)
"""

from .pycrgba import *