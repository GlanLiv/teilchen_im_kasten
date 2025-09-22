import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

st.set_page_config(page_title="Teilchen im Kasten – n und Intervallanalyse")

st.title("🔬 Teilchen im Kasten – Wahrscheinlichkeitsanalyse")

st.markdown("""
Dieses Tool zeigt die **Wahrscheinlichkeitsdichte** für ein Teilchen im Kasten bei gegebener Quantenzahl \( n \), 
und berechnet die **Wahrscheinlichkeit**, das Teilchen in einem bestimmten Intervall zu finden.

Es wird auch gezeigt, wie die Wellenfunktion und die Wahrscheinlichkeitsdichte aussehen.
""")

# Eingaben
n = st.slider("Quantenzahl n", min_value=1, max_value=10, value=2)
x_center = st.slider("Intervall-Mitte (x)", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
width = st.slider("Intervall-Breite", min_value=0.001, max_value=0.2, value=0.02, step=0.001)
show_maxima = st.checkbox("Wahrscheinlichste Orte (Maxima) anzeigen")

# Fix: L = 1
L = 1
x_min = max(0, x_center - width / 2)
x_max = min(L, x_center + width / 2)

# Definition der Wellenfunktion und Dichte
def psi_n(x, n):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)

def prob_density(x, n):
    return psi_n(x, n)**2

# Wahrscheinlichkeit im Intervall berechnen
P, _ = quad(lambda x: prob_density(x, n), x_min, x_max)

# Maxima berechnen
if show_maxima:
    # Für sin^2(nπx): Maxima bei x = (2k+1)L/(2n)
    max_positions = [((2*k + 1)*L)/(2*n) for k in range(n) if 0 <= ((2*k + 1)*L)/(2*n) <= L]
else:
    max_positions = []

# Plot
x_vals = np.linspace(0, 1, 1000)
y_vals = prob_density(x_vals, n)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_vals, y_vals, label=r"$|\psi_n(x)|^2$")
ax.axvspan(x_min, x_max, color='orange', alpha=0.3, label="Intervall")
ax.axvline(x_center, color='red', linestyle='--', label="Intervall-Mitte")

for x_m in max_positions:
    ax.axvline(x_m, color='green', linestyle=':', alpha=0.7, label="Maximum" if x_m == max_positions[0] else "")

ax.set_xlabel("x")
ax.set_ylabel(r"$|\psi_n(x)|^2$")
ax.set_title(f"Wahrscheinlichkeitsdichte für n = {n}")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Ergebnisanzeige
st.subheader("📊 Ergebnis")

st.markdown(f"""
- **Intervall:** [ {x_min:.4f} , {x_max:.4f} ]
- **Berechnete Wahrscheinlichkeit:**  
  \[
  P = \int_{{{x_min:.3f}}}^{{{x_max:.3f}}} |\psi_{n}(x)|^2 \, dx = {P:.6f}
  \]
""")

# Rechenweg anzeigen
st.subheader("🧮 Rechenweg")

st.markdown(f"""
- Wellenfunktion:
  \[
  \psi_{n}(x) = \sqrt{{\\frac{{2}}{{L}}}} \cdot \sin\\left(\\frac{{{n} \pi x}}{{L}}\\right)
  \]

- Wahrscheinlichkeitsdichte:
  \[
  |\psi_{n}(x)|^2 = \\frac{{2}}{{L}} \cdot \sin^2\\left(\\frac{{{n} \pi x}}{{L}}\\right)
  \]

- Da \( L = 1 \):
  \[
  |\psi_{n}(x)|^2 = 2 \cdot \sin^2({n}\pi x)
  \]

- Integriert über:
  \[
  x \in [{x_min:.3f}, {x_max:.3f}]
  \]
""")

if show_maxima and max_positions:
    st.subheader("📍 Wahrscheinlichste Orte (Maxima)")
    max_str = ", ".join([f"x = {x:.3f}" for x in max_positions])
    st.markdown(f"Die Maxima der Wahrscheinlichkeitsdichte für \( n = {n} \) liegen bei:\n\n**{max_str}**")

---

## 🧪 Wie du’s startest

1. Stelle sicher, dass du `streamlit`, `numpy`, `scipy` und `matplotlib` installiert hast:
   ```bash
   pip install streamlit numpy scipy matplotlib

