import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvo ja noppa")

st.sidebar.header("Asetukset")

# Alustetaan todennäköisyydet
probabilities = []
remaining = 1.0
for i in range(6):
    if i < 5:
        prob = st.sidebar.slider(f"P({i+1})", 0.0, 1.0, remaining / (6 - i))
        adjusted_prob = min(prob, remaining)  # Varmistetaan, ettei ylitä 1.0:n summaa
        probabilities.append(adjusted_prob)
        remaining -= adjusted_prob
    else:
        probabilities.append(remaining)

st.sidebar.write("Todennäköisyyksien summan tulee olla 1.0.")

# Heittojen määrä
n = st.sidebar.slider("Nopan heittojen määrä (n)", 1, 1000, 100)

# Simulaatioiden määrä
num_simulations = 1000
st.sidebar.write(f"Jokaiselle n:lle suoritetaan {num_simulations} simulaatiota.")

# Simuloidaan satunnaismuuttujien summia
samples = np.random.choice([1, 2, 3, 4, 5, 6], size=(num_simulations, n), p=probabilities)
sample_means = samples.mean(axis=1)

# Piirretään histogrammi
fig, ax = plt.subplots()
ax.hist(sample_means, bins=30, density=True, alpha=0.7, color="blue", edgecolor="black")

# Normaalijakauman sovitus
mu, sigma = np.mean(sample_means), np.std(sample_means, ddof=1)
x = np.linspace(min(sample_means), max(sample_means), 100)
pdf = stats.norm.pdf(x, mu, sigma)
ax.plot(x, pdf, "r-", label="Normaalijakauma")

ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()

st.pyplot(fig)
