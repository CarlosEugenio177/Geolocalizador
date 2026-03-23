import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

TIPOS_DISPONIVEIS = {
    "Padaria": "bakery",
    "Farmácia": "pharmacy",
    "Restaurante": "restaurant",
    "Supermercado": "supermarket",
    "Posto de gasolina": "gas_station",
    "Hospital": "hospital",
    "Academia": "gym",
    "Escola": "school",
    "Café": "cafe",
    "Hotel": "lodging"
}