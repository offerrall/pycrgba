from setuptools import setup

setup(
    name="pycrgba",
    version="0.1",
    description="Python bindings for basic image processing with C",
    author="Beltrán Offerrall",
    author_email="offerrallps4@gmail.com",
    packages=["pycrgba"],
    setup_requires=["cffi"],
    cffi_modules=["pycrgba/build.py:ffibuilder"],
    install_requires=["cffi"],
)
