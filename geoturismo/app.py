import streamlit as st
from streamlit_folium import st_folium

from config import TIPOS_DISPONIVEIS
from services.google_maps import geocodificar_endereco, buscar_locais_proximos
from utils.distance import calcular_distancia_km
from components.map import gerar_mapa
from components.ui import aplicar_estilo, card_local


def inicializar_estado():
    if "resultados" not in st.session_state:
        st.session_state.resultados = []
    if "referencia" not in st.session_state:
        st.session_state.referencia = None
    if "erro_busca" not in st.session_state:
        st.session_state.erro_busca = None
    if "busca_realizada" not in st.session_state:
        st.session_state.busca_realizada = False
    if "raio_atual" not in st.session_state:
        st.session_state.raio_atual = 5


st.set_page_config(page_title="GeoTurismo", page_icon="📍", layout="centered")
aplicar_estilo()
inicializar_estado()

st.title("GeoTurismo")
st.write("Encontre locais próximos a um ponto de referência.")

with st.form("form_busca", clear_on_submit=False):
    ponto = st.text_input(
        "Ponto de referência",
        placeholder="Ex.: Igreja São Benedito"
    )
    cidade = st.text_input("Cidade", value="Teresina")
    tipo_label = st.selectbox("Tipo", list(TIPOS_DISPONIVEIS.keys()))
    raio = st.slider("Raio (km)", 1, 20, 5)
    max_resultados = st.slider("Máximo de resultados", 5, 20, 10)

    submitted = st.form_submit_button("Buscar", use_container_width=True)

if submitted:
    try:
        st.session_state.erro_busca = None
        st.session_state.busca_realizada = False
        st.session_state.resultados = []
        st.session_state.referencia = None
        st.session_state.raio_atual = raio

        if not ponto.strip():
            raise ValueError("Digite um ponto de referência.")

        consulta = f"{ponto.strip()}, {cidade.strip()}, PI, Brasil"
        tipo = TIPOS_DISPONIVEIS[tipo_label]

        with st.spinner("Buscando locais..."):
            ref = geocodificar_endereco(consulta)

            lugares = buscar_locais_proximos(
                ref["latitude"],
                ref["longitude"],
                raio * 1000,
                tipo,
                max_resultados=max_resultados
            )

            resultados = []
            for l in lugares:
                loc = l.get("location", {})
                lat = loc.get("latitude")
                lng = loc.get("longitude")

                if lat is None or lng is None:
                    continue

                nome = l.get("displayName", {}).get("text", "Sem nome")
                endereco = l.get("formattedAddress", "Endereço não disponível")
                maps_url = l.get("googleMapsUri")
                tipo_local = l.get("primaryType", "Não informado")

                dist = calcular_distancia_km(
                    ref["latitude"],
                    ref["longitude"],
                    lat,
                    lng
                )

                resultados.append({
                    "nome": nome,
                    "endereco": endereco,
                    "latitude": lat,
                    "longitude": lng,
                    "maps_url": maps_url,
                    "tipo": tipo_local,
                    "distancia_km": round(dist, 2),
                    "avaliacao": l.get("rating"),
                    "total_avaliacoes": l.get("userRatingCount")
                })

            resultados.sort(key=lambda x: x["distancia_km"])

        st.session_state.referencia = ref
        st.session_state.resultados = resultados
        st.session_state.busca_realizada = True

    except Exception as e:
        st.session_state.erro_busca = str(e)
        st.session_state.busca_realizada = False

if st.session_state.erro_busca:
    st.error(f"Erro ao buscar: {st.session_state.erro_busca}")

if st.session_state.busca_realizada and st.session_state.referencia:
    ref = st.session_state.referencia
    resultados = st.session_state.resultados
    raio_atual = st.session_state.raio_atual

    st.success("Busca concluída com sucesso.")
    st.write(f"**Referência encontrada:** {ref['endereco_formatado']}")

    st.text_area(
        "Endereço exato para copiar e usar no Uber/99",
        value=ref["endereco_formatado"],
        height=70
    )

    if not resultados:
        st.info("Nenhum resultado encontrado.")
    else:
        mapa = gerar_mapa(ref, resultados, raio_atual * 1000)
        st_folium(mapa, height=420, width=None, key="mapa_resultados")

        for i, r in enumerate(resultados, 1):
            card_local(r, i)