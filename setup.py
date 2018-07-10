import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuning_fork",
    version="1.4",
    author="Garrett Credi",
    author_email="gcc@ameritech.net",
    description="A clip/sample auto tuner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddxtanx/TuningFork",
    packages=["tuning_fork", "tuning_fork.tools"],
    py_modules=["tuning_fork.main"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=["librosa", "numpy", "pysoundfile"]
)
