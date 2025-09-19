import streamlit as st

# -------------------------
# Rutinas con datos completos
# -------------------------
rutinas = {
    "A": [
        ["Chest Press", 32, "Maquina 20", "Asiento: 3; Respaldo: 3"],
        ["Pectoral Fly", 39, "Maquina 26", "Asiento: 3"],
        ["Tríceps Polea", 14.7, "Maquina 62", ""],
        ["Abdominal Maquina", 32, "Maquina 40", "Asiento: 3"],
        ["Dip Chin", 32, "", ""]
    ],
    "B": [
        ["Press Militar Maquina", 18, "Maquina 50", ""],
        ["Seated Leg Curl", 38, "Maquina 3", ""],
        ["Leg Extension", 36, "Maquina 2", ""],
        ["Abductor de Cadera", 50, "Maquina 4", ""],
        ["Adductor de Cadera", 45, "", "Maquina"]
    ],
    "C": [
        ["Leg Press", 63, "Maquina 1", ""],
        ["Remada Maquina Agarre Neutro", 36, "Maquina 30", ""],
        ["Vuelo Posterior Alternado Maquina", 32, "Maquina 26", ""],
        ["Curl Bíceps con Mancuerna", 14, "", ""],
        ["Lumbar Maquina", 63, "Maquina 43", ""]
    ]
}

# -------------------------
# Estado de rutinas
# -------------------------
if "estado" not in st.session_state:
    st.session_state.estado = {nombre: {"pendientes": ejercicios.copy(), "completados": []} for nombre, ejercicios in rutinas.items()}

# -------------------------
# Mostrar interfaz
# -------------------------
st.title("🏋️ FitnessApp")

opcion = st.radio("Elige tu entrenamiento:", ["A", "B", "C"])

estado = st.session_state.estado[opcion]

st.subheader("Ejercicios pendientes")
for i, e in enumerate(estado["pendientes"]):
    if st.button(f"✓ {e[0]} - {e[1]} kg", key=f"pendiente-{opcion}-{i}"):
        estado["pendientes"].remove(e)
        estado["completados"].append(e)
        st.experimental_rerun()

if not estado["pendientes"]:
    st.success("🏆 Rutina completada!")

st.subheader("Ejercicios completados")
for i, e in enumerate(estado["completados"]):
    if st.button(f"✗ {e[0]} - {e[1]} kg", key=f"completado-{opcion}-{i}"):
        estado["completados"].remove(e)
        estado["pendientes"].append(e)
        st.experimental_rerun()
