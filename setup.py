from setuptools import setup, find_packages

setup(
    name="bharatOCR",
    version="1.0.1",
    description="An OCR package for detection, script identification, and text recognition in Indian scripts",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.md").read(),
    long_description_content_type="text/markdown",
    author="Anik De",
    author_email="anekde@gmail.com",
    url="https://github.com/Bhashini-IITJ/BharatOCR",
    packages=find_packages(),
    python_requires='>=3.9',
)