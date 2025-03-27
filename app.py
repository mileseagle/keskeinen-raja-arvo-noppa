import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.title("🎲 Keskeinen Raja-arvolause - Noppasimulaatio")

# Sidebar for probability selection
st.sidebar.header("🎛 Säädä Nopan Todennäköisyyksiä")

# Initialize probability list
todennakoisyydet = []
sum_prob = 0

# User selects first 5 probabilities
for i in range(1, 6):  # P(1) to P(5)
    max_val = 1 - sum_prob  # Ensure sum never exceeds 1
    max_val = 1.0  # Ensure max_val is always properly set
    prob = st.sidebar.slider(f"P({i})", 0.0, max_val, max_val / 6, 0.01)
    todennakoisyydet.append(prob)
    sum_prob += prob

# The last probability is auto-adjusted
todennakoisyydet.append(1 - sum_prob)

st.sidebar.write(f"**P(6) automaattisesti:** {todennakoisyydet[-1]:.2f}")

# User selects number of dice rolls
heittojen_maara = st.slider("🔄 Nopan Heitot", 10, 5000, 1000, 10)

# Simulate dice rolls
otokset = np.random.choice([1, 2, 3, 4, 5, 6], size=(heittojen_maara, 100), p=todennakoisyydet)

# Calculate sample means
otosten_keskiarvot = otokset.mean(axis=1)

# Plot histogram
fig, ax = plt.subplots()
ax.hist(otosten_keskiarvot, bins=30, density=True, alpha=0.5, color='blue', label="Histogrammi")

# Add smooth KDE curve
kde = stats.gaussian_kde(otosten_keskiarvot)
x_vals = np.linspace(min(otosten_keskiarvot), max(otosten_keskiarvot), 200)
ax.plot(x_vals, kde(x_vals), color='red', linewidth=2, label="KDE (pehmennetty)")

ax.set_title("Otosten Keskiarvojakauma")
ax.set_xlabel("Keskiarvo")
ax.set_ylabel("Tiheys")
ax.legend()
st.pyplot(fig)

