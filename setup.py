import setuptools

with open('README.md') as f:
    long_description = f.read()

with open('kathymurdochhomepage/release.py') as f:
    # includes version
    exec(f.read())

setuptools.setup(
    name="kathymurdochhomepage",
    version=version,
    author="Kathy Murdoch",
    author_email="kathy@nivan.net",
    description="Homepage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iguanaonmystack/kathymurdochhomepage",
    packages=setuptools.find_packages(),
    install_requires=[
        'Flask',
        'Flash-Caching',
        'Flask-Genshi',# currently needs to be a branch
                       # eg https://github.com/vthriller/flask-genshi
        'Genshi==0.8', # could we have a release please Edgewall?
        # TODO - use dependency_links: https://python-packaging.readthedocs.io/en/latest/dependencies.html
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 3.7 needed for module-level __getattr__ in helpers.py
    python_requires='>=3.7',
)
