---
title: Getting Started
layout: template
filename: index
--- 

## Ozone: Getting Started

Welcome to Ozone ☁️

In this guide, I'll walk you through the process of installing the Ozone package, and getting started with fetching data. Then, I'll cover each of the methods available through the Ozone API.

### Step 0: Setup

Before doing anything, we need to make sure that you have the Ozone package on your computer. The easiest way to get it is by using pip.
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

Ozone uses the World Air Quality Index's API under the hood, to fetch air quality data. You need to get your own private API token to use Ozone's services.
Getting the token is really easy, and takes only a couple minutes. Register for the WAQI API with your email [here](https://aqicn.org/data-platform/token/#/), and they'll send you your token within a few minutes. 

> **Note:** Your API token is only for you to use. Keep it private and try not to reveal it in publicly visible code.

### Step 2: Import and Instantiate Ozone

You can now go ahead and import Ozone into your Python code:
```python
import ozone as ooo
```
Don't worry if you want to give it a different alias than 'ooo' - that's just something we thought was funny

Next, Give ozone your token like this:
```python
o3 = ooo.Ozone('YOUR_PRIVATE_TOKEN')
```

### Step 3: Get data!

#### For a single city

Pass in the name of the city, and optionally a specific list of parameters that you want to retrieve (if you don't enter this, Ozone will get all air pollutant parameters)
```python
o3.get_city_air(city='Hong Kong', params=['pm25', 'pm10', 'o3', 'dew'])
```

#### For many cities
```python
o3.get_multiple_city_air(cities=['Hong Kong', 'London', 'New Delhi', 'Los Angeles'], params=['no2', 'so2', 'aqi', 'co'])
```

##### Output:
> **Note:** Ozone will return a Pandas dataframe by default, but you can also choose between CSV file, Excel file, JSON file if you prefer any of those. Simply use the data_format argument for this!

<img width="1045" alt="Screenshot 2022-03-12 at 8 32 46 PM" src="https://user-images.githubusercontent.com/68847270/158023272-2843d6b8-2d0f-46b1-b9da-f190f3034696.png">


There you have it - Customized air quality data for a list of cities!


### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
