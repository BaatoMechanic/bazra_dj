import requests


def send_request(url):
    return requests.get(url)


def decode_polyline(polyline_str, precision):
  index = 0
  lat = 0
  lng = 0
  coordinates = []
  shift = 0
  result = 0
  byte = None
  factor = 10 ** (precision if isinstance(precision, int) else 5)

  while index < len(polyline_str):
      byte = None
      shift = 1
      result = 0

      while True:
          byte = ord(polyline_str[index]) - 63
          index += 1
          result += (byte & 0x1f) * shift
          shift *= 32
          if byte < 0x20:
              break

      latitude_change = (-result - 1) / 2 if result & 1 else result / 2

      shift = 1
      result = 0

      while True:
          byte = ord(polyline_str[index]) - 63
          index += 1
          result += (byte & 0x1f) * shift
          shift *= 32
          if byte < 0x20:
              break

      longitude_change = (-result - 1) / 2 if result & 1 else result / 2

      lat += latitude_change
      lng += longitude_change

    #   coordinates.append([lat / factor, lng / factor])
      coordinates.append([lng / factor, lat / factor])

  return coordinates


def decode_geometries(data, precision=5):
    for route in data.get("routes", []):
        for leg in route.get("legs", []):
            for step in leg.get("steps", []):
                decoded_coordinates = decode_polyline(step["geometry"], precision)
                step["geometry"] = decoded_coordinates
    return data
