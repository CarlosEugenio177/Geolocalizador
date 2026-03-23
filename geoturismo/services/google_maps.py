import requests
from config import API_KEY


def validar_api_key():
    if not API_KEY:
        raise ValueError(
            "GOOGLE_MAPS_API_KEY não encontrada. "
            "Crie um arquivo .env com a sua chave."
        )


def geocodificar_endereco(endereco):
    validar_api_key()

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": endereco,
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    status = data.get("status")
    results = data.get("results", [])

    if status != "OK" or not results:
        raise ValueError(f"Não foi possível localizar: {endereco}. Status: {status}")

    result = results[0]
    location = result["geometry"]["location"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"],
        "endereco_formatado": result["formatted_address"]
    }


def buscar_locais_proximos(lat, lng, raio, tipo, max_resultados=10):
    validar_api_key()

    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": ",".join([
            "places.displayName",
            "places.formattedAddress",
            "places.location",
            "places.rating",
            "places.userRatingCount",
            "places.googleMapsUri",
            "places.primaryType"
        ])
    }

    payload = {
        "includedTypes": [tipo],
        "maxResultCount": max_resultados,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": raio
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    return data.get("places", [])