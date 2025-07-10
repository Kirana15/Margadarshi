# MargaDarshi - Smart route planner using graph alogithhms of Google-ortools 

A web application that displays the optimized route for a custom trip by taking location names from the user. It leverages graph optimization (TSP) using Google OR-Tools and real-world distances via OpenRouteService.

## Features
Input your starting location and up to 10 destinations

Automatically geocodes all places using OpenStreetMap

Computes travel distances using OpenRouteService (driving)

Uses Google OR-Tools to solve the Travelling Salesman Problem

 Displays optimized route on an interactive map (Folium)

 Download your map as an offline HTML file

## How it works
1. User Input  
-Starting location
-Number of destinations
-Place names for each destination
The optimized route is calculated and the map is displayed  

2. Distance Calculation  
- Uses OpenRouteService and geopy to compute accurate driving distances

3. optimisation
- Google OR-Tools TSP solver determines the most efficient visiting order

4. Output  
- An optimized route map is shown with markers and route path
- Full trip path is displayed in a readable visiting order


## Folder Structure

Margadarshi/

├── python/ # Python scripts (route_core, route_app.py)

├── requirements.txt # Project dependencies

└── README.md # Project overview

## Requirements
 Core Logic
 
-openrouteservice
-geopy
-ortools

For Web Interface

-streamlit
-folium
## 🗺️ Margadarshi- Smart Route Planner

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://margadarshi-smart-route-planner-9hzmnack56cvbhvpwsappzb.streamlit.app/)

An interactive web app that optimizes your travel plan using real-world driving distances and graph algorithms (TSP with OR-Tools)…

## Disclaimer
This application uses OpenStreetMap data rendered via Folium. The map may not accurately reflect official international borders or jurisdictions. No geopolitical stance is expressed or implied.

## Author
Kirana BV

kiranaish15@gmail.com

linkedin.com/in/kirana-BV0106
