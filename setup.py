import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sequence_generator", # Replace with your own username
    version="0.0.1",
    author="Clayton",
    author_email="clayton.bonelli@agriness.com",
    description="Sequence generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claytonbonelli/sequence_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)