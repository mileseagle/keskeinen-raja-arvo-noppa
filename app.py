import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvolause: Nopan heittäminen")

st.sidebar.header("Asetukset")

# Käyttäjä voi valita heittojen määrän
heittojen_maara = st.sidebar.slider("Heittojen määrä", 100, 10_000, 1000, 100)

st.sidebar.subheader("Nopan todennäköisyydet")

# Lista todennäköisyyksille
probabilities = [0] * 6
remaining_prob = 1.0

for i in range(5):  # Käyttäjä voi säätää ensimmäiset 5 todennäköisyyttä
    max_val = 1.0  # Näytettävä alue aina 0 - 1, mutta rajataan käytettävä osa
    available_max = min(max_val, remaining_prob)  # Todellinen max perustuu jäljellä olevaan
    probabilities[i] = st.sidebar.slider(f"P({i+1})", 0.0, max_val, probabilities[i], 0.01, disabled=(remaining_prob == 0))
    probabilities[i] = min(probabilities[i], available_max)  # Estetään liian isot arvot
    remaining_prob -= probabilities[i]  # Päivitetään jäljellä oleva osuus

# Viimeinen todennäköisyys asetetaan automaattisesti
probabilities[5] = max(0.0, remaining_prob)
st.sidebar.write(f"P
