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
        'Flask-Caching',
        'Flask-Genshi==0.5+iguanaonmystack',
        'Genshi==0.8', # could we have a release please Edgewall?
        'Bleach',
    ],
    dependency_links=[
        'https://github.com/iguanaonmystack/flask-genshi/tarball/0.5+iguanaonmystack#egg=flask-genshi-0.5+iguanaonmystack'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 3.7 needed for module-level __getattr__ in helpers.py
    python_requires='>=3.7',
)
