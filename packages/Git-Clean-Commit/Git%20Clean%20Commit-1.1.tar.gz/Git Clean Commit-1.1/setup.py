import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Git Clean Commit',  
    version='1.1',
    scripts=['git-clean-commit'] ,
    author="Low Yiyiu",
    author_email="lowyiyiu@gmail.com",
    description="Easily clean commit history",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lowyiyiu/git-clean-commit",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )