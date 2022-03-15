---
title: All Methods
layout: template
filename: methods
--- 

This page goes over all the methods that Ozone offers to fet

## To get air quality data using city names

### get_city_air

This method is used to get the air quality for a single city using its name.

#### Usage Example

```python
data = get_city_air(city='Tokyo', data_format='df', params=['co', 'no2'])
```

#### Arguments

**city** : str

The name of the city/location for which you want air quality data.

**data_format** : str

An optional argument to specify the format that you want the data returned in. You can choose between the following:

df - a Pandas dataframe. Selected by default  
csv - A CSV file (saved to your local directory)  
xslx - An Excel file (saved to your local directory)  
json - A JSON file (saved to your local directory)  

If this argument is left blank, a dataframe with the data is automatically returned

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi. Now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument as you fetch the new data for London.

**params** List[str]

An optional argument to specifiy which air quality parameters to get data for. If this is left blank then data for every air quality parameter is retrieved.  
You can choose from the following - pm25, aqi, pm10, o3, co, no2, so2, dew, h, p, t, w, wg



### get_multiple_city_air

This method is used to get the air quality for a single city using its name.

#### Usage Example

```python
get_multiple_city_air(cities=['Tokyo', 'Seattle', 'Sydney'], data_format='csv', params=['co', 'no2', 'dew', 'co2'])
```

#### Arguments

**city** : str

The name of the city/location for which you want air quality data.

**data_format** : str

An optional argument to specify the format that you want the data returned in. You can choose between the following:

df - a Pandas dataframe. Selected by default  
csv - A CSV file (saved to your local directory)  
xslx - An Excel file (saved to your local directory)  
json - A JSON file (saved to your local directory)  

If this argument is left blank, a dataframe with the data is automatically returned

**df** : pandas.Dataframe

An optional argument to pass in a dataframe that you may have previously retrieved. 

For example:- You previously used this method to get data for Delhi. Now you want to combine this existing dataframe with some new data from London, then you can consolidate both dataframes by passing the old one into this argument as you fetch the new data for London.

**params** List[str]

An optional argument to specifiy which air quality parameters to get data for. If this is left blank then data for every air quality parameter is retrieved.  
You can choose from the following - pm25, aqi, pm10, o3, co, no2, so2, dew, h, p, t, w, wg


*A Description of more methods is coming soon!*
