import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvolause: Nopan heittäminen")

st.sidebar.header("Asetukset")

# Käyttäjä voi valita heittojen määrän
heittojen_maara = st.sidebar.slider("Heittojen määrä", 100, 10_000, 1000, 100)

st.sidebar.subheader("Nopan todennäköisyydet")

# Tallennetaan aiemmat arvot
if "probs" not in st.session_state:
    st.session_state.probs = [1/6] * 6  # Aloitetaan tasajakaumalla

def normalize_probs(idx, new_value):
    """Säätää muiden todennäköisyyksien arvoja niin, että summa pysyy 1:ssä"""
    remaining = 1 - new_value
    other_sum = sum(st.session_state.probs) - st.session_state.probs[idx]
    
    if other_sum > 0:
        scale = remaining / other_sum
    else:
        scale = 0  # Kaikki muut ovat 0, annetaan yksi arvo 1
    
    for i in range(6):
        if i != idx:
            st.session_state.probs[i] *= scale
    
    st.session_state.probs[idx] = new_value

# Luo liukusäätimet, joiden summa on aina 1, ja näytetään todennäköisyys vieressä
for i in range(6):
    cols = st.sidebar.columns([4, 1])  # Jako kahteen: liukusäädin (4) ja luku (1)
    new_value = cols[0].slider(f"P({i+1})", 0.0, 1.0, st.session_state.probs[i], 0.01)
    normalize_probs(i, new_value)
    cols[1].write(f"{st.session_state.probs[i]:.2f}")  # Näytetään arvo suoraan liukusäätimen vieressä

# Simuloidaan nopanheittoja
otokset = np.random.choice([1, 2, 3, 4, 5, 6], size=(heittojen_maara, 100), p=st.session_state.probs)

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
