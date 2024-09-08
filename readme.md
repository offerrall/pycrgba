# pycrgba

## Overview

pycrgba is a personal learning project that provides Python bindings for basic image manipulation using optimized C functions. This package leverages CFFI to create a bridge between Python and C, allowing for high-performance image processing operations.

## Features

- Basic image operations (create, copy, fill)
- Image overlay with alpha blending
- Nearest neighbor resizing
- AVX2 acceleration for supported operations

## Installation

To install pycrgba, follow these steps:

```
git clone https://github.com/offerrall/pycrgba.git
cd pycrgba
python install.py
```

## Usage

Here's a quick example of how to use pycrgba:

```python
from pycrgba import create_image_rgba, fill_image_rgba, free_image_rgba

# Create a new RGBA image
image = create_image_rgba(800, 600)

# Fill the image with red
fill_image_rgba(image, 800, 600, 255, 0, 0, 255)

# Don't forget to free the allocated memory
free_image_rgba(image)
```

For a complete list of available functions, please refer to the [pycrgba/pycrgba.py](https://github.com/offerrall/pycrgba/blob/main/pycrgba/pycrgba.py) file in the repository. This file contains all the Python bindings for the C functions, providing a comprehensive overview of the library's capabilities.

## License

This project is open-source and available under the MIT License.