import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvolause: Nopan heittäminen")

st.sidebar.header("Asetukset")

# Käyttäjä voi valita heittojen määrän
heittojen_maara = st.sidebar.slider("Heittojen määrä", 100, 10_000, 1000, 100)

# Käyttäjä voi säätää noppalukujen todennäköisyyksiä
st.sidebar.subheader("Nopan todennäköisyydet")

# Käyttäjän syöttämät todennäköisyydet
probabilities = np.array([
    st.sidebar.slider(f"P({i})", 0.0, 1.0, 1.0 / 6, 0.01) for i in range(1, 7)
])

# Normalisoidaan todennäköisyydet niin, että niiden summa on aina 1
probabilities = probabilities / probabilities.sum()

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
