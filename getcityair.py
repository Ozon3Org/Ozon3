import sys
import ozon3 as ooo

# Check if the city is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python getcityair.py <city>")
    sys.exit(1)

# Get the city from the command-line argument
city = sys.argv[1]

o3 = ooo.Ozon3('YOUR_TOKEN')

try:
    # Fetch air quality data for the specified city
    data = o3.get_city_air(city)
    print(data)

except Exception as e:
    print(f"Error: {str(e)}")


