import matplotlib.pyplot as plt
import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_current_weather(city):
    """
    Fetch weather for the given city and return
    """
    # 1. Create the API endpoint URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # 2. Set query parameters
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # temperature in Celsius
    }
    
    # 3. Make the request
    response = requests.get(url, params=params)
    
    # 4. Parse JSON
    data = response.json()

    return data

def get_5_day_forecast(city):
    """
    Fetch 5 day forecast for given city
    """
    # 1. Create the API endpoint URL
    url = "https://api.openweathermap.org/data/2.5/forecast"
    
    # 2. Set query parameters
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # temperature in Celsius
    }
    
    # 3. Make the request
    response = requests.get(url, params=params)
    
    # 4. Parse JSON
    data = response.json()
    return data

# streamlit display
st.title("Weather information")
city = st.text_input("Please input the city you'd like weather information for: ")
if city:
    choice = st.radio(
        "Choose timeframe for weather information to get",
        ("Current", "24 hr Forecast")
    )
    if choice == "Current":
        # display given temperature, humidity, and condition for city
        weather_data = get_current_weather(city)
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]
        st.header(f"{city} Weather Right Now")
        st.write(f"Temperature: {temp}°C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Condition: {description}")
    elif choice == "24 hr Forecast":
        weather_type = st.radio(
                    "Choose weather information type",
                    ("Temperature", "Conditions", "Rain")
                )
        weather_data = get_5_day_forecast(city)
        data_24_hr = weather_data["list"][:8] # 3 hour data for next 24 hours
        weather_times = [partition["dt_txt"] for partition in data_24_hr]
        if weather_type == "Temperature":
            # display bar chart of temperature over time
            temps = [partition["main"]["temp"] for partition in data_24_hr]
            fig, ax = plt.subplots()
            ax.bar(weather_times, temps)
            ax.set_title("24 hr Temperature forecast")
            ax.set_xlabel("Time (UTC)")
            ax.set_ylabel("Temperature (°C)")
            ax.set_xticklabels(weather_times, rotation=45, ha='right')
            st.pyplot(fig)
        elif weather_type == "Conditions":
            # display columns of conditions at each time slice
            conditions = [partition["weather"][0]["description"] for partition in data_24_hr]
            columns = st.columns(len(weather_times))
            for index, column in enumerate(columns):
                with column:
                    st.write(f"{weather_times[index]}")
                    st.write(f"{conditions[index]}")
        elif weather_type == "Rain":
            # display line chart of rain
            # set to 0 if rain key doesn't exist
            rain = [partition["rain"]["3h"] if "rain" in partition.keys() else 0 for partition in data_24_hr]
            fig, ax = plt.subplots()
            ax.plot(weather_times, rain)
            ax.set_title("24 hr Rain forecast")
            ax.set_xlabel("Time (UTC)")
            ax.set_ylabel("Rainfall (mm)")
            ax.set_xticklabels(weather_times, rotation=45, ha='right')
            ax.set_ylim(bottom=0)
            st.pyplot(fig)