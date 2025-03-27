import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvolause: Nopan heittäminen")

st.sidebar.header("Asetukset")

# Käyttäjä voi valita heittojen määrän
heittojen_maara = st.sidebar.slider("Heittojen määrä", 100, 10_000, 1000, 100)

st.sidebar.subheader("Nopan todennäköisyydet")

# Käyttäjän syöttämät todennäköisyydet
probabilities = [0] * 6
remaining_prob = 1.0

for i in range(5):  # Käyttäjä säätää vain ensimmäiset 5 todennäköisyyttä
    max_val = min(1.0, remaining_prob)  # Varmistetaan, ettei summaa yli 1.0
    probabilities[i] = st.sidebar.slider(f"P({i+1})", 0.0, max_val, max_val / 2, 0.01)
    remaining_prob -= probabilities[i]

# Viimeinen todennäköisyys lasketaan automaattisesti niin, että summa on 1
probabilities[5] = max(0.0, remaining_prob)
st.sidebar.write(f"P(6) (automaattisesti): {probabilities[5]:.2f}")

# Simuloidaan nopanheittoja
otokset = np.random.choice([1, 2, 3, 4, 5, 6], size=(heittojen_maara, 100), p=probabilities)

# Lasketaan keskiarvot jokaisesta 100 kokeesta
keskiarvot = np.mean(otokset, axis=1)

# Piirretään histogrammi keskiarvoista
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(keskiarvot, bins=30, density=True, alpha=0.6, color="blue", edgecolor="black")

# Sovitetaan normaalijakauma päälle
mu, sigma = np.mean(keskiarvot), np.std(keskiarvot)
x = np.linspace(min(keskiarvot), max(keskiarvot), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), "r-", label="Normaalijakauma")

ax.set_title("Keskiarvojen jakauma (Nopanheitto)")
ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()

st.pyplot(fig)

st.write("""
Tämä sovellus havainnollistaa **keskeistä raja-arvolausetta** (Central Limit Theorem, CLT) käyttämällä **nopanheittoa**.
Kun otoskoko kasvaa, **keskiarvojen jakauma lähestyy normaalijakaumaa**, vaikka alkuperäinen jakauma (nopanheitto) ei olisi normaali.
""")
