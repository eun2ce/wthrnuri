from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
    name="wthrnuri",
    version="0.1.0",
    author="eun2ce",
    author_email="joeun2ce@gmail.com",
    description="Natural language based weather information service package",
    install_requires=required,
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11"
    ],
    packages=find_packages(include=["wthrnuri"])
)