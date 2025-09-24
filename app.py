import streamlit as st
import pandas as pd
from openai import OpenAI
from getpass import getpass

st.set_page_config(page_title="Comparador BSC: Manual vs IA", layout="centered")
st.title("Comparador de Estrategias del Balanced Scorecard")

st.markdown("""
Esta app permite comparar estrategias manuales redactadas por el estudiante con estrategias generadas por Inteligencia Artificial, basadas en un archivo Excel con la estructura del Balanced Scorecard.
""")

# Configuración del cliente OpenAI vía OpenRouter
HF_TOKEN = st.text_input("Ingresa tu token de OpenRouter (permiso 'chat/completions')", type="password")
if HF_TOKEN:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=HF_TOKEN,
    )

    # Subida de archivo Excel
    archivo = st.file_uploader("Carga tu archivo Excel (con columnas: Perspectiva, Objetivo, Meta, Indicador, Iniciativa)", type=["xlsx"])

    if archivo:
        df = pd.read_excel(archivo)
        st.dataframe(df)

        index = st.number_input("Selecciona el número de fila para trabajar:", 0, len(df)-1)
        objetivo = df.loc[index, 'Objetivo']
        iniciativa = df.loc[index, 'Iniciativa']

        st.subheader("Estrategia Manual del Estudiante")
        estrategia_manual = st.text_area("Escribe tu estrategia manual basada en el objetivo e iniciativa:")

        st.subheader("Estrategia Generada por IA")
        if st.button("Generar Estrategia con IA") and HF_TOKEN:
            try:
                prompt = f"""Eres un experto en estrategia organizacional.\nObjetivo: {objetivo}\nIniciativa: {iniciativa}\nGenera una estrategia clara, medible y coherente que relacione la iniciativa con el cumplimiento del objetivo."""

                completion = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                estrategia_ia = completion.choices[0].message.content
                st.success("Estrategia generada por IA:")
                st.text_area("Resultado IA", estrategia_ia, height=200)

                # Comparativo
                st.subheader("Comparativo Manual vs IA")
                st.markdown("**Estrategia Manual**")
                st.write(estrategia_manual)
                st.markdown("**Estrategia IA**")
                st.write(estrategia_ia)

            except Exception as e:
                st.error(f"Error al generar estrategia con IA: {e}")
        elif not HF_TOKEN:
            st.warning("Por favor, ingresa un token válido de OpenRouter para usar la IA.")