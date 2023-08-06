import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testmodelkb1",
    version="0.0.4",
    author="Sirisha Rella",
    author_email="srnk2@mail.umkc.edu",
    description="ModelKB",
    long_description="ModelKB",
    long_description_content_type="text/markdown",
    url="https://github.com/SirishaRella/Xsequential_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)