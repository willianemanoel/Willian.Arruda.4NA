import streamlit as st
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Previsão do Tempo", page_icon="⛅")

# Título com estilo
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    color: #1E90FF;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">🌤️ Previsão do Tempo Agora</p>', unsafe_allow_html=True)

# Chave da API da WeatherAPI (substitua pela sua chave pessoal)
API_KEY = "71aa1f6702f941b78a9231303252904"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Input da cidade
city = st.text_input("Digite o nome da cidade:", "São Paulo")

if st.button("Buscar Previsão"):
    if city:
        try:
            # Requisição à API
            params = {
                'key': API_KEY,
                'q': city,
                'lang': 'pt'
            }
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if 'error' in data:
                st.error(data['error']['message'])
            else:
                # Extração dos dados
                location = data['location']['name']
                country = data['location']['country']
                temp_c = data['current']['temp_c']
                feels_like = data['current']['feelslike_c']
                condition = data['current']['condition']['text']
                icon_url = "https:" + data['current']['condition']['icon']
                humidity = data['current']['humidity']
                wind_kph = data['current']['wind_kph']
                last_updated = data['current']['last_updated']

                # Exibição
                col1, col2 = st.columns(2)

                with col1:
                    st.image(icon_url, width=100)
                    st.metric("Temperatura Atual", f"{temp_c}°C")
                    st.metric("Sensação Térmica", f"{feels_like}°C")

                with col2:
                    st.write(f"**Local:** {location}, {country}")
                    st.write(f"**Condição:** {condition}")
                    st.write(f"**Umidade:** {humidity}%")
                    st.write(f"**Vento:** {wind_kph} km/h")
                    st.write(f"**Atualizado às:** {last_updated}")

        except Exception as e:
            st.error(f"Erro ao buscar dados: {e}")
    else:
        st.warning("Por favor, digite o nome de uma cidade.")
