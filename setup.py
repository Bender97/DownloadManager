import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()
long_description = "..."

setuptools.setup(
    name="download-manager", # Replace with your own username
    version="0.0.1",
    author="Daniel Fusaro",
    author_email="bopallino@gmail.com",
    description="A first working version of download manager for unipd moodle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bender97/DownloadManager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)