import openrouteservice
import time
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from ortools.constraint_solver import routing_enums_pb2, pywrapcp


API_KEY = os.getenv("ORS_API_KEY")
geolocator = Nominatim(user_agent="kiran_route_planner_app_12")
client = openrouteservice.Client(key=API_KEY)

def get_lat_lng(place_name):
    try:
        location = geolocator.geocode(place_name)
        time.sleep(1)
        if location:
            return location.latitude, location.longitude
        return None, None
    except GeocoderTimedOut:
        return None, None

def build_distance_matrix(places, locations):
    coords = [[lng, lat] for lat, lng in [locations[p] for p in places]]
    matrix = client.distance_matrix(
        locations=coords,
        profile='driving-car',
        metrics=['distance', 'duration'],
        units='km'
    )
    return matrix['distances'], matrix['durations']

def solve_tsp(places, distances):
    data = {
        'distance_matrix': distances,
        'num_vehicles': 1,
        'depot': 0
    }
    manager = pywrapcp.RoutingIndexManager(len(distances), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distances[from_node][to_node] * 1000)

    transit_cb_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_params.time_limit.FromSeconds(10)

    solution = routing.SolveWithParameters(search_params)
    if not solution:
        return []

    # Extract route
    index = routing.Start(0)
    tsp_order = []
    while not routing.IsEnd(index):
        tsp_order.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    tsp_order.append(manager.IndexToNode(index))  # return to depot
    return [places[i] for i in tsp_order]
