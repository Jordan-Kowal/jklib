"""Setup file for the PyPi packaging."""


# Third-party
from setuptools import find_packages, setup

# --------------------------------------------------------------------------------
# > Variables
# --------------------------------------------------------------------------------
VERSION = "3.2.1"
packages = find_packages()
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# --------------------------------------------------------------------------------
# > Setup
# --------------------------------------------------------------------------------
setup(
    # General
    name="jklib",
    version=VERSION,
    license="MIT",
    # Description
    description="Package with utility functions on many different subjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Author
    author="Jordan Kowal",
    author_email="kowaljordan@gmail.com",
    # URLs
    url="https://github.com/Jordan-Kowal/jklib",
    download_url=f"https://github.com/Jordan-Kowal/jklib/archive/v{VERSION}.tar.gz",
    # Packages
    packages=packages,
    install_requires=[],
    # Other info
    keywords=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
