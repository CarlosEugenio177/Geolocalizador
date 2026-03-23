from streamlit_js_eval import streamlit_js_eval

def obter_localizacao():
    return streamlit_js_eval(
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