"""Script for uploading a new version of our package to PyPi"""

# Built-in
import os
import sys
from shutil import rmtree

# Third-party
from local_settings import PYPI_PASSWORD, PYPI_USERNAME


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
    setup_cmd = "python setup.py sdist bdist_wheel"
    upload_cmd = f"twine upload dist/* -u {PYPI_USERNAME} -p {PYPI_PASSWORD}"
    os.system(f"{setup_cmd} & {upload_cmd}")


# --------------------------------------------------------------------------------
# > Main
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    package_our_code()
