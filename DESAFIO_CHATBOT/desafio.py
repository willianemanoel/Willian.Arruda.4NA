import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configurações da página
st.set_page_config(
    page_title="Previsão do Tempo Premium",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .weather-card:hover {
        transform: translateY(-5px);
    }
    .highlight {
        font-size: 1.4rem;
        font-weight: bold;
        color: #1E90FF;
    }
    .section-title {
        border-left: 5px solid #1E90FF;
        padding-left: 10px;
        margin: 20px 0 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados da API (sua chave já incluída)
API_KEY = "71aa1f6702f941b78a9231303252904"
BASE_URL = "http://api.weatherapi.com/v1"

# Sidebar para configurações
with st.sidebar:
    st.title("⚙️ Configurações")
    city = st.text_input("Digite a cidade:", "São Paulo")
    days = st.slider("Dias de previsão:", 1, 7, 3)
    st.markdown("---")
    st.markdown("**Desenvolvido por Willian e Paulo usando:**")
    st.markdown("- [WeatherAPI.com](https://www.weatherapi.com/)")
    st.markdown("- Streamlit")
    st.markdown("- Plotly")

# Função para buscar dados
def get_weather():
    try:
        # Current weather
        current_url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}&lang=pt"
        current_data = requests.get(current_url).json()
        
        # Forecast
        forecast_url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={city}&days={days}&lang=pt"
        forecast_data = requests.get(forecast_url).json()
        
        return current_data, forecast_data
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return None, None

# Layout principal
st.title("🌦️ Previsão do Tempo Avançada")
st.markdown(f"### 📍 {city}")

if city:
    current, forecast = get_weather()
    
    if current and forecast:
        # Dados atuais
        local_time = datetime.strptime(current['location']['localtime'], '%Y-%m-%d %H:%M')
        
        # Layout em colunas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Agora")
            st.image(f"https:{current['current']['condition']['icon']}", width=100)
            st.markdown(f"<div class='highlight'>{current['current']['temp_c']}°C</div>", unsafe_allow_html=True)
            st.write(f"**{current['current']['condition']['text']}**")
            st.write(f"🌡️ Sensação: {current['current']['feelslike_c']}°C")
        
        with col2:
            st.markdown("### Detalhes")
            st.write(f"💧 Umidade: {current['current']['humidity']}%")
            st.write(f"🌬️ Vento: {current['current']['wind_kph']} km/h")
            st.write(f"☁️ Nuvens: {current['current']['cloud']}%")
            st.write(f"🌡️ Pressão: {current['current']['pressure_mb']} hPa")
        
        with col3:
            st.markdown("### Astronomia")
            st.write(f"🌅 Nascer do sol: {forecast['forecast']['forecastday'][0]['astro']['sunrise']}")
            st.write(f"🌇 Pôr do sol: {forecast['forecast']['forecastday'][0]['astro']['sunset']}")
            st.write(f"🌔 Fase lunar: {forecast['forecast']['forecastday'][0]['astro']['moon_phase']}")
            st.write(f"🕒 Hora local: {local_time.strftime('%H:%M')}")
        
        # Gráfico de previsão horária
        st.markdown("---")
        st.markdown("### 📊 Variação Horária (Hoje)")
        
        hourly_data = []
        for hour in forecast['forecast']['forecastday'][0]['hour']:
            time = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
            hourly_data.append({
                'Hora': time.strftime('%H:%M'),
                'Temperatura': hour['temp_c'],
                'Chuva (mm)': hour['precip_mm'],
                'Umidade': hour['humidity'],
                'Condição': hour['condition']['text']
            })
        
        df_hourly = pd.DataFrame(hourly_data)
        fig = px.line(df_hourly, x='Hora', y='Temperatura', 
                     title='Temperatura ao longo do dia',
                     markers=True,
                     labels={'Temperatura': 'Temperatura (°C)'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Previsão diária
        st.markdown("---")
        st.markdown(f"### 📅 Previsão para {days} dias")
        
        daily_data = []
        for day in forecast['forecast']['forecastday']:
            date = datetime.strptime(day['date'], '%Y-%m-%d')
            daily_data.append({
                'Dia': date.strftime('%a, %d/%m'),
                'Máx': day['day']['maxtemp_c'],
                'Mín': day['day']['mintemp_c'],
                'Chuva': day['day']['totalprecip_mm'],
                'Condição': day['day']['condition']['text'],
                'Ícone': day['day']['condition']['icon']
            })
        
        df_daily = pd.DataFrame(daily_data)
        
        cols = st.columns(days)
        for idx, row in df_daily.iterrows():
            with cols[idx]:
                st.markdown(f"#### {row['Dia']}")
                st.image(f"https:{row['Ícone']}", width=60)
                st.write(f"**{row['Condição']}**")
                st.write(f"⬆️ {row['Máx']}°C / ⬇️ {row['Mín']}°C")
                st.write(f"🌧️ {row['Chuva']}mm")
        
        # Mapa de calor de temperatura
        st.markdown("---")
        st.markdown("### 🔥 Mapa de Calor por Hora")
        
        heatmap_data = []
        for day in forecast['forecast']['forecastday']:
            for hour in day['hour']:
                time = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
                heatmap_data.append({
                    'Dia': time.strftime('%a'),
                    'Hora': time.hour,
                    'Temperatura': hour['temp_c']
                })
        
        df_heatmap = pd.DataFrame(heatmap_data)
        pivot_df = df_heatmap.pivot(index='Dia', columns='Hora', values='Temperatura')
        
        fig_heat = px.imshow(pivot_df, 
                            color_continuous_scale="thermal",
                            labels=dict(x="Hora do dia", y="Dia", color="Temperatura (°C)"))
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Alertas meteorológicos
        if 'alerts' in forecast and forecast['alerts']['alert']:
            st.markdown("---")
            st.markdown("### ⚠️ Alertas Meteorológicos")
            for alert in forecast['alerts']['alert']:
                with st.expander(f"{alert['headline']} (Até {alert['expires']})"):
                    st.write(alert['desc'])
        
# Rodapé
st.markdown("---")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Feito por Willian Arruda:41620 e Paulo Victor:85948")