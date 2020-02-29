"""Script for uploading a new version of our package to PyPi"""

# Built-in
import os
import sys
from shutil import rmtree


# --------------------------------------------------------------------------------
# > Functions
# --------------------------------------------------------------------------------
def package_our_code():
    """Clears the previous build and generate a new one"""
    # Set current working directory
    file = sys.argv[0]
    root_dir = os.path.dirname(file)
    os.chdir(root_dir)
    # Clear previous packaged build
    package_name = "jklib"
    rmtree(f"{package_name}.egg-info")
    rmtree("build")
    rmtree("dist")
    # Generate new build and upload it
    os.system("python setup.py sdist bdist_wheel")
    os.system("python twine upload dist/*")


# --------------------------------------------------------------------------------
# > Main
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    package_our_code()
