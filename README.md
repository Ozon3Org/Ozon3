# Ozone ☁️

[![PyPI version](https://badge.fury.io/py/ozon3.svg)](https://badge.fury.io/py/ozon3)
<a href="CONTRIBUTING.md#pull-requests"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
![GitHub](https://img.shields.io/github/license/Milind220/Ozone)
[![Buy Me a Coffee](https://img.shields.io/badge/buy_me_a_coffee-orange.svg?style=flat)](https://www.buymeacoffee.com/MilindSharma)



## The simplest AQI API

I want to make it easy to get your hands on accurate air quality data for your project, whatever it is. Ozone makes this as straightforward as typing out a few lines of code. Ozone uses the World Air Quality Index's API to fetch data, so you can trust the data you get to be accurate and reliable. ✅ 📈

###### You can view our complete documentation [here](https://milind220.github.io/Ozone/)

#### Table of Contents

[Install ozon3](#install-it-here)

[Getting your API token](#getting-your-api-token)

[Getting started](#getting-started)

[Contributing and submitting PR's](#contributing-and-submitting-pull-requests)

[Semantic Versioning System](#semantic-versioning-system)

[Attributions](#World-Air-Quality-Index-and-EPA-attribution)

[License and TOS](#license-and-terms-of-service)

## Install it here!

```sh
pip install ozon3
```

You can find more information on the PyPI page for Ozone [here](https://pypi.org/project/ozon3/) (called ozon3 on PyPI).

## Getting your API token 

To use Ozone, you must first request and get a your own unique API token 🎫. This is required to access for the underlying API to work 👮🏼‍♂️.

This is very easy to do, and takes no time at all as your token is generally emailed to you instantly.

Get your token [here](https://aqicn.org/data-platform/token/#/)!

## Getting started 🏃‍♂️

```python
import ozone as ooo

o3 = ooo.Ozone('YOUR_PRIVATE_TOKEN')
data = o3.get_city_air('CITY_NAME')
```

for many cities:

```python
data = o3.get_multiple_city_air([ARRAY OF CITY NAMES])
```

<hr>

### Examples In Action 🎬
![Gif of ozone.get_city_air()](/src/media/ozone_get_city_air.gif)

![Gif of ozone.get_multiple_city_air()](/src/media/ozone_get_multiple_city_air_updated.gif)


Sample output:
<img width="1065" alt="blehblhe" src="https://user-images.githubusercontent.com/68847270/159113134-e7e2d76d-c64d-4f96-83c4-e85d8c76b503.png">


## Contributing and submitting Pull requests

**We love PR's!**

Take a look at the [CONTRIBUTING.md](https://github.com/Milind220/Ozone/blob/main/CONTRIBUTING.md) file for details on how to go about this!

## Semantic Versioning System

Ozone uses a semantic versioning system to increment its release version number. Using this model, changes in version numbers can help indicate the meaning of modified code for each version.

See more information on semantic versioning [here](https://github.com/Milind220/Ozone/discussions/26).

## World Air Quality Index and EPA attribution

This package is a wrapper around an API provided by the World Air Quality Index project. Without them as well as the US EPA, Ozone would not exist. Please consider visiting the WAQI website and contributing to their project if you have time:

[World Air Quality Index](https://aqicn.org/contact/)

[United States Environmental Protection Agency](https://www.epa.gov/aboutepa)

## LICENSE and Terms of Services 📰

1. Ozone is licensed under the GNU GENERAL PUBLIC LICENSE v3.0, and so it cannot be used for closed-source software or for monetary gain.
2. The WAQI API, which Ozone uses to provide data, has it's own [Acceptable Usage Policy](https://aqicn.org/api/tos/). Please refer to it for more details.

Enjoy using Ozone!
🥳 🍾 🚀

#### _Created by [Milind Sharma](https://github.com/Milind220)_
