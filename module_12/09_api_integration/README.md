# API Integration

**Objective:**  
Fetch external data and push to your service:
- GET weather data from OpenWeatherMap API
- POST transformed JSON to your internal endpoint

**Codex Prompt:**  
“Generate a Python script that retrieves current weather for a city using the OpenWeatherMap API, transforms the JSON to only include `temp`, `humidity`, and `description`, then posts it to `https://internal.example.com/ingest` via `requests`.”
