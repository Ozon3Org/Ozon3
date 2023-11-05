import sys
import ozon3 as ooo

# Define a function to get a specific parameter for a given city
def get_specific_parameter(city, parameter):
    o3 = ooo.Ozon3('YOUR_TOKEN')

    try:
        # Fetch air quality data for the specified city
        data = o3.get_city_air(city)

        # Check if the parameter exists in the data
        if parameter in data:
            return data[parameter]
        else:
            return f"Parameter '{parameter}' not found in the data."

    except Exception as e:
        return f"Error: {str(e)}"

# Check if the city and parameter are provided as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python getspecificparam.py <city> <parameter>")
    sys.exit(1)

# Get the city and parameter from the command-line arguments
city = sys.argv[1]
parameter = sys.argv[2]

result = get_specific_parameter(city, parameter)
print(result)

