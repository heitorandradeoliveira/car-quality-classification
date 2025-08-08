import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Classificação de Veículos",
    layout="wide"
)
st.markdown(
    """
    <div style="display:flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
        <a href="https://github.com/heitorandradeoliveira" target="_blank" style="text-decoration:none; font-weight:bold; font-size:16px;">
            🚀 github.com/heitorandradeoliveira
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_model_and_data():
    modelo = joblib.load("./app/modelo_nb.joblib")
    encoder = joblib.load("./app/encoder.joblib")
    class_categories = joblib.load("./app/class_categories.joblib")
    return modelo, encoder, class_categories


modelo, encoder, class_categories = load_model_and_data()

st.title("🚗 Previsão de Qualidade de Veículo")

# Exibir mensagem da acurácia (opcional, pode salvar e carregar de arquivo)
# Poderia salvar a acurácia em um arquivo texto durante o treino e ler aqui,
# mas vamos pular para simplicidade.

# Criar inputs para usuário, baseando-se no encoder.categories_
input_features = []
feature_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']

for i, col in enumerate(feature_names):
    opcoes = encoder.categories_[i].tolist()
    valor = st.selectbox(f"{col.capitalize()}:", opcoes, key=col)
    input_features.append(valor)

if st.button("Processar"):
    input_df = pd.DataFrame([input_features], columns=feature_names)
    input_encoded = encoder.transform(input_df)
    predict_encoded = modelo.predict(input_encoded)
    previsao = class_categories[predict_encoded][0]
    st.header(f"Resultado da previsão:  {previsao}")

    explicacoes = {
        'unacc': "Classificação: Inaceitável. Veículo com baixa qualidade ou condições ruins.",
        'acc': "Classificação: Aceitável. Veículo com qualidade básica, atende requisitos mínimos.",
        'good': "Classificação: Boa. Veículo com qualidade satisfatória para a maioria dos usuários.",
        'vgood': "Classificação: Muito Boa. Veículo de alta qualidade e desempenho superior."
    }
    explicacao = explicacoes.get(
        previsao, "Nenhuma explicação disponível para essa classificação.")
    st.info(explicacao)
