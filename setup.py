from setuptools import setup, find_packages

setup(
    name="distinstall-python",
    version="0.4.0",
    description = "Portable, Customizable and Modular distribution installation library/framework",
    author="Thanatisia",
    author_email="55834101+Thanatisia@users.noreply.github.com",
    packages=find_packages(),
    package_dir={'':'src/distinstall-python'},
    install_requires=[
        # List of dependencies here
        "ruamel.yaml"
    ],
    url="https://github.com/Thanatisia/distinstall-python",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming language :: Python :: 3.11",
    ],
)
