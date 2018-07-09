import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuning_fork_cli",
    version="2",
    author="Garrett Credi",
    author_email="gcc@ameritech.net",
    description="CLI for tuning_fork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddxtanx/TuningFork",
    py_modules=["main"],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=["tuning_fork"],
    entry_points={
        'console_scripts': [
            'tuning-fork = main:main'
        ]
    }
)
