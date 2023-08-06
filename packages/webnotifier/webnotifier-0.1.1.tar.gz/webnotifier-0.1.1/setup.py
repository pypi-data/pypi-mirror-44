import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webnotifier",
    version="0.1.1",
    author="Pol MP",
    author_email="pol.moreno30@gmail.com",
    description="A package for notifying any webpage change",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/polmp/webnotifier",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests>=2.21.0',
          'lxml>=4.3.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)