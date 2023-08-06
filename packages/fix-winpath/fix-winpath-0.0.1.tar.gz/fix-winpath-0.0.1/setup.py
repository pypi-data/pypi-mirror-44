import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fix-winpath",
    version="0.0.1",
    author="Udi Oron",
    author_email="udioron@gmail.com",
    description="Fixes windows PATH environment variable to find python.exe, pip.exe and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nonZero/fix-winpath",
    py_modules=['fix_winpath'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: Microsoft :: Windows",
    ],
)
