import requests
from config import API_KEY


def geocodificar_endereco(endereco):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": endereco, "key": API_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    result = data["results"][0]
    location = result["geometry"]["location"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"],
        "endereco_formatado": result["formatted_address"]
    }


def buscar_locais_proximos(lat, lng, raio, tipo):
    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.googleMapsUri"
    }

    payload = {
        "includedTypes": [tipo],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": raio
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("places", [])