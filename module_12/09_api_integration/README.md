# API Integration

## Project Overview
`weather_to_internal.py` acts as a bridge between the OpenWeatherMap API and your own service. It fetches current weather for a city and forwards a simplified payload to an internal endpoint.

## Variables
`WEATHER_API` and `TARGET_ENDPOINT` define the external and internal URLs. `CITY` and `OPENWEATHER_API_KEY` are read from environment variables when running the script.

## Instructions
Install `requests` and set the required environment variables. Then run `python weather_to_internal.py`. The script retrieves the temperature, humidity, and description for the specified city and posts that JSON to your internal service.

## Explanation
The code uses `requests.get` to call the weather API and `requests.post` to forward the transformed data. The small payload keeps only the needed fields, demonstrating how to mediate between two APIs in a simple workflow.
