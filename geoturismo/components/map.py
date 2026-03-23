import folium

def gerar_mapa(ref, resultados, raio):
    mapa = folium.Map(
        location=[ref["latitude"], ref["longitude"]],
        zoom_start=14
    )

    folium.Marker(
        [ref["latitude"], ref["longitude"]],
        popup="Referência",
        icon=folium.Icon(color="red")
    ).add_to(mapa)

    folium.Circle(
        location=[ref["latitude"], ref["longitude"]],
        radius=raio,
        color="blue",
        fill=True
    ).add_to(mapa)

    for r in resultados:
        folium.Marker(
            [r["latitude"], r["longitude"]],
            popup=r["nome"]
        ).add_to(mapa)

    return mapa