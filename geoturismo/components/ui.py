import streamlit as st
from utils.formatters import formatar_avaliacao


def aplicar_estilo():
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 900px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def card_local(local, i):
    with st.container():
        st.markdown(f"### {i}. {local['nome']}")
        st.write(f"**Endereço:** {local['endereco']}")
        st.write(f"**Tipo:** {local['tipo']}")
        st.write(f"**Distância:** {local['distancia_km']} km")
        st.write(
            f"**Avaliação:** {formatar_avaliacao(local.get('avaliacao'), local.get('total_avaliacoes'))}"
        )
        st.write(f"**Latitude/Longitude:** {local['latitude']}, {local['longitude']}")

        st.text_area(
            f"Copiar para Uber/99 — {local['nome']}",
            value=local["endereco"],
            height=70,
            key=f"copy_{i}"
        )

        st.markdown(f"[Abrir no Google Maps]({local['maps_url']})")
        st.divider()