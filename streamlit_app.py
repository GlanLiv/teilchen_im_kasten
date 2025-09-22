import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Streamlit-Seitenlayout
st.set_page_config(page_title="Teilchen im Kasten", layout="centered")

st.title("🔬 Teilchen im Kasten – Wahrscheinlichkeitsanalyse")

st.markdown("""
Diese App zeigt die Wahrscheinlichkeitsdichte \( |\psi_n(x)|^2 \) für ein Teilchen im Kasten mit Länge \( L = 1 \).

Wähle die Quantenzahl \( n \) sowie ein Intervall, um:
- die Wahrscheinlichkeit zu berechnen, das Teilchen im Intervall zu finden,
- und (falls das Intervall [0, 1] ist) die Orte mit maximaler Wahrscheinlichkeitsdichte zu sehen.
""")

# Physikalische Konstante
L = 1

# Auswahl der Quantenzahl
n = st.selectbox("Quantenzahl n auswählen", options=[1, 2, 3, 4], index=1)

# Intervall-Eingabe
st.subheader("🔧 Intervall")
col1, col2 = st.columns(2)
with col1:
    x_min = st.number_input("Untere Intervallgrenze", min_value=0.0, max_value=1.0, value=0.0, step=0.01, format="%.3f")
with col2:
    x_max = st.number_input("Obere Intervallgrenze", min_value=0.0, max_value=1.0, value=1.0, step=0.01, format="%.3f")

if x_max <= x_min:
    st.error("Die obere Grenze muss größer als die untere sein.")
    st.stop()

# Wellenfunktion und Dichte
def psi_n(x, n):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)

def prob_density(x, n):
    return psi_n(x, n) ** 2

# Wahrscheinlichkeit im Intervall berechnen
P, _ = quad(lambda x: prob_density(x, n), x_min, x_max)

# Theorie: Maxima bei x = (2k+1)/(2n) * L
all_maxima = [((2 * k + 1) * L) / (2 * n) for k in range(n)]

# Plot vorbereiten
x_vals = np.linspace(0, L, 1000)
y_vals = prob_density(x_vals, n)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_vals, y_vals, label=r"$|\psi_n(x)|^2$")
ax.axvspan(x_min, x_max, color='orange', alpha=0.3, label="Intervall")
ax.axvline(x_min, color='red', linestyle='--', label="Intervallgrenze")
ax.axvline(x_max, color='red', linestyle='--')

# Falls Intervall [0, 1] ist → alle Maxima anzeigen
if x_min == 0.0 and x_max == 1.0:
    for x_m in all_maxima:
        ax.axvline(x_m, color='purple', linestyle='-.', alpha=0.7)

ax.set_xlabel("x")
ax.set_ylabel(r"$|\psi_n(x)|^2$")
ax.set_title(f"Wahrscheinlichkeitsdichte für n = {n}")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Ergebnisanzeige
st.subheader("📊 Ergebnisse")
st.markdown(f"""
- **Intervall:** [ {x_min:.3f} , {x_max:.3f} ]
- **Wahrscheinlichkeit im Intervall:**  
  \n\n
  \[
  P = {P:.6f}
  \]
""")

# Nur anzeigen, wenn Intervall exakt [0.0, 1.0]
if x_min == 0.0 and x_max == 1.0:
    st.subheader("📍 Orte mit maximaler Wahrscheinlichkeitsdichte (vollständiger Kasten)")
    for x in all_maxima:
        y = prob_density(x, n)
        st.markdown(f"- Ort: x = {x:.4f}, Wahrscheinlichkeitsdichte: |ψₙ(x)|² = {y:.4f}")
