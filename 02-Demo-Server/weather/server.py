import httpx
from fastmcp import FastMCP

mcp = FastMCP("Weather Server")
timeout = httpx.Timeout(connect=5.0, read=20.0, write=5.0, pool=5.0)

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the current weather for a given location"""
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout, http2=True) as client:
        try:
            print("Fetching weather data from wttr.in for location:", location)
            response = await client.get(f"https://wttr.in/{location}?format=j1")
            data = response.json()

            current = data["current_condition"][0]
            area = data["nearest_area"][0]["areaName"][0]["value"]

            return f"Weather in {area}: {current['temp_C']}°C, {current['weatherDesc'][0]['value']}"
        except Exception as e:
            return f"Error fetching weather data: {e}"

@mcp.tool()
async def get_forecast(location: str) -> str:
    """Get the forecast for a given location"""
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout, http2=True) as client:
        try:
            print("Fetching weather forecast data from wttr.in for location:", location)
            url = f"https://wttr.in/{location}?format=j1"
            response = await client.get(url, timeout=10)
            data = response.json()

            result = f"3-day forecast for {location}:\n"
            for day in data["weather"][:3]:
                result += f"{day['date']} - Lo: {day['mintempC']}, Hi: {day['maxtempC']}\n"

            return result
        except Exception as e:
            return f"Error fetching weather forecast: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")