import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuning_fork",
    version="1.5.1",
    author="Garrett Credi",
    author_email="gcc@ameritech.net",
    description="A clip/sample auto tuner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddxtanx/TuningFork",
    packages=["tuning_fork", "tuning_fork.tools"],
    py_modules=["tuning_fork.main"],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Mixers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Utilities"
    ),
    install_requires=["librosa", "numpy", "pysoundfile"]
)
