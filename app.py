import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🎲 Keskeinen Raja-arvolause - Noppasimulaatio")

# Käyttäjä valitsee todennäköisyydet nopan silmälukujen välillä
st.sidebar.header("🎛 Säädä Nopan Todennäköisyyksiä")
todennakoisyydet = []
for i in range(1, 7):
    prob = st.sidebar.slider(f"P({i})", 0.0, 1.0, 1/6.0, 0.01)
    todennakoisyydet.append(prob)

# Normalisoidaan todennäköisyydet summaksi 1
todennakoisyydet = np.array(todennakoisyydet)
todennakoisyydet /= todennakoisyydet.sum()

# Käyttäjä valitsee heittojen määrän
heittojen_maara = st.slider("🔄 Nopan Heitot", 10, 5000, 1000, 10)

# Simuloidaan noppien heittoja
otokset = np.random.choice([1, 2, 3, 4, 5, 6], size=(heittojen_maara, 100), p=todennakoisyydet)

# Lasketaan keskiarvot
otosten_keskiarvot = otokset.mean(axis=1)

# Piirretään histogrammi
fig, ax = plt.subplots()
ax.hist(otosten_keskiarvot, bins=30, density=True, alpha=0.7, color='blue')
ax.set_title("Otosten Keskiarvojakauma")
ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
st.pyplot(fig)
