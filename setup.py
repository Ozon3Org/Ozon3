import setuptools


setuptools.setup(
    name="ozon3",
    author="Milind Sharma",
    author_email="milindsharma8@gmail.com",
    keywords=["aqi", "air quality", "world air quality", "api", "open source"],
    description="An open-source package to easily obtain real-time, historical,"
    "or forecasted air quality data for anywhere in the world. Reliable,"
    "accurate and simple.",
    license="GPLv3+",
    url="https://github.com/Milind220/Ozone",
    version="3.0.0",
    download_url="https://github.com/Milind220/Ozone/archive/refs/tags/v3.0.0.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy; python_version>='3'",
        "pandas; python_version>='3'",
        "requests; python_version>='3'",
        "openpyxl; python_version>='3'",
        "ratelimit; python_version>='3'",
        "js2py; python_version>='3'",
        "sseclient-py; python_version>='3'",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
