import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_log",
    version="0.0.1",
    author="Lucas Resende",
    author_email="lucasresone@gmail.com",
    description="Log request, response and erros in file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mandala21/django_log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)