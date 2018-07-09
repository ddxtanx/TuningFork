import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuning_fork",
    version="1.2.1",
    author="Garrett Credi",
    author_email="gcc@ameritech.net",
    description="A clip/sample auto tuner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddxtanx/TuningFork",
    py_modules=["tuning_fork"],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=["librosa", "scipy", "numpy"]
)
