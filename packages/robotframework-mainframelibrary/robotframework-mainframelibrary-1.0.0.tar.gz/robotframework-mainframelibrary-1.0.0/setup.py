import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-mainframelibrary",
    version="1.0.0",
    author="Nadezhda Baranova",
    description="Robot Framework Library for Mainframe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NadezhdaBaranova/robotframework-mainframelibrary",
    py_modules=['MainframeLibrary'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
