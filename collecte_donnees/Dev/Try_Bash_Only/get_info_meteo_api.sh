#!/bin/sh

latitude=47.2488
longitude=6.0182

url="https://api.open-meteo.com/v1/forecast"
params="latitude=$latitude&longitude=$longitude&current[]=temperature_2m&current[]=relative_humidity_2m&current[]=apparent_temperature&current[]=is_day&current[]=precipitation&current[]=rain&current[]=weather_code&timeformat=unixtime&forecast_days=1"

response=$(curl -s "$url?$params")

current_temperature_2m=$(echo "$response" | jq -r '.current.temperature_2m')
current_relative_humidity_2m=$(echo "$response" | jq -r '.current.relative_humidity_2m')

echo "current_temperature_2m: $current_temperature_2m"
echo "current_relative_humidity_2m: $current_relative_humidity_2m"