# Ozone ☁️

[![PyPI version](https://badge.fury.io/py/ozon3.svg)](https://badge.fury.io/py/ozon3)
<a href="CONTRIBUTING.md#pull-requests"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
![GitHub](https://img.shields.io/github/license/Milind220/Ozone)


## The simplest AQI API

I want to make it easy to get your hands on accurate air quality data for your project, whatever it is. Ozone makes this as straightforward as typing out a few lines of code. Ozone uses the World Air Quality Index's API to fetch data, so you can trust the data you get to be accurate and reliable. ✅ 📈

###### You can view our complete documentation [here](https://milind220.github.io/Ozone/)

#### Table of Contents

[Install ozon3](#install-it-here)

[Getting your API token](#getting-your-api-token)

[Getting started](#getting-started)

[Contributing and submitting PR's](#contributing-and-submitting-pull-requests)


[Attributions](#World-Air-Quality-Index-and-EPA-attribution)

[License and TOS](#license-and-terms-of-service)

## Install it here!

```sh
pip install ozon3
```

## Getting your API token :atom:

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

## Contributing and submitting Pull requests

**We love PR's!**

Take a look at the [CONTRIBUTING.md](https://github.com/Milind220/Ozone/blob/main/CONTRIBUTING.md) file for details on how to go about this!


## World Air Quality Index and EPA attribution

This package is a wrapper around an API provided by the World Air Quality Index project. Without them as well as the US EPA, Ozone would not exist. Please consider visiting the WAQI website and contributing to their project if you have time:

[World Air Quality Index](https://aqicn.org/contact/)

[United States Environmental Protection Agency](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiBwZWSyYv2AhVkkNgFHaqsCWAQjBB6BAgaEAE&url=https%3A%2F%2Fwww.epa.gov%2Faboutepa&usg=AOvVaw2WGGvbn5P-QCjOB57cEcm5)

## LICENSE and Terms of Services 📰

1. Ozone is licensed under the GNU GENERAL PUBLIC LICENSE v3.0, and so it cannot be used for closed-source software or for monetary gain.
2. The WAQI API, which Ozone usees to provide data, has it's own [Acceptable Usage Policy](https://aqicn.org/api/tos/). Please refer to it for more details.

Enjoy using Ozone!
🥳 🍾 🚀
