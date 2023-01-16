---
title: Getting Started
layout: template
filename: index
--- 

## Ozon3: Getting Started

Welcome to Ozon3 ☁️

In this guide, I'll walk you through the process of installing the Ozon3 package, and getting started with fetching data. Then, I'll cover each of the methods available through the Ozon3 API.

### Step 0: Setup

First, we need to make sure that you have the Ozon3 package on your computer. The easiest way to get it is by using pip.
Run the following command in your terminal/command prompt:
```sh
pip install ozon3
```
Ideally, keep up to date with the latest stable version by running:
```sh
pip install --upgrade ozon3
```
You can check if you have it already by running:
```sh
pip show ozon3
```

### Step 1: Get your API token

Ozon3 uses the World Air Quality Index's API under the hood, to fetch air quality data. You need to get your own private API token to use Ozon3's services.
Getting the token is easy and takes only a couple minutes. Register for the WAQI API with your email [here](https://aqicn.org/data-platform/token/#/), and they'll send you your token within a few minutes. 

> **Note:** Your API token is only for you to use. Keep it private and try not to reveal it in publicly visible code.

### Step 2: Import and Instantiate Ozon3

You can now go ahead and import Ozone into your Python code:
```python
import ozon3 as ooo
```
Don't worry if you want to give it a different alias than 'ooo' - that's just something we thought was funny

Next, Give ozon3 your token like this:
```python
o3 = ooo.Ozon3('YOUR_PRIVATE_TOKEN')
```

### Step 3: Get data!

#### For a single city

Pass in the name of the city, and optionally a specific list of parameters that you want to retrieve (if you don't enter this, Ozon3 will get all air pollutant parameters)
```python
o3.get_city_air(city='Hong Kong', params=['pm25', 'pm10', 'o3', 'dew'])
```

#### For many cities
```python
o3.get_multiple_city_air(cities=['Hong Kong', 'London', 'New Delhi', 'Los Angeles'], params=['no2', 'so2', 'aqi', 'co'])
```

##### Output:
> **Note:** Ozon3 will return a Pandas dataframe.


<img width="1065" alt="Screenshot 2022-03-14 at 12 07 47 PM" src="https://user-images.githubusercontent.com/68847270/158118100-9365665b-088d-4b79-a130-48ba51b3d937.png">


There you have it - Customized air quality data for a list of cities!
