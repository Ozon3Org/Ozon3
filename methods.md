---
title: All Methods
layout: template
filename: methods
--- 

This page goes over all the methods that Ozone offers to fetch air quality data:

* [get_city_air](#get_city_air) 
* [get_multiple_city_air](#get_multiple_city_air)
* [get_coordinate_air](#get_coordinate_air)
* [get_specific_parameter](#get_specific_parameter)
* [get_multiple_coordinate_air](#get_multiple_coordinate_air)
* [get_range_coordinates_air](#get_range_coordinates_air)
* [get city station options](#get_city_station_options)
* [reset_token](#reset_token)


## To get air quality data using city names

### get_city_air

Get the air quality data for a single city using its name.

#### Usage Example

```python
data = get_city_air(city='Tokyo')
```

#### Arguments

**city** : str

The name of the city/location for which you want air quality data.

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi. Now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument as you fetch the new data for London.

---

### get_multiple_city_air

Get the air quality for multiple cities using their names.

#### Usage Example

```python
get_multiple_city_air(cities=['Tokyo', 'Seattle', 'Sydney'])
```

#### Arguments

**cities** : List[str]

The name of the cities/locations for which you want air quality data. Pass them in as a list of strings.

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi. Now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument as you fetch the new data for London.

---

### get_specific_parameter

Get a single air quality parameter (example: CO or PM2.5) for a city.

#### Usage Example

```python
get_specific_parameter('Shanghai', 'pm2.5')
```

#### Arguments

**city** : str

The name of the city that you wish to get air quality data for. This argument is required.

**air_param** : str

The name of the parameter that you wish to fetch. Choose from ["aqi", "pm2.5", "pm10", "o3", "co", "no2", "so2", "dew", "h", "p", "t", "w", "wg"]. Gets all parameters by default.

---
## To get air quality data using geographical coordinates

### get_coordinate_air

Gets the air quality data for the closest measuring station to the input coordinate pair (latitude-longitude). 

#### Usage Example

```python
get_coordinate_air(lat=26.2041, long=28.0473)
```

#### Arguments

**lat** : float

The latitude coordinate

**long** : float

The longitude coordinate

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi, and now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument.

---

### get_multiple_coordinate_air

Get air quality data for several coordinate pairs.  
Input a list of coordinate pairs (lat-long) and get air quality data from the closest measuring station to each one. 

#### Usage Example

```python
get_multiple_coordinate_air(locations=[(12.4783,11.6143), (57.15780,106.75697), (-35.04664, 120.51377)])
```

#### Arguments

**locations** : List[Tuple[float, float]]

A list of coordinates, entered in tuples in this form (latitude, longitude).

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi, and now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument.

---

### get_range_coordinates_air

Get air quality data for all measuring stations between two latitude-longitude coordinate boundaries. Every station between the latitude bounds, and the longitude bounds will be polled for data.

> **NOTE**: This can be a very large number of stations sometimes and can take quite long - so don't be alarmed if it runs for a while.

#### Usage Example

```python
get_range_coordinates_air((20, 0), (0, 30))
```

#### Arguments

**lower_bound**: Tuple[float, float]

The lower boundary coordinate pair.

**upper_bound**: Tuple[float, float]

The upper boundary coordinate pair.

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi, and now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument.

---

### get_city_station_options

Get options for air quality measuring stations that Ozone can fetch data from. Pass in the name of the city that you want to fetch data from and Ozone will return a dataframe of options.

#### Usage Example

```python
get_city_station_options("jakarta")
```
#### Arguments

**city** : str

---
## Other methods

### reset_token

Method to change your private API token, if you set an incorrect one at first. 

#### Usage Example

```python
o3 = ooo.Ozone('INCORRECT_TOKEN')   # oh no! now what?

o3.reset_token('YOUR_NEW_TOKEN')   # No worries!
```
