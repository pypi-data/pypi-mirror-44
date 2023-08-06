from setuptools import setup

readme_markdown = None
with open("README.md") as f:
    readme_markdown = f.read()

setup(
    name="texlivemetadata",
    version="0.1.2",
    url="https://github.com/YtoTech/python-texlivemetadata",
    license="MIT",
    author="Yoan Tournade",
    author_email="yoan@ytotech.com",
    description="A library for getting information on TexLive installation",
    long_description=readme_markdown,
    long_description_content_type="text/markdown",
    packages=["texlivemetadata"],
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=[],
)
