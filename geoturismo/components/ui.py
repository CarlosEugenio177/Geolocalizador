import streamlit as st

def card_local(local, i):
    st.markdown(f"### {i}. {local['nome']}")
    st.write(f"Endereço: {local['endereco']}")
    st.write(f"Distância: {local['distancia_km']} km")

    st.text_area(
        "Copiar para Uber/99",
        value=local["endereco"],
        height=60,
        key=f"copy_{i}"
    )

    st.markdown(f"[Abrir no Maps]({local['maps_url']})")
    st.divider()