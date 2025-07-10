import streamlit as st
import folium
from streamlit_folium import st_folium
from route_core import get_lat_lng, build_distance_matrix, solve_tsp
import streamlit.components.v1 as components


st.set_page_config(page_title="Smart Route Planner", layout="wide")
st.title("🗺️ Smart Route Planner using ORS + TSP")

origin = st.text_input("Enter starting location:")

num_stops = st.number_input("How many stops?", min_value=1, max_value=10, step=1)
destinations = []
for i in range(num_stops):
    place = st.text_input(f"Destination {i+1}")
    destinations.append(place)

if st.button("Plan Optimal Route"):
    if not origin or any(p.strip() == "" for p in destinations):
        st.warning("Please fill all fields.")
    else:
        places = [origin] + destinations
        locations = {}
        for place in places:
            lat, lon = get_lat_lng(place)
            if lat is None:
                st.error(f"Could not find: {place}")
                st.stop()
            locations[place] = (lat, lon)

        with st.spinner("Calculating route..."):
            distances, durations = build_distance_matrix(places, locations)
            tsp_route = solve_tsp(places, distances)

        if not tsp_route:
            st.error("Could not compute optimized route.")
        else:
            st.success("✅ Optimized Visiting Order:")
            st.markdown(" → ".join(tsp_route))

            # Create route map using folium
            route_coords = [locations[place] for place in tsp_route]
            start_lat, start_lon = route_coords[0]
            fmap = folium.Map(location=[start_lat, start_lon], zoom_start=12)

            # Add markers
            for idx, (lat, lon) in enumerate(route_coords):
                folium.Marker(
                    location=[lat, lon],
                    popup=f"Stop {idx + 1}: {tsp_route[idx]}",
                    tooltip=tsp_route[idx]
                ).add_to(fmap)

            # Add route path
            folium.PolyLine(route_coords, color="blue", weight=4).add_to(fmap)

            # Save map to HTML
            map_file = "route_map.html"
            fmap.save(map_file)

            # Display the HTML map in Streamlit
            st.subheader("📍 Optimized Route Map")
            with open(map_file, 'r', encoding='utf-8') as f:
                components.html(f.read(), height=600, width=900)

            # Optional: download button
            with open(map_file, "rb") as f:
                st.download_button("⬇️ Download Map as HTML", f, file_name="route_map.html")
