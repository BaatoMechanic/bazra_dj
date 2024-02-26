import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.app_helpers.gis import decode_geometries, send_request


@api_view(['GET'])
def reverse_geocode(request):
    lat = request.query_params.get("lat")
    lon = request.query_params.get("lon")
    url = f"http://nominatim:8080/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    response = send_request(url)
    return Response(response.json())


@api_view(['GET'])
def location_search(request):
    search_text = request.query_params.get("search")
    # url = f"http://nominatim:8080/search?q={search_text}&format=json&polygon_geojson=1&addressdetails=1&accept-language=en"
    url = f"http://nominatim:8080/search?q={search_text}&format=json&polygon_geojson=1&addressdetails=1"
    response = send_request(url)
    return Response(response.json())


@api_view(['GET'])
def route(request):
    source_lon = request.query_params.get("source_lon")
    source_lat = request.query_params.get("source_lat")
    destination_lon = request.query_params.get("destination_lon")
    destination_lat = request.query_params.get("destination_lat")
    url = f"http://maarga-container:5000/route/v1/driving/{source_lon},{source_lat};{destination_lon},{destination_lat}?overview=false&alternatives=true&steps=true"
    response = send_request(url)
    data = json.loads(response.content)
    data = decode_geometries(data)                
    return Response(data)


@api_view(['GET'])
def map(request):
    url = "http://bhugol-container:8080/geoserver/gwc/demo/bhumi_layer?gridSet=EPSG:3857&format=image/png"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return Response({"message": str(e)}, status=500)

    return Response(response.content, content_type='image/png')
