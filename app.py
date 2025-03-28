import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Title
st.title("Keskeinen Raja-arvolause: Noppasimulaatio")

# Sidebar controls
st.sidebar.header("Säädä todennäköisyydet")
probabilities = []
remaining_prob = 1.0

for i in range(6):
    max_val = remaining_prob if i < 5 else remaining_prob
    p = st.sidebar.slider(f"P({i+1})", 0.0, 1.0, max_val / 2, 0.01)
    probabilities.append(p)
    remaining_prob -= p

# Ensure probabilities sum to 1 (adjust last value)
probabilities[-1] += remaining_prob

# Number of dice rolls
n = st.slider("Heittojen lukumäärä (n)", 1, 100, 30)

# Simulation: 1000 repetitions
samples = np.random.choice([1, 2, 3, 4, 5, 6], size=(1000, n), p=probabilities)
sample_means = samples.mean(axis=1)

# Plot histogram
fig, ax = plt.subplots()
ax.hist(sample_means, bins=30, density=True, alpha=0.6, color='b', label="Simuloitu keskiarvojakauma")

# Overlay normal distribution
mu, sigma = np.mean(sample_means), np.std(sample_means)
x = np.linspace(min(sample_means), max(sample_means), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', label="Normaalijakauma")

ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()
st.pyplot(fig)

# Explanation at the bottom
st.markdown(
    "**Huom:** Tämä simulaatio toistetaan 1000 kertaa. Kun n kasvaa, jakauma lähestyy normaalijakaumaa keskeisen raja-arvolauseen mukaan."
)
