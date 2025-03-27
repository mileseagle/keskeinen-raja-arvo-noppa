import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvolause: Nopan heittäminen")

st.sidebar.header("Asetukset")

# Käyttäjä voi valita heittojen määrän
heittojen_maara = st.sidebar.slider("Heittojen määrä", 100, 10_000, 1000, 100)

st.sidebar.subheader("Nopan todennäköisyydet")

# Tallennetaan käyttäjän syöttämät alkuperäiset arvot
raw_probs = [st.sidebar.slider(f"P({i+1})", 0.0, 1.0, 1/6, 0.01) for i in range(6)]

# Skaalataan niin, että summa pysyy 1:n sisällä
sum_probs = sum(raw_probs)
if sum_probs > 0:
    todennakoisyydet = [p / sum_probs for p in raw_probs]  # Normalisoidaan
else:
    todennakoisyydet = [1/6] * 6  # Jos kaikki ovat nollia, käytetään tasajakaumaa

# Näytetään lopulliset skaalatut todennäköisyydet
st.sidebar.write("Todennäköisyydet normalisoituna:")
for i in range(6):
    st.sidebar.write(f"P({i+1}) = {todennakoisyydet[i]:.2f}")

# Simuloidaan nopanheittoja
otokset = np.random.choice([1, 2, 3, 4, 5, 6], size=(heittojen_maara, 100), p=todennakoisyydet)

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
