import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("Keskeinen raja-arvo ja noppa")

st.sidebar.header("Asetukset")

# Sliders for dice probabilities
probabilities = []
remaining_probability = 1.0

for i in range(6):
    max_val = remaining_probability if i < 5 else remaining_probability
    prob = st.sidebar.slider(f"P({i+1})", 0.0, 1.0, max_val / 6, 0.01)
    probabilities.append(prob)
    remaining_probability -= prob

todennakoisyydet = np.array(probabilities)

# Ensure probabilities sum to 1
if not np.isclose(sum(todennakoisyydet), 1.0):
    st.sidebar.error("Todennäköisyyksien summan tulee olla 1.0!")
    st.stop()

# Number of throws
n = st.slider("Heittojen lukumäärä (n)", 1, 100, 30)
heittojen_maara = 1000  # Number of simulations

# Simulating dice rolls
otoskeskiarvot = []
for _ in range(heittojen_maara):
    heitot = np.random.choice([1, 2, 3, 4, 5, 6], size=n, p=todennakoisyydet)
    otoskeskiarvot.append(np.mean(heitot))

# Plot histogram
fig, ax = plt.subplots()
ax.hist(otoskeskiarvot, bins=20, density=True, alpha=0.6, color='b', label="Otosten keskiarvot")

# Normal distribution for comparison
mu = np.dot([1, 2, 3, 4, 5, 6], todennakoisyydet)
sigma = np.sqrt(np.dot((np.array([1, 2, 3, 4, 5, 6]) - mu) ** 2, todennakoisyydet))
X = np.linspace(min(otoskeskiarvot), max(otoskeskiarvot), 1000)
normal_dist = stats.norm.pdf(X, mu, sigma / np.sqrt(n))
ax.plot(X, normal_dist, 'r', lw=2, label="Normaalijakauma")

ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()
st.pyplot(fig)

# Explanation text
st.write("Simulaatio suoritetaan 1000 kertaa jokaisella valitulla heittojen lukumäärällä n.")
