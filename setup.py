from setuptools import setup, find_packages

setup(
    name="pybaseballdatana",
    version="0.1.0",
    description="Baseball data and analysis in Python",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    packages=find_packages(),
    package_data={"pybaseballdatana": ["*.csv"]},
    include_package_data=True
)
