import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Git Clean Commit',  
    version='0.2',
    scripts=['git-clean-commit'] ,
    author="Low Yiyiu",
    author_email="lowyiyiu@gmail.com",
    description="Easily clean commit history",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lowyiyiu/git-clean-commit",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )