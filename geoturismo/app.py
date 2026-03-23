import streamlit as st
from config import TIPOS_DISPONIVEIS
from services.google_maps import geocodificar_endereco, buscar_locais_proximos
from utils.distance import calcular_distancia_km
from components.map import gerar_mapa
from components.ui import card_local
from streamlit_folium import st_folium

st.set_page_config(layout="centered")

st.title("GeoTurismo")

ponto = st.text_input("Ponto de referência")
tipo_label = st.selectbox("Tipo", list(TIPOS_DISPONIVEIS.keys()))
raio = st.slider("Raio (km)", 1, 20, 5)

if st.button("Buscar"):
    ref = geocodificar_endereco(ponto)
    tipo = TIPOS_DISPONIVEIS[tipo_label]

    lugares = buscar_locais_proximos(
        ref["latitude"], ref["longitude"], raio * 1000, tipo
    )

    resultados = []
    for l in lugares:
        loc = l["location"]
        dist = calcular_distancia_km(
            ref["latitude"], ref["longitude"],
            loc["latitude"], loc["longitude"]
        )

        resultados.append({
            "nome": l["displayName"]["text"],
            "endereco": l["formattedAddress"],
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "maps_url": l["googleMapsUri"],
            "distancia_km": round(dist, 2)
        })

    resultados.sort(key=lambda x: x["distancia_km"])

    mapa = gerar_mapa(ref, resultados, raio * 1000)
    st_folium(mapa, height=400)

    for i, r in enumerate(resultados, 1):
        card_local(r, i)