from setuptools import setup, find_packages
import pkg_resources

"""
General setup
"""
setup(
    name="distinstall-python",
    version="0.4.5",
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
    entry_points = {
        # Set entry points here
        "console_scripts" : [
            "main = src.distinstall-python.main:main",
        ],
    },
)

"""
Entry point setup
"""
named_objects = {}

# Loop through all entry points in a group and populate named objects dictionary
for entry_point in pkg_resources.iter_entry_points(group='main'):
    # Populate named objects dictionary mapping with the entry points
    named_objects.update({entry_point.name : entry_point.load()})

