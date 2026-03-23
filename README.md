# 🗺️ Busca Inteligente por Proximidade (Turismo)

Este projeto é uma aplicação desenvolvida em **Python + Streamlit** que utiliza a **Google Maps Platform** para encontrar estabelecimentos próximos a um ponto de interesse.

## 🎯 Objetivo

O intuito principal é **auxiliar o turismo local**, permitindo que usuários encontrem facilmente locais como:

- Padarias
- Restaurantes
- Farmácias
- Hotéis
- Cafés
- Entre outros

Tudo isso com base em um ponto-chave, como uma igreja, praça ou ponto turístico.

---

## 🚀 Como funciona

1. O usuário informa um ponto de referência (ex: igreja)
2. O sistema converte esse local em coordenadas (Geocoding API)
3. Busca estabelecimentos próximos (Places API)
4. Exibe:
   - Lista de locais encontrados
   - Distância até o ponto
   - Avaliações
   - Link para o Google Maps
   - Mini mapa interativo

---

## 🛠️ Tecnologias utilizadas

- Python
- Streamlit
- Requests
- Pandas
- Google Maps Platform:
  - Geocoding API
  - Places API

---

## 📦 Instalação

pip install -r requirements.txt

---

## 🔑 Configuração

Crie um arquivo `.env` na raiz do projeto:

GOOGLE_MAPS_API_KEY=SUA_CHAVE_AQUI

---

## ▶️ Execução

streamlit run app.py

---

## 📌 Observações

- É necessário ativar faturamento na Google Cloud (mesmo com uso gratuito).
- O Google oferece **US$ 200/mês grátis**, suficiente para testes e uso leve.

---

## 🌍 Aplicação no Turismo

Este projeto pode ser utilizado para:

- Guias turísticos digitais
- Planejamento de viagens
- Descoberta de comércios locais
- Aplicações de mobilidade urbana
- Plataformas de recomendação geográfica

---

## 📈 Possíveis melhorias

- Filtros por avaliação mínima
- Exportação para Excel/CSV
- Integração com mapas interativos avançados
- Sistema de recomendação inteligente
- API própria para consumo externo

---

## 👨‍💻 Autor

Carlos Eugênio  
Estudante de Engenharia de Software  
Foco em Back-end, IA e Machine Learning
