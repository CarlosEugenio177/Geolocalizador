import os
import math
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def validar_api_key():
    if not API_KEY:
        st.error(
            "A variável GOOGLE_MAPS_API_KEY não foi encontrada. "
            "Crie um arquivo .env com sua chave da API do Google Maps."
        )
        st.stop()


def geocodificar_endereco(endereco: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": endereco,
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK" or not data.get("results"):
        raise ValueError(f"Não foi possível localizar o endereço: {endereco}")

    result = data["results"][0]
    location = result["geometry"]["location"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"],
        "endereco_formatado": result["formatted_address"]
    }


def calcular_distancia_km(lat1, lon1, lat2, lon2) -> float:
    raio_terra_km = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return raio_terra_km * c


def buscar_locais_proximos(
    latitude: float,
    longitude: float,
    raio_metros: int,
    tipo_local: str,
    max_resultados: int = 20
) -> list:
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
        "includedTypes": [tipo_local],
        "maxResultCount": max_resultados,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": raio_metros
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    return data.get("places", [])


def buscar_estabelecimentos(ponto_chave: str, cidade: str, tipo_local: str, raio_metros: int):
    consulta = f"{ponto_chave}, {cidade}, PI, Brasil"
    referencia = geocodificar_endereco(consulta)

    lugares = buscar_locais_proximos(
        latitude=referencia["latitude"],
        longitude=referencia["longitude"],
        raio_metros=raio_metros,
        tipo_local=tipo_local
    )

    resultados = []
    for lugar in lugares:
        loc = lugar.get("location", {})
        lat = loc.get("latitude")
        lng = loc.get("longitude")

        if lat is None or lng is None:
            continue

        distancia = calcular_distancia_km(
            referencia["latitude"],
            referencia["longitude"],
            lat,
            lng
        )

        resultados.append({
            "nome": lugar.get("displayName", {}).get("text", "Sem nome"),
            "endereco": lugar.get("formattedAddress", "Endereço não disponível"),
            "tipo": lugar.get("primaryType", "Não informado"),
            "distancia_km": round(distancia, 2),
            "avaliacao": lugar.get("rating"),
            "total_avaliacoes": lugar.get("userRatingCount"),
            "maps_url": lugar.get("googleMapsUri"),
            "latitude": lat,
            "longitude": lng
        })

    resultados.sort(key=lambda x: x["distancia_km"])

    return referencia, resultados


def montar_dados_mapa(referencia: dict, resultados: list) -> pd.DataFrame:
    pontos = [
        {
            "lat": referencia["latitude"],
            "lon": referencia["longitude"],
            "label": "Ponto de referência"
        }
    ]

    for item in resultados:
        pontos.append({
            "lat": item["latitude"],
            "lon": item["longitude"],
            "label": item["nome"]
        })

    return pd.DataFrame(pontos)


def main():
    st.set_page_config(page_title="Busca por proximidade", layout="wide")
    validar_api_key()

    st.title("Busca de estabelecimentos por ponto-chave")
    st.write(
        "Informe um ponto de referência em Teresina e encontre estabelecimentos "
        "em um raio específico usando Google Maps."
    )

    tipos_disponiveis = {
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

    with st.form("form_busca"):
        col1, col2 = st.columns(2)

        with col1:
            ponto_chave = st.text_input(
                "Ponto-chave",
                placeholder="Ex.: Igreja São Benedito"
            )
            cidade = st.text_input(
                "Cidade",
                value="Teresina"
            )

        with col2:
            tipo_label = st.selectbox(
                "Tipo de local",
                options=list(tipos_disponiveis.keys())
            )
            raio_km = st.slider(
                "Raio de busca (km)",
                min_value=1,
                max_value=20,
                value=5
            )

        buscar = st.form_submit_button("Buscar")

    if buscar:
        if not ponto_chave.strip():
            st.warning("Informe o ponto-chave.")
            st.stop()

        try:
            tipo_api = tipos_disponiveis[tipo_label]
            referencia, resultados = buscar_estabelecimentos(
                ponto_chave=ponto_chave.strip(),
                cidade=cidade.strip(),
                tipo_local=tipo_api,
                raio_metros=raio_km * 1000
            )

            st.success("Busca concluída com sucesso.")

            st.subheader("Ponto de referência")
            st.write(f"**Endereço encontrado:** {referencia['endereco_formatado']}")
            st.write(
                f"**Coordenadas:** {referencia['latitude']}, {referencia['longitude']}"
            )

            if not resultados:
                st.info("Nenhum local encontrado dentro do raio informado.")
                st.stop()

            st.subheader("Mini mapa")
            dados_mapa = montar_dados_mapa(referencia, resultados)
            st.map(dados_mapa, latitude="lat", longitude="lon", size=15)

            st.subheader("Resultados encontrados")

            for i, local in enumerate(resultados, start=1):
                with st.container():
                    st.markdown(f"### {i}. {local['nome']}")
                    st.write(f"**Endereço:** {local['endereco']}")
                    st.write(f"**Tipo:** {local['tipo']}")
                    st.write(f"**Distância:** {local['distancia_km']} km")
                    st.write(f"**Avaliação:** {local['avaliacao']}")
                    st.write(f"**Total de avaliações:** {local['total_avaliacoes']}")
                    st.write(f"**Latitude/Longitude:** {local['latitude']}, {local['longitude']}")
                    st.markdown(f"[Abrir no Google Maps]({local['maps_url']})")
                    st.divider()

        except Exception as e:
            st.error(f"Erro ao buscar dados: {e}")


if __name__ == "__main__":
    main()