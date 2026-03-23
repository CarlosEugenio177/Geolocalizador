try:
    from streamlit_js_eval import streamlit_js_eval
except ImportError:
    streamlit_js_eval = None


def obter_localizacao():
    if streamlit_js_eval is None:
        return None

    resultado = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => resolve({
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude
                }),
                () => resolve(null)
            );
        })
        """,
        key="geo"
    )

    return resultado