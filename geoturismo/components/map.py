import folium
from utils.formatters import formatar_avaliacao


def gerar_mapa(ref, resultados, raio):
    mapa = folium.Map(
        location=[ref["latitude"], ref["longitude"]],
        zoom_start=14,
        control_scale=True
    )

    folium.Marker(
        [ref["latitude"], ref["longitude"]],
        popup=f"Ponto de referência<br>{ref['endereco_formatado']}",
        tooltip="Ponto de referência",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(mapa)

    folium.Circle(
        location=[ref["latitude"], ref["longitude"]],
        radius=raio,
        color="blue",
        fill=True,
        fill_opacity=0.1
    ).add_to(mapa)

    for r in resultados:
        popup_html = f"""
        <b>{r['nome']}</b><br>
        {r['endereco']}<br>
        Distância: {r['distancia_km']} km<br>
        Avaliação: {formatar_avaliacao(r.get('avaliacao'), r.get('total_avaliacoes'))}<br>
        <a href="{r['maps_url']}" target="_blank">Abrir no Google Maps</a>
        """

        folium.Marker(
            [r["latitude"], r["longitude"]],
            popup=popup_html,
            tooltip=r["nome"],
            icon=folium.Icon(color="green", icon="ok-sign")
        ).add_to(mapa)

    return mapa