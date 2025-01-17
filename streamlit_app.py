import streamlit as st
import os
import time

st.title("Egitto Svelato")
st.write(
    "Benvenuto nel programma di vendita dei biglietti."
)

def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)

with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)


import streamlit as st
import pandas as pd
import datetime

# Inizializza il carrello e lo storico
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'sales_history' not in st.session_state:
    st.session_state.sales_history = pd.DataFrame(columns=['Date', 'Tickets', 'Total Price'])

# Funzione per aggiungere biglietti al carrello
def add_to_cart(ticket_type, quantity, price):
    total_price = quantity * price
    st.session_state.cart.append({
        'ticket_type': ticket_type,
        'quantity': quantity,
        'total_price': total_price
    })

# Funzione per completare la vendita
def complete_sale():
    if st.session_state.cart:
        total_tickets = sum(item['quantity'] for item in st.session_state.cart)
        total_price = sum(item['total_price'] for item in st.session_state.cart)
        
        st.session_state.sales_history = st.session_state.sales_history.append({
            'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Tickets': total_tickets,
            'Total Price': total_price
        }, ignore_index=True)
        
        st.session_state.cart.clear()
        st.success("Vendita completata con successo!")

# Interfaccia utente
st.title("Museo - Vendita Biglietti")

# Selezione del tipo di biglietto e quantità
ticket_type = st.selectbox("Seleziona il tipo di biglietto:", ["Biglietto intero - €10", "Biglietto ridotto - €5"])
price = 10 if "intero" in ticket_type else 5
quantity = st.number_input("Quantità:", min_value=1, max_value=100, value=1)

if st.button("Aggiungi al carrello"):
    add_to_cart(ticket_type, quantity, price)
    st.success(f"{quantity} biglietti {ticket_type} aggiunti al carrello.")

# Visualizza il carrello
if st.session_state.cart:
    st.subheader("Carrello")
    cart_df = pd.DataFrame(st.session_state.cart)
    st.write(cart_df)

# Visualizzazione andamento vendite
if st.button("Completa vendita"):
    complete_sale()

# Visualizzazione storico vendite
st.subheader("Andamento Vendite")
if not st.session_state.sales_history.empty:
    st.line_chart(st.session_state.sales_history['Tickets'])
    st.write(st.session_state.sales_history)
else:
    st.write("Nessuna vendita effettuata finora.")
