import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
        name="freesia",
        version="3.3.2",
        description="Takes Qt for Python and adds extra functionality including automatic scaling",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/lgwilliams/freesia.git",
        author="Luke Williams",
        author_email="luke@dominoid.net",
        license="LGPL v2.1",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
        packages=["freesia"],
        include_package_data=True,
        install_requires=["PySide2"],
)       

