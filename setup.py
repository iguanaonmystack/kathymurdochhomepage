import setuptools

with open('README.md') as f:
    long_description = fh.read()

with open('kathymurdochhomepage/release.py') as f:
    # includes version
    exec(f.read())

setuptools.setup(
    name="example-pkg-your-username",
    version=version,
    author="Kathy Murdoch",
    author_email="kathy@nivan.net",
    description="Homepage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iguanaonmystack/kathymurdochhomepage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
