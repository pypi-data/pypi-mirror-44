import setuptools


with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="cqc",
    version="2.2.0",
    author="Axel Dahlberg",
    author_email="e.a.dahlberg@tudelft.nl",
    description="The CQC interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoftwareQuTech/CQC-Python",
    include_package_data=True,
    package_data={
        'cqc': ['settings.ini']
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
