import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvo ja noppa - Simulaatiot")

st.sidebar.header("Valitse todennäköisyydet")

# Käyttäjä valitsee todennäköisyydet
probabilities = []
remaining = 1.0
for i in range(6):
    if i == 5:
        probabilities.append(remaining)
    else:
        prob = st.sidebar.slider(f"P({i+1})", 0.0, remaining, remaining / (6 - i), 0.01)
        probabilities.append(prob)
        remaining -= prob

toistoja = st.sidebar.slider("Heittojen lukumäärä (n)", 1, 100, 10)

# Simulaatioiden lukumäärä
simulaatioita = 1000

# Suoritetaan simulaatiot
samples = np.random.choice([1, 2, 3, 4, 5, 6], size=(simulaatioita, toistoja), p=probabilities)
means = samples.mean(axis=1)

# Histogrammi
fig, ax = plt.subplots()
ax.hist(means, bins=30, density=True, alpha=0.6, color='b', label="Simuloidut keskiarvot")

# Normaalijakauman tiheysfunktio
mu = np.mean(means)
sigma = np.std(means)
x = np.linspace(min(means), max(means), 100)
y = stats.norm.pdf(x, mu, sigma)
ax.plot(x, y, 'r-', label="Normaalijakauma")

ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()
st.pyplot(fig)

st.write("Simulaatio toistetaan 1000 kertaa.")
