# 🧭 DataCoop25

Equip compost per **Cristina Huanca**, **Lucas**, **Maria Siles** i **Clara Priego**, estudiants d’enginyeria de dades de la **UAB**.

---

## 🗂️ Estructura del projecte
````
  DATACOOP25/
  ├── 3tops/ # Selecció dels municipis prioritaris
  ├── 10RENTAS/ # Dades de renda per municipi
  ├── alquiler/ # Informació sobre cost mitjà de lloguer
  ├── bancos/ # Dades d'entitats financeres per municipi
  ├── dashboard/ # Components del quadre de comandament Streamlit
  ├── parte_2/ # Scripts de models predictius i mapes
  ├── poblacion/ # Processament i fusió de dades de població
  ├── STREAMLITAPP/ # Aplicació Streamlit principal
  │
  ├── df_merged_output.csv # Dataset final integrat per anàlisi
  ├── dispersion.py # Gràfic de dispersió entre renda, població i bancs
  ├── poblacion_total_merged.py # Script de consolidació de dades poblacionals
  └── predictcompare.py # Model predictiu i comparació de rendiment
````
---

## 🎯 Descripció del projecte

Aquest repositori conté el desenvolupament complet del repte de **Caixa Enginyers**, proposat a **UAB The Hack 2025**.  
L’objectiu és **identificar ubicacions prioritàries per a l’expansió territorial** d’una entitat cooperativa, equilibrant criteris de **sostenibilitat econòmica** i **impacte social**.

---

## 🔍 Procés de treball

### 1. Recollida i neteja de dades
- Fonts: **INE** i portals institucionals oberts.  
- Variables principals: població, renda mitjana, cost de lloguer, presència d’entitats financeres, i indicadors d’inclusió.  
- Integració per municipi utilitzant codis **CPRO** i **CMUN** per garantir consistència.

### 2. Construcció del model de priorització
- Desenvolupament d’un **score compost** que pondera criteris econòmics i socials.  
- Normalització i calibratge per detectar municipis amb major propensió a beneficiar-se d’un punt d’atenció cooperatiu.

### 3. Geolocalització i visualització
- Assignació automàtica de coordenades per municipi.  
- Creació de **mapes de calor interactius** amb **Folium** i visualització en **Streamlit**.  
- Cada municipi inclou informació contextual i score al mapa.

### 4. Selecció d’ubicacions prioritzades
- Selecció final de **3 municipis** segons:
  - Viabilitat econòmica (cost de lloguer)  
  - Impacte social (baixa cobertura bancària)  
  - Capacitat operativa (població mínima)

### 5. Model de propensió avançat
- Model predictiu per estimar l’evolució del **score** a 1, 3 i 5 anys vista.  
- Variables considerades: digitalització, creixement demogràfic i PIB local.  
- Permet simular escenaris futurs per planificar l’expansió territorial.

---

## 📊 Resultats

- **Dashboard interactiu** amb gràfics i mapes que mostren la distribució del score.  
- **Model de propensió reutilitzable** per aplicar a noves zones o escenaris.  
- **Pipeline de dades** modular i fàcilment ampliable.

---

## 🌐 Visualització en Streamlit

Accés directe al dashboard desplegat:  
👉 [DataCoop25 App](https://datacoop-hackathon-caixa.streamlit.app/)
