import streamlit as st
import pandas as pd
import random

def load_data(file):
    # Carrega os dados sem considerar a primeira linha como cabeçalho
    data = pd.read_csv(file, header=None)
    return data[0].tolist()  # Assume que os tickets estão na primeira coluna

def generate_ticket_id(model, existing_tickets):
    firstCharOptions = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    otherChars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while True:
        firstChar = random.choice(firstCharOptions)
        randomChars = ''.join(random.choices(otherChars, k=5))
        ticket_id = f"{model}-{firstChar}{randomChars}"
        # Verifica duplicidade apenas pela parte após o traço
        if not any(ticket_id.split('-')[1] == ticket.split('-')[1] for ticket in existing_tickets):
            return ticket_id

def main():
    st.title("Gerador de Ticket ID")

    # Carregador de arquivo
    uploaded_file = st.file_uploader("Carregue um arquivo CSV", type='csv')
    if uploaded_file is not None:
        tickets = load_data(uploaded_file)
        st.success("Arquivo carregado com sucesso!")

        # Layout com duas colunas para os inputs
        col1, col2 = st.columns(2)

        with col1:
            model = st.text_input("Digite o modelo do ticket:")

        with col2:
            number_of_tickets = st.number_input("Quantos tickets você quer gerar?", min_value=1, max_value=1000, value=1, step=1)

        if st.button("Gerar Tickets"):
            if model:
                generated_tickets = [generate_ticket_id(model, tickets) for _ in range(number_of_tickets)]
                # Cria um DataFrame e exibe
                df_tickets = pd.DataFrame(generated_tickets, columns=["Tickets Gerados"])
                st.dataframe(df_tickets, use_container_width=True, hide_index=True)
            else:
                st.error("Por favor, insira um modelo para os tickets.")
    else:
        st.warning("Por favor, carregue um arquivo para começar.")

if __name__ == "__main__":
    main()
