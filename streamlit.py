import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image


image = Image.open("gestacao.png")

# Exibir a imagem usando st.image
st.image(image, caption='Dados', use_column_width=True)


st.title("Pesquisa de dados em CSV")
uploaded_file = st.file_uploader("Faça upload do seu CSV aqui: ", type=["csv"])

#Verifica se o arquivo foi carregado
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    #Config para selecionar a coluna do csv
    selected_column = st.selectbox("Aqui está as opções de colunas para pesquisar no seu arquivo csv: ", df.columns)

    #Campo de pesquisa
    search_term = st.text_input("Faça uma pesquisa de forma coerente com a coluna selecionada na etapa anterior:")

    #Verifica se o termo de pesquisa foi inserido
    if search_term:
        #Realiza a pesquisa na coluna selecionada
        result_df = df[df[selected_column].astype(str).str.contains(search_term, case=False)]

        #Resultados
        if not result_df.empty:
            st.write("Resultado da pesquisa:")
            st.dataframe(result_df)

            #Criando um checkbox
            create_chart = st.checkbox("Criar Gráfico")

            #Verifica se o checkbox está marcado
            if create_chart:
                #Criando gráfico de barras
                st.subheader("Gráfico de Barras:")
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.countplot(data=result_df, x=selected_column, ax=ax)
                st.pyplot(fig)
            
                #Botão para fazer download do gráfico gerado na pesquisa
                buffer = BytesIO()
                fig.savefig(buffer, format="png")
                buffer.seek(0)
                st.download_button(
                    label="Download do Gráfico",
                    data=buffer,
                    file_name="grafico.png",
                    mime="image/png"
                )
        else:
            st.write("Nenhum resultado encontrado.")
            
            # Título da aplicação
st.title("Obteve sucesso em sua pesquisa?")

# Lista de opções
opcoes = ['sim', 'talvez', 'nao']

# Criando um botão de seleção de rádio
opcao_selecionada = st.radio("Selecione uma opção:", opcoes)

# Exibindo a opção selecionada
st.write(f"Você selecionou: {opcao_selecionada}")
