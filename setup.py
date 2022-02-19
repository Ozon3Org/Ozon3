import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ozone", 
    version="1.0.0",                        # The initial release version
    author="Milind Sharma",                     # Full name of the author
    description="A package to get air quality data using the WAQI API",
    license='GPLv3+',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['ozone', 'ozone.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Packages',
    ],                                      
    python_requires='>=3.6',                
    py_modules=["ozone"],            
    package_dir={'':'ozone/'},     # Directory of the source code of the package
    install_requires=[
        'pandas==1.4.0',
        'numpy==1.22.1',
        "requests==2.27.1",

    ]                     # Install other dependencies if any
)