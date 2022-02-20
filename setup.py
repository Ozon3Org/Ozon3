import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ozone",
    version="1.0.0",
    author="Milind Sharma",
    url="https://github.com/Milind220/Ozone",
    description="A package to get air quality data using the WAQI API",
    license="GPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["ozone", "ozone.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Packages",
    ],
    setup_requires=["pytest-runner", "flake8", "black"],
    tests_require=["pytest"],
    python_requires=">=3.6",
    py_modules=["ozone"],
    package_dir={"": "ozone/"},
    install_requires=[
        "pandas==1.4.0",
        "numpy==1.22.1",
        "requests==2.27.1",
        "entrypoints==0.3",
        "idna==3.3",
        "iniconfig==1.1.1",
        "pluggy==1.0.0",
        "py==1.11.0",
        "pytz==2021.1",
        "terminado==0.9.4",
        "toml==0.10.2",
        "tomli==2.0.1",
        "urllib3==1.26.8",
        "webencodings==0.5.1",
    ],
)

# TODO: Check the requirements and trim the install_requires list.
